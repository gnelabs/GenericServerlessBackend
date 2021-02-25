
__author__ = "Nathan Ward"

import json
import logging
import os
import boto3
from secrets import token_urlsafe
from views import register_view
from api.utils import LambdaMessageEncoder

_LOGGER = logging.getLogger()
_LOGGER.setLevel(logging.INFO)

def generate_device_token() -> str:
    """
    Placeholder function to generate a unique device token in order to generate a 2FA challange.
    Update later on with your own 2FA rollout.
    """
    return token_urlsafe(16)

def generate_challenge(user: str, passwd: str, device_token: str, sendviasms: bool) -> str:
    """
    Generate a 2FA challenge ID. Can be rolled into other packages later.
    For now, generates a mock ID.
    """
    if sendviasms:
        challenge_type = "sms"
    else:
        challenge_type = "email"
    
    #Placeholder mock challange ID. To be filled in later with 2FA service.
    return 'mock_challangeid1'

@register_view('/api/login')
def lambda_handler(event, context):
    """
    Lambda function to receive external 2FA code.
    """
    try:
        body = json.loads(event['body'])
        username = body['username']
        password = body['password']
        sendviasms = body['sms']
    except KeyError:
        return {
            'statusCode': 400,
            'body': json.dumps(
                {'challenge_id': '', 'message': 'No parameters specified or missing parameters.'},
                cls=LambdaMessageEncoder
            ),
            'headers': {'Content-Type': 'application/json'}
        }
    
    device_token = generate_device_token()
    
    try:
        ddb_client = boto3.resource('dynamodb')
        table = ddb_client.Table(os.environ['CREDENTIALS_TABLE'])
        table.update_item(
            Key = {'credsPlatform': 'misc_generic'},
            UpdateExpression = "SET deviceToken = :a",
            ExpressionAttributeValues = {':a': device_token}
        )
    except Exception:
        _LOGGER.error('Unable stick 2FA device token into DDB.')
        return {
            'statusCode': 500,
            'body': json.dumps(
                {'challenge_id': '', 'message': 'Something went wrong server-side.'},
                cls=LambdaMessageEncoder
            ),
            'headers': {'Content-Type': 'application/json'}
        }
    
    challenge_id = generate_challenge(
        user = username,
        passwd = password,
        device_token = device_token,
        sendviasms = sendviasms
    )
    if challenge_id:
        return {
            'statusCode': 200,
            'body': json.dumps(
                {'challenge_id': challenge_id, 'message': 'Successfully generated challenge ID.'},
                cls=LambdaMessageEncoder
            ),
            'headers': {'Content-Type': 'application/json'}
        }
    else:
        return {
            'statusCode': 401,
            'body': json.dumps(
                {'challenge_id': '', 'message': 'Failed to login.'},
                cls=LambdaMessageEncoder
            ),
            'headers': {'Content-Type': 'application/json'}
        }