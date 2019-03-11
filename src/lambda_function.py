import json
import chargebee

from decimal import Decimal

chargebee.configure("test_tKRMcENOfS41Zp0sc50mAT4M3LIuw7Hu", "indyfin-test")


class CustomJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(CustomJsonEncoder, self).default(obj)


def generate_checkout_new_url(plan_id):
    customer_id = "janedoe@jdmail.com"
    result = chargebee.HostedPage.checkout_new({
        "subscription": {
            "plan_id": plan_id
        },
        "customer": {
            "id": customer_id,
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jd@jdmail.com"
        }
    })
    hosted_page = result._response['hosted_page']
    return json.dumps(hosted_page, cls=CustomJsonEncoder)


def confirm_subscription_details(hoste_pae_id):
    result = chargebee.HostedPage.retrieve(hoste_pae_id)
    content = result.hosted_page.content
    subscription = content.subscription
    customer = content.customer
    return_obj = {
        "subscriptionId": subscription.id,
        "subscriptionPlan": subscription.plan_id,
        "customerId": customer.id
    }
    # TODO - 1. Link subscription ID and plan_id with the customer - this is important
    # TODO - 2. Based on if link is present, display subscription details
    #           to customer when they sign in (see get_subscription_details method)
    #           You can make this call when you are loading customer details, I
    #           have just implemented it here for example purposes
    return json.dumps(return_obj, cls=CustomJsonEncoder)


def get_subscription_details(subscription_id):
    result = chargebee.Subscription.retrieve(subscription_id)
    return {
        "plan_id": result.subscription.plan_id,
        "plan_status": result.subscription.status,
        "plan_start": result.subscription.trial_start,
        "plan_end": result.subscription.trial_end
    }


def lambda_handler(event, context):
    query_params = event["queryStringParameters"]
    if "plan_id" in query_params:
        body = generate_checkout_new_url(query_params["plan_id"])
    elif "hosted_page_id" in query_params:
        body = confirm_subscription_details(query_params["hosted_page_id"])
    else:
        body = get_subscription_details(query_params["subscription_id"])

    return {
        'statusCode': 200,
        'headers': {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        'body': body
    }

