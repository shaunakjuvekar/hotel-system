import json
import os
import boto3
from dotenv import load_dotenv
import jwt # pyJwt
from http import HTTPStatus
from typing import Any, Dict, List
from boto3.dynamodb.conditions import Key
from dynamodb_json import json_util as ddb_json




def main():
    token = ""  # get from Secrets Manager
    return list_hotels(token)

def list_hotels(token):
    load_dotenv()  # This line brings all environment variables from .env into os.environ
    response = {
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "OPTIONS, GET"
        },
        "body":"",
        "statusCode": HTTPStatus.OK,
    }    

    if not token:
        response["statusCode"] = HTTPStatus.BAD_REQUEST
        response["body"] = json.dumps({"Error":"Query string parameter 'event' is missing"})
        return response
    
    token_details = jwt.decode(token, options={"verify_signature":False})
    user_id = token_details.get("sub")

    region = os.environ.get("AWS_REGION")
    print("region: ", region)
    db_client = boto3.resource("dynamodb" , region_name = "us-west-2",
                                aws_access_key_id=os.environ['AWS_ACCESS_KEY'],
                                aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY']
                              )
    table = db_client.Table("Hotels")

    scan_response = table.scan(
        FilterExpression = Key("userId").eq(user_id)
    )

    hotels = ddb_json.loads(scan_response["Items"])

    response["body"] = json.dumps({"Hotels": hotels})
    
    print(response)

    return response


def handler(event, context):    
    token = event["queryStringParameters"]["token"]
    return list_hotels(token)


if __name__ == "__main__":
    main()

    

   