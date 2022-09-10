uimport json
import time
import boto3
import random
import pprint

from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from pprint import pprint
from datetime import datetime

def lambda_handler(event, context):
    ddb = boto3.resource('dynamodb')
    client = boto3.client('dynamodb')
    
    accounts = ddb.Table('accounts')
            
    phoneNumber = event['queryStringParameters']['phoneNumber']
    verificationCode = event['queryStringParameters']['verificationCode']
    #$phoneNumber = "6612031768"
    #$verificationCode = str("779202")
    
    response = accounts.query(
        KeyConditionExpression=Key('phoneNumber').eq(phoneNumber)
        )
    
    items = response['Items']
    #print(items[0]['verificationCode'])
    
    try:
        dbVerificationCode = str(items[0]["verificationCode"])
        firstName = str(items[0]["firstName"])
        lastName = str(items[0]["lastName"])
        address = str(items[0]["address"])
        addressLineTwo = str(items[0]["addressLineTwo"])
        city = str(items[0]["city"])
        emailAddress = str(items[0]["emailAddress"])
        zipCode = str(items[0]["zipCode"])
        
        params = {
            "firstName" : firstName, 
            "lastName" : lastName,
            "address" : address,
            "addressLineTwo" : addressLineTwo,
            "city" : city,
            "emailAddress" : emailAddress,
            "zipCode" : zipCode
            }
        
        print (dbVerificationCode)
        print(verificationCode)
        if (verificationCode == dbVerificationCode):
            
            return {
                "body" : params
                }
        else:
            return {
                "statusCode" : 400
            }
            
    except Exception as e:
        print(e)
        return {
            'statusCode' : 500,
            'body' : json.dumps('Faiaal')
    } 
