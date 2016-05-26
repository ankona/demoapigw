from __future__ import print_function

import logging
from decimal import *
import json
import uuid
import time
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.info('Loading...')

# Sample Test Event:
# {
#   "hello_log_db": "hello_log",
#   "who": "Chris"
# }

def store_message(table_name, who):
    dynamodb = boto3.resource('dynamodb')
    hello_table = dynamodb.Table(table_name)
    hello_table.put_item(
        Item={
            "hello_id": str(uuid.uuid4()),
            "who": who,
            "timestamp": Decimal(time.time())
        }
    )

def lambda_handler(event, context):
    if "log_level" in event:
        log_level = event["log_level"].upper()
        if log_level in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            logger.setLevel(getattr(logging, log_level))
    if not "hello_log_db" in event:
    	logger.error("Unable to continue. The table_name could not be found. Check the stageVariables.")
        return "An internal error occurred."
        
    table_name = event['hello_log_db']
    guest_name = event['who']
    store_message(table_name, guest_name)
    return "Hello, {0}!".format(guest_name)