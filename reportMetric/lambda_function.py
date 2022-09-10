import json
import time
import boto3
import random
import base64
import googlemaps

from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

from datetime import datetime

gmaps = googlemaps.Client(key='AIzaSyBPUUIC3mXSlfSNsATFSskmbGNMFliAjJ4')

def lambda_handler(event, context):
    ddb = boto3.resource('dynamodb')
    client = boto3.client('dynamodb')
    
    actions = ddb.Table('actions')
    account = ddb.Table('accounts')
    
    phoneNumber = event['queryStringParameters']['phoneNumber']
    #phoneNumber = "6612031768"
    
    ts = int(time.time())
        
    try:
        metric = event['queryStringParameters']['metric']
        value = event['queryStringParameters']['value']
        #metric="Location"
        #value="Location Changed"
        
        if (metric == "Location"):
            longitude = event['queryStringParameters']['longitude']
            latitude = event['queryStringParameters']['latitude']
            #longitude = -119.399750
            #latitude = 35.056990
            
            addressResult = gmaps.reverse_geocode((latitude, longitude))
            address = addressResult[0]['formatted_address']
            actions.put_item(
                Item={
                    'phoneNumber' : str(phoneNumber),
                    'metric' : str(metric),
                    'value' : str(value),
                    'longitude' : str(longitude),
                    'latitude' : str(latitude),
                    'address' : json.dumps(addressResult),
                    'ts' : ts
                }
            ) 
        else:
            actions.put_item(
                Item={
                    'phoneNumber' : str(phoneNumber),
                    'metric' : str(metric),
                    'value' : str(value),
                    'ts' : ts
                }
            ) 
        
        response = account.update_item(
            Key={
                'phoneNumber': str(phoneNumber)
            }, 
            UpdateExpression='SET last_checked_in = :newTime',  
            ExpressionAttributeValues={':newTime': ts},
            ReturnValues="UPDATED_NEW"
        )
        
        return {
            'statusCode' : 200,
            'body' : json.dumps('Success') + phoneNumber
        }
    except Exception as e:
        print(e)
        return {
            'statusCode' : 450,
            'body' : json.dumps('Faaail') + str(e)
        }

