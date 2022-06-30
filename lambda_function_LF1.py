import json
import boto3
import requests
from boto3.dynamodb.conditions import Key

host = 'https://search-ccs22-ikx7naonkhx3bqbsffouzpa3aq.us-east-1.es.amazonaws.com/'
region = 'us-east-1' 
service = 'es'
index = "posts"
url = host  + index + '/_search'

def lambda_handler(event, context):
    # TODO implement
    data_temp = json.dumps(event)
    
    data1 = json.loads(data_temp)
    
    qtext = event['queryStringParameters']['q']
    
    
    query = {
        "size": 25,
        "query": {
            "multi_match": {
                "query": qtext,
                "fields": ["tags"]
            }
        }
    }
    headers = { "Content-Type": "application/json" }
    r = requests.get(url, auth=("Test1", "Test1Test1!"), headers=headers, data=json.dumps(query))
    response = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": '*'
            },
        "isBase64Encoded": False
    }
   

    rdata = json.loads(r.text)
    result = rdata['hits']['hits']
    ridlist = []
    
    for row in result:
        rid = row['_id']
        ridlist.append(rid)
        
    
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('posts')
    
    plist = []
    
    for i in ridlist:
        
        if len(plist) == 3: break
    
        resp = table.query(KeyConditionExpression=Key('id').eq(i))
        if resp['Items']: plist.append(resp['Items'])
        
    response['body'] = json.dumps(plist)
    
    
    return response
