"""
A Flask web application for a simple voting system.
This module implements a web interface where users can vote between two options.
Votes are stored in Redis and each voter is tracked using a cookie.
"""

import json
import logging
import os
import random
import socket

from flask import Flask, g, make_response, render_template, request
from redis import Redis

option_a = os.getenv("OPTION_A", "Cats")
option_b = os.getenv("OPTION_B", "Dogs")
hostname = socket.gethostname()

app = Flask(__name__)

gunicorn_error_logger = logging.getLogger("gunicorn.error")
app.logger.handlers.extend(gunicorn_error_logger.handlers)
app.logger.setLevel(logging.INFO)


def get_redis():
    """
    Get or create a Redis connection.

    Returns:
        Redis: A Redis connection instance stored in Flask's application context.
    """
    if not hasattr(g, "redis"):
        g.redis = Redis(host="redis", db=0, socket_timeout=5)
    return g.redis


@app.route("/", methods=["POST", "GET"])
def hello():
    """
    Handle the main voting page requests.

    Returns:
        Response: A Flask response object containing the rendered voting page.
        For GET requests, displays the voting form.
        For POST requests, processes the vote and displays the updated form.
    """
    voter_id = request.cookies.get("voter_id")
    if not voter_id:
        voter_id = hex(random.getrandbits(64))[2:-1]

    vote = None

    if request.method == "POST":
        redis = get_redis()
        vote = request.form["vote"]
        app.logger.info("Received vote for %s", vote)
        data = json.dumps({"voter_id": voter_id, "vote": vote})
        redis.rpush("votes", data)

    resp = make_response(
        render_template(
            "index.html",
            option_a=option_a,
            option_b=option_b,
            hostname=hostname,
            vote=vote,
        )
    )
    resp.set_cookie("voter_id", voter_id)
    return resp


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True, threaded=True)
