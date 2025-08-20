from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_dynamodb as dynamodb,
    aws_apigateway as apigateway
)
from constructs import Construct
import os
class ApiCdkLabStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # DynamoDB Table
        table = dynamodb.Table(
            self, "ItemsTable",
            partition_key={"name": "id", "type": dynamodb.AttributeType.STRING},
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST
        )

        # Lambda Function
        lambda_fn = _lambda.Function(
            self, "MyLambda",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="lambda_function.handler",
            code=_lambda.Code.from_asset("lambda"),
            environment={
                "TABLE_NAME": table.table_name
            }
        )

        # Grant Lambda permissions to read/write the table
        table.grant_read_write_data(lambda_fn)

        # API Gateway with OpenAPI Spec (Swagger)
        api = apigateway.SpecRestApi(
            self, "ItemsApi",
            api_definition=apigateway.ApiDefinition.from_asset(
                os.path.join(os.path.dirname(__file__), "api/openapi.yaml")
            ),
            deploy=True
        )

        # Integrate Lambda with API Gateway
        lambda_integration = apigateway.LambdaIntegration(lambda_fn)
        api.root.add_method("ANY", lambda_integration)  # Fallback route