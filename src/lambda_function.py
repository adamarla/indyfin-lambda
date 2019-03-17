import json


def lambda_handler(event, context):
    body = {
        "plan_id": "123123123",
        "plan_status": "new_trial",
        "plan_start": "111219",
        "plan_end": "111224"
    }

    return {
        'statusCode': 200,
        'headers': {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        'body': json.dumps(body)
    }

