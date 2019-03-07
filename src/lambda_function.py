import json
import boto3
import chargebee

from decimal import Decimal

dynamodb = boto3.resource('dynamodb')


class CustomJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(CustomJsonEncoder, self).default(obj)


def generate_checkout_new_url(event):
    result = chargebee.HostedPage.checkout_new({
        "subscription": {
            "plan_id": event.get("plan_id")
        },
        "customer": {
            "first_name": "John",
            "last_name": "Doe",
            "email": "johnhdoe@jdmail.com"
        }
    })
    hosted_page = result._response['hosted_page']
    return json.dumps(hosted_page, cls=CustomJsonEncoder)


def lambda_handler(event, context):
    item = None
    investor = dynamodb.Table('Investor')
    try:
        response = investor.get_item(Key={'email': 'aa@abc.com'})
        item = response['Item']
    except Exception as e:
        print(e)
    risk_profile = {
        "horizon_years": 10,
        "upside": 0.25,
        "downside": 0.25,
        "item": item,
    }
    return {
        'statusCode': 200,
        'headers': {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        'body': generate_checkout_new_url(event)
    }

