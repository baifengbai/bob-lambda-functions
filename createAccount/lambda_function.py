import json
import time
import boto3
import random
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

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
    
    phoneNumber = event['queryStringParameters']['phoneNumber']
    #phoneNumber = "6612031768"
    
    response = accounts.query(
        KeyConditionExpression=Key('phoneNumber').eq(phoneNumber)
        )
    
    existing = response['Items']
    
    if (len(existing) != 0):
        return {
            'statusCode' : 300
        }
    else:
        ts = int(time.time())
        
        try:
            
            firstName = event['queryStringParameters']['firstName']
            lastName = event['queryStringParameters']['lastName']
            emailAddress = event['queryStringParameters']['emailAddress']
            address = event['queryStringParameters']['address']
            addressLineTwo = event['queryStringParameters']['addressLineTwo']
            city = event['queryStringParameters']['city']
            #state = event['queryStringParameters']['state']
            zipCode = event['queryStringParameters']['zipcode']
            password = event['queryStringParameters']['password']
            """
            firstName = "Chester"
            lastName = "Frazier"
            emailAddress = "cwfrazier@cwfrazier.com"
            address = "514 South Kern St"
            addressLineTwo = ""
            city = "Maricopa"
            state = "CA"
            zipCode = "93252"
            password = "azazazaz"
            """
            verificationCode = str(random.randrange(100000, 999999, 1))
            
            accounts.put_item(
                Item={
                    'phoneNumber' : str(phoneNumber),
                    'firstName' : str(firstName),
                    'lastName' : str(lastName),
                    'emailAddress' : str(emailAddress),
                    'address' : str(address),
                    'addressLineTwo' : str(addressLineTwo),
                    'city' : str(city),
                    #'state' : str(state),
                    'zipCode' : str(zipCode),
                    'password' : str(password),
                    'verificationCode' : str(verificationCode),
                    'last_checked_in' : ts,
                    'ts' : ts
                }
            ) 
            sendSms(phoneNumber, "Please enter the following number to verify your phone number: " + verificationCode)
            
            return {
                'statusCode' : 200,
                'verificationCode' : verificationCode
            }
        except Exception as e:
            print(e)
            return {
                'statusCode' : 400,
                'body' : json.dumps('Fail')
    }
