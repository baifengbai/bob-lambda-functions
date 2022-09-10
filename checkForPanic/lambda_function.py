import json
import boto3

def lambda_handler(event, context):
    ddb = boto3.resource('dynamodb')
    client = boto3.client('dynamodb')
    table = ddb.Table('accounts')

    done = False
    start_key = None
    while not done:
        if start_key:
            scan_kwargs['ExclusiveStartKey'] = start_key
        response = table.scan(s)
        display_movies(response.get('Items', []))
        start_key = response.get('LastEvaluatedKey', None)
        done = start_key is None


    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

