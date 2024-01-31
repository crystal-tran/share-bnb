import boto3
import os
from dotenv import load_dotenv
from botocore.exceptions import ClientError
import logging



load_dotenv()

access_key_id = os.environ['ACCESS_KEY_ID']
secret_access_key = os.environ['SECRET_ACCESS_KEY']
region = os.environ['REGION']
SHAREBNB_BUCKET = os.environ['BUCKET_NAME']


s3 = boto3.client(
    's3',
    region,
    aws_access_key_id=access_key_id,
    aws_secret_access_key=secret_access_key
)

# response = s3.list_buckets()

# print('Existing buckets:')
# for bucket in response['Buckets']:
#     print(f'  {bucket["Name"]}')

def upload_file(file_name, bucket=SHAREBNB_BUCKET, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    try:
        response_from_aws = s3.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    print("response from aws:", response_from_aws)
    return True

upload_file('default-pic.png')

def create_presigned_url(object_name, bucket=SHAREBNB_BUCKET, expiration=3600):
    """Generate a presigned URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """

    # Generate a presigned URL for the S3 object
    try:
        response = s3.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
        print("response from presigned url:", response)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response


pre_signed_url = create_presigned_url('default-pic.png')
# upload_file(pre_signed_url)