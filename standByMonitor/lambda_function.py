import json
from botocore.vendored import requests


def lambda_handler(event, context):
    try:
        for record in event['Records']:
            if record['eventName'] == 'INSERT':
                handle_insert(record)
            elif record['eventName'] == 'MODIFY':
                handle_modify(record)
            elif record['eventName'] == 'REMOVE':
                handle_remove(record)
                
    except Exception, e:
        return "Error"
        
def handle_insert(record):
    newImage = record['dynamodb']['NewImage']
    newId = newImage['id']['S']
    
    print('New ID: ' + newId)
    
def handle_modify(record):
    #url = "https://checkonmine.com/bob/api/sendSmsFromLambda.php"
    #postData = {'message' : 'hello'}
    #x = requests.post(url, postData)
    #print(x.status)
    #standByTime = record['dynamodb']['NewImage']
    #newStandByTime = newImage['stand_by_time']['N']
    
def handle_remove():
    print("remove")
