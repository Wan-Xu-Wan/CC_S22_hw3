import json
import boto3
import requests

def lambda_handler(event, context):
    # TODO implement
    data_temp = json.dumps(event)
    data = json.loads(data_temp)
    pid = data["id"]
    pdate = data["date"]
    ppost = data["posts"]
    
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('posts')
    
    with table.batch_writer() as batch:
        batch.put_item(Item={"id": pid, "date": pdate, "posts": ppost})


    return {
        
        'statusCode': 200,
        'body': json.dumps('Post successfully')
    }
