import json
import time
import boto3
import random
import pprint

from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientErrr
from pprint import pprint
from datetime import datetime

def encrypt(string):
    import hashlib
    from hashlib import md5
    m = hashlib.md5()
    m.update(string.encode('utf-8'))
    md5string=m.digest()
    return md5string

def sendSms(phoneNumber, message):
    region = "us-west-2"
    originationNumber = "+19302006018"
    destinationNumber = "+1" + phoneNumber
    applicationId = "03d7e7b8b2a94912abdd56afdd66cb09"
    messageType = "TRANSACTIONAL"
    registeredKeyword = "keyword_870717836641"
    senderId = "MySenderID"
    client = boto3.client('pinpoint',region_name=region)
    try:
        response = client.send_messages(
            ApplicationId=applicationId,
            MessageRequest={
                'Addresses': {
                    destinationNumber: {
                        'ChannelType': 'SMS'
                    }
                },
                'MessageConfiguration': {
                    'SMSMessage': {
                        'Body': message,
                        'Keyword': registeredKeyword,
                        'MessageType': messageType,
                        'OriginationNumber': originationNumber,
                        'SenderId': senderId
                    }
                }
            }
        )
        print(response)
    
    
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Message sent! Message ID: "
                + response['MessageResponse']['Result'][destinationNumber]['MessageId'])

def lambda_handler(event, context):
    ddb = boto3.resource('dynamodb')
    client = boto3.client('dynamodb')
    
    accounts = ddb.Table('accounts')
            
    #phoneNumber = event['queryStringParameters']['phoneNumber']
    #userPassword = event['queryStringParameters']['password']
    phoneNumber = "6612031768"
    userPassword = "azazazaz"
    
    response = accounts.query(
        KeyConditionExpression=Key('phoneNumber').eq(phoneNumber)
        )
    
    items = response['Items']
    print(items[0]['password'])
    
    try:
        dbPassword = items[0]["password"]
        print (dbPassword)
        
        if (userPassword == dbPassword):
            gVerificationCode = str(random.randrange(100000, 999999, 1))
            sendSms(phoneNumber, "Please enter the following number to verify your phone number: " + gVerificationCode)
            
            table = ddb.Table('accounts')
            response = table.update_item(
                Key={
                    'phoneNumber': str(phoneNumber)
                },
                UpdateExpression="set verificationCode=:gVerificationCode",
                    ExpressionAttributeValues={
                        ':gVerificationCode': gVerificationCode
                    },
                ReturnValues="UPDATED_NEW"
            )
            return {
                "status" : "success"
                }
            
    except Exception as e:
        print(e)
        return {
            'body' : {"status" : "fail"}
    }
