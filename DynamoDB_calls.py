from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)

def getTable():
    dynamodb = boto3.resource('dynamodb')
    try:
        table = dynamodb.create_table(
            TableName='Project',
            KeySchema=[
                {
                    'AttributeName': 'code',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                { 'AttributeName': 'code',
                    'AttributeType': 'S'}
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            } )
        print("creating new table..")
    except:
        print('using existing table..')
        table = dynamodb.Table('Project')
    table.meta.client.get_waiter('table_exists').wait(TableName='Project')
    print("items:", table.item_count)
    return table
def getItem(table, code):
    response = table.get_item(Key={'code': 'mecode' })
    try:
        return response["Item"]
    except KeyError:
        return None

def insertItem(table, code, desc):
    table.put_item(
        Item={
            'code': code,
            'description': desc, })
