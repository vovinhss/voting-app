# voting-app
A secure, end-to-end voting application showcasing modern DevSecOps practices

## Initial Setup
```sh
# ---Git configuration---
git config --global user.name <your_user>
git config --global user.email <your_email>
# Avoid re-entering credentials every time (using Github PAT)
git config --global credential.helper store

# Docker Installation (Ubuntu)
sudo apt update
sudo apt install docker.io -y

# Grant current user docker permission with sudo mode
sudo groupadd docker
sudo usermod -aG docker $USER
newgrp docker
```