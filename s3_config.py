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
# ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

s3 = boto3.client(
    's3',
    region,
    aws_access_key_id=access_key_id,
    aws_secret_access_key=secret_access_key
)


def upload_file(file_obj, object_name, bucket=SHAREBNB_BUCKET, ):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name

    # Upload the file
    try:
        s3.upload_fileobj(file_obj, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True




def create_presigned_url(object_name, expiration=60000, bucket_name=SHAREBNB_BUCKET):
    """Generate a presigned URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """

    # Generate a presigned URL for the S3 object

    try:
        response = s3.generate_presigned_url(
            'get_object',
            Params={
                    'Bucket': bucket_name,
                    'Key': object_name,
                    },
            ExpiresIn=expiration
            )
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response


# def allowed_file(filename):
#     """Accepts a filename.
#     Returns true if filename is one of the allowed extensions.

#     False if it's not in the list.
#     """

#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
