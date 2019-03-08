import json
import chargebee

from decimal import Decimal

chargebee.configure("test_tKRMcENOfS41Zp0sc50mAT4M3LIuw7Hu", "indyfin-test")


class CustomJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(CustomJsonEncoder, self).default(obj)


def generate_checkout_new_url(query_params):
    result = chargebee.HostedPage.checkout_new({
        "subscription": {
            "plan_id": query_params.get("plan_id")
        },
        "customer": {
            "id": "johndoe@jdmail.com",
            "first_name": "John",
            "last_name": "Doe",
            "email": "johnhdoe@jdmail.com"
        }
    })
    hosted_page = result._response['hosted_page']
    return json.dumps(hosted_page, cls=CustomJsonEncoder)


def lambda_handler(event, context):
    query_params = event["queryStringParameters"]
    return {
        'statusCode': 200,
        'headers': {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        'body': generate_checkout_new_url(query_params)
    }

