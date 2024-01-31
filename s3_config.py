import boto3
import os
from dotenv import load_dotenv

load_dotenv()

access_key_id = os.environ['ACCESS_KEY_ID']
secret_access_key = os.environ['SECRET_ACCESS_KEY']
region = os.environ['REGION']



s3 = boto3.client(
    's3',
    region,
    aws_access_key_id=access_key_id,
    aws_secret_access_key=secret_access_key
)

response = s3.list_buckets()

print('Existing buckets:')
for bucket in response['Buckets']:
    print(f'  {bucket["Name"]}')


def upload_file(file_name, bucket, object_name=None):
    """Upload file to an S3 bucket"""

    if object_name is None:
        object_name = os.path.basename(file_name)

    s3_client = boto3.client('s3')

    response = s3_client.upload_file(file_name, bucket, object_name)

    return True


upload_file("default-pic.png", "bml-share-bnb")