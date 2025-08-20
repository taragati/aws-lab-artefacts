### Initialize AWS CDK
mkdir api-stack
cd api-stack

cdk init app --language python

source .venv/bin/activate

pip install aws-cdk-lib constructs

> Copy api_cdk_stack.py content to your new project cdk stack file

> Copy folder lambda to your new project folder

### One Time
cdk bootstrap --force aws://559050223676/us-east-1

### Deploy
cdk deploy

### If existing SSM parameter to be deleted
aws ssm delete-parameter --name "/cdk-bootstrap/hnb659fds/version"

### Destory
cdk destroy

