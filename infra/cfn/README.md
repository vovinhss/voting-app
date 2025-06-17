# This is the guideline for setting up initial AWS EC2 machine

```sh
export SSH_KEY_DIR=${HOME}/.aws/.ssh
export SSH_KEY_NAME="vinhvo"

aws ec2 create-key-pair \
  --key-name ${SSH_KEY_NAME} \
  --query 'KeyMaterial' \
  --output text > ${SSH_KEY_DIR}/${SSH_KEY_NAME}.pem
chmod 400 ${SSH_KEY_DIR}/${SSH_KEY_NAME}.pem

aws cloudformation create-stack \
  --stack-name ec2-init-stack \
  --template-body file://init_ec2.yaml \
  --parameters ParameterKey=KeyName,ParameterValue=${SSH_KEY_NAME} \
  --capabilities CAPABILITY_NAMED_IAM
```
