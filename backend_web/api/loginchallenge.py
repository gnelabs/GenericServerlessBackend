
__author__ = "Nathan Ward"

import json
import logging
import os
from datetime import datetime, timezone, timedelta
import boto3
from views import register_view
from api.utils import LambdaMessageEncoder

_LOGGER = logging.getLogger()
_LOGGER.setLevel(logging.INFO)

@register_view('/api/loginchallenge')
def lambda_handler(event, context):
    """
    Lambda function placeholder to generate and store temporary tokens using
    2FA. For now just mocks the behavior.
    """
    try:
        body = json.loads(event['body'])
        code = body['code']
        challenge_id = body['challenge']
        username = body['username']
        password = body['password']
        sendviasms = body['sms']
    except KeyError:
        return {
            'statusCode': 400,
            'body': json.dumps(
                {'2fa_login_successful': False, 'message': 'No parameters specified or missing parameters.'},
                cls=LambdaMessageEncoder
            ),
            'headers': {'Content-Type': 'application/json'}
        }
    
    #Implement external 2FA service logic here.
    
    return {
        'statusCode': 200,
        'body': json.dumps(
            {'2fa_login_successful': True, 'message': 'Successfully authenticated. Logging in.'},
            cls=LambdaMessageEncoder
        ),
        'headers': {'Content-Type': 'application/json'}
    }