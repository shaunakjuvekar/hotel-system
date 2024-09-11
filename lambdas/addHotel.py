import os
import io
import jwt
import json
import uuid
import boto3
import base64
import logging
import multipart as python_multipart


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def parse_form(headers, body, boundary):
    fields, files = {}, {}

    def on_field(field):
        key = field.field_name.decode()
        value = field.value.decode()
        fields[key] = value

    def on_file(file):
        key = file.field_name.decode()
        files[key] = file
        print("Printing file: ", files[key])

    headers['Content-Type']= headers['content-type']
    
    content_type = headers.get('content-type')
    if content_type is None:
        logging.getLogger(__name__).warning("Your header misses Content-Type")
        raise ValueError("Your header misses Content-Type")

    # Extract the multipart/form-data part and remove whitespace
    content_type_part = content_type.split(';')[0].strip()
    boundary_part = content_type.split(';')[1].strip()

    # Update the headers with the modified Content-Type value
    new_headers: Dict[str, any] = {}
    new_headers['Content-Type'] = content_type_part+';'+boundary_part
   
    python_multipart.parse_form(headers= new_headers, input_stream = body, on_field= on_field, on_file= on_file)
    return fields, files


def lambda_handler(event, context):
    
    response_headers = {
        "Access-Control-Allow-Headers": "*",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "*"
    }
    
    request_headers = event['headers']

    body = event['body']
    
    if bool(event.get('isBase64Encoded')):
        body = base64.b64decode(body)
    else:
        body = body.encode('utf-8')
     
    # logger.info(f"Raw body content: {body[:500]}")  # Print the first 500 bytes
    boundary = extract_boundary(request_headers)
    fields, files = parse_form(request_headers, io.BytesIO(body), boundary)
    
    # logger.info(f"fields: {fields}")
    

    hotel_name = fields.get('hotelName')
    hotel_rating = fields.get('hotelRating')
    hotel_city = fields.get('hotelCity')
    hotel_price = fields.get('hotelPrice')
    user_id = fields.get('userId')
    id_token = fields.get('idToken')

    file = files.get('photo')
    file_name = file.file_name.decode()
    file_content=file.file_object.read()
    file.file_object.seek(0)
    
    logger.info(f"Test file content: {file_content[:500]}")  # Print the first 500 bytes
    
    # Log the file content length and type for debugging
    logger.info(f'File length: {len(file_content)}')
    logger.info(f'File content type: {type(file_content)}')
    
    # We now have the field values and the file.
    
    # Performing Authorization.
    # Authorization must be done at API Gateway Level using a Custom Lambda Authorizer
    # In this code it is done in the microservice for educational purposes
    
    token = jwt.decode(id_token, options={"verify_signature": False})
    group = token.get('cognito:groups')
    
    logger.info(group)

    if group is None or 'Admin' not in group:
        return {
            'statusCode': 401,
            'headers':response_headers,
            'body': json.dumps({
                'Error': 'You are not a member of the Admin group'
            })
        }

    bucket_name = os.environ.get('bucketName')
    region = os.environ.get('AWS_REGION')
    s3_client = boto3.client('s3', region_name=region)
    dynamoDb = boto3.resource('dynamodb', region_name=region)
    table = dynamoDb.Table('Hotels')
    
    logger.info(f"bucket: {bucket_name}")
    logger.info(f"region: {region}")
    logger.info(f"dynamoDb: {dynamoDb}")
    logger.info(f"table: {table}")
    try:
        
        # Upload the image to S3
        s3_client.put_object(
            Bucket=bucket_name,
            Key=file_name,
            Body=file_content
        )
    
        hotel = {
            "userId": user_id,
            "Id": str(uuid.uuid4()),
            "Name": hotel_name,
            "CityName": hotel_city,
            "Price": int(hotel_price),
            "Rating": int(hotel_rating),
            "FileName": file_name
        }
    
    
        # Store the hotel record in DynamoDb
        table.put_item(Item=hotel)
        
        sns_topic_arn = os.getenv("hotelCreationTopicArn")
        sns_client = boto3.client('sns')
        sns_client.publish(
            TopicArn=sns_topic_arn,
            Message= json.dumps(hotel)
        )
        
    except Exception as e:
        return {
            "statusCode": 500,
            'headers': response_headers,
            "body": json.dumps({
                "Error": traceback.format_exc()
            })
        }
    
    return {
        'statusCode': 200,
        'headers': response_headers,
        'body': json.dumps({"message": "ok"})
    }

    
def extract_boundary(headers):
    content_type = headers.get('content-type', '')
    boundary_start = content_type.find('boundary=')
    if boundary_start != -1:
        boundary_end = content_type.find(';', boundary_start)
        if boundary_end == -1:
            boundary_end = len(content_type)
        boundary = content_type[boundary_start + len('boundary='):boundary_end].strip()

        # Check if the boundary is enclosed in quotes and remove them if present
        if boundary.startswith('"') and boundary.endswith('"'):
            boundary = boundary[1:-1]

        return boundary

    return None