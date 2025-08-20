from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_dynamodb as dynamodb,
    aws_apigateway as apigateway,
    aws_iam as iam,
)
from constructs import Construct
import json

class CdkLabStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # DynamoDB Table
        table = dynamodb.Table(
            self, "ItemsTable",
            table_name="MyCDKTable",
            partition_key={"name": "id", "type": dynamodb.AttributeType.STRING},
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST
        )

        # Lambda Function
        lambda_fn = _lambda.Function(
            self, "MyLambda",
            function_name="MyCDKLambda",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="lambda_function.handler",
            code=_lambda.Code.from_asset("lambda"),
            environment={
                "TABLE_NAME": table.table_name
            }
        )

        # Grant Lambda permissions to read/write the table
        table.grant_read_write_data(lambda_fn)

        # Load YAML
        with open("./api/openapi.json") as f:
            spec = json.load(f)

        # Replace placeholder with correct Lambda invoke URI
        spec["paths"]["/items"]["get"]["x-amazon-apigateway-integration"]["uri"] = (
            f"arn:aws:apigateway:{self.region}:lambda:path/2015-03-31/functions/{lambda_fn.function_arn}/invocations"
        )
        spec["paths"]["/items"]["post"]["x-amazon-apigateway-integration"]["uri"] = (
            f"arn:aws:apigateway:{self.region}:lambda:path/2015-03-31/functions/{lambda_fn.function_arn}/invocations"
        )

        # Pass spec inline
        api = apigateway.SpecRestApi(
            self, "ItemsApi",
            rest_api_name="MyCDKApi",
            api_definition=apigateway.ApiDefinition.from_inline(spec)
        )

        # Grant API Gateway permission to call the Lambda
        lambda_fn.add_permission(
            "ApiGwInvoke",
            principal=iam.ServicePrincipal("apigateway.amazonaws.com"),
            action="lambda:InvokeFunction",
            source_arn=f"arn:aws:execute-api:{self.region}:{self.account}:{api.rest_api_id}/*/*"
        )
