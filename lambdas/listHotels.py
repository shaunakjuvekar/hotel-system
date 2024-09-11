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
    token = "eyJrbWQiOiJhR3RUSUl1bWg4UnZMMG1ObjVZOHB1dVhxaEVseksyQ291NDl1TjhaOXljPSIsImFsZyI6IlJTMjU2In0.eyJhdF9oYXNoIjoiS2ZDVFFKNENyZmJMcWdiSjFuT2M5QSIsInN1YiI6IjY4ZTE5M2MwLTMwZDEtNzAwOS0xZTIzLWIwMjliZTFmZGFlYSIsImNvZ25pdG86Z3JvdXBzIjpbIkFkbWluIl0sImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtd2VzdC0yLmFtYXpvbmF3cy5jb21cL3VzLXdlc3QtMl9UYndsMUhFZEQiLCJjb2duaXRvOnVzZXJuYW1lIjoiNjhlMTkzYzAtMzBkMS03MDA5LTFlMjMtYjAyOWJlMWZkYWVhIiwiYXVkIjoiMzZtYm8zY3AwcnMzdm1nNmdiZHYzOXJvbTYiLCJldmVudF9pZCI6IjljOWY5ZTFmLTliMWYtNGNlYi1iMWJlLTc5MTNhNjlhZDA1ZSIsInRva2VuX3VzZSI6ImlkIiwiYXV0aF90aW1lIjoxNzI1MTMwNzkyLCJleHAiOjE3MjUxMzQzOTIsImlhdCI6MTcyNTEzMDc5MiwianRpIjoiYzEzYWZiOTUtNzk2MC00ODMyLTg2MjMtNTVmNTQ3Y2EyYTAzIiwiZW1haWwiOiJhZG1pbkBteWRvbWFpbi5jb20ifQ.CFyOqYtAETD9Jza5yu2aqTYBA4NehL2f5umcO36MGVxNgcXGrYsfFF5F6WwgNScKKVl8sf_MW6KRHcOLDT7h99aA9mA9V59x-L8ZN2Bz_90GOV4ta2Nz_ebPlzpi2nE_AS-b70hhyj6XaX5seFQn-Ac7doe8fX6y3X_Yt4u4Pvk4dEwdi8RWZMgbyajVmpO8Frm0EQWcGqHUXCLcR3tSHnIFviwOOAATfcaryi0POZpDet23URJ9gDE2DmHUUcv7jghtQR72ytu__oz4jyqEw-BjB-kNrzHUZzxAjYmK9Qf78nxZjJf72x82Yr8DK-QvcOLK3Gs51JfGg688ksjlTg"
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

    

   