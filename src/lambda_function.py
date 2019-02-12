import json
import boto3

from decimal import Decimal

dynamodb = boto3.resource('dynamodb')

class CustomJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(CustomJsonEncoder, self).default(obj)

def lambda_handler(event, context):
    item = None
    investor = dynamodb.Table('Investor')
    try:
        response = investor.get_item(Key={'email': 'aa@abc.com'})
        item = response['Item']
    except Exception as e:
        print(e)
    risk_profile = {
        "horizon_years": 15,
        "upside": 0.3,
        "downside": 0.25,
        "item": item,
    }
    return {
        'statusCode': 200,
        'headers': {
            "Content-Type": "application/json", 
            "Access-Control-Allow-Origin": "*"
        },
        'body': json.dumps(risk_profile, cls=CustomJsonEncoder)
    }

