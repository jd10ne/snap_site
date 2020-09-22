import logging
import os
import datetime

import boto3
from botocore.exceptions import ClientError
from google.cloud import storage
from google.cloud import exceptions

AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID'] if 'AWS_ACCESS_KEY_ID' in os.environ.keys() else ''
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY'] if 'AWS_SECRET_ACCESS_KEY' in os.environ.keys() else ''
PROVIDER = os.environ['PROVIDER'] if 'PROVIDER' in os.environ.keys() else 'AWS'

def put_obj(file_path, bucket):
    print("PROVIDER: {}".format(PROVIDER))
    if PROVIDER == 'AWS':
        return put_s3(file_path, bucket)
    return put_gcs(file_path, bucket)

def s3_bucket_client():
    if AWS_ACCESS_KEY_ID == '':
        s3 = boto3.client('s3')
        return s3

    s3 = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )
    return s3

def put_s3(file_path, s3_bucket):
    try:
        file_name = os.path.basename(file_path)
        s3 = s3_bucket_client()
        print(file_path)

        # upload file
        s3.upload_file(file_path, s3_bucket, file_name)
        logging.info('Put-File: {}'.format(file_path))

        # get presigned url
        presigned_url = s3.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': s3_bucket,
                'Key': file_name
            },
            ExpiresIn=3600,
            HttpMethod='GET'
        )

        logging.info('Presigned-URL: {}'.format(presigned_url))
        return presigned_url

    except ClientError as e:
        logging.error(e)
        logging.error('Failed S3 Manipulation: {} {}'.format(file_path, s3_bucket))
        return None
    except Exception as e:
        logging.error(e)
        return None

def gcs_bucket_client(gcs_bucket):
    client = storage.Client()
    bucket = client.get_bucket(gcs_bucket)
    return client, bucket

def put_gcs(file_path, gcs_bucket):
    try:
        file_name = os.path.basename(file_path)
        client, bucket = gcs_bucket_client(gcs_bucket)

        # upload file
        blob = bucket.blob(file_name)
        blob.upload_from_filename(file_path)
        logging.info('Put-File: {}'.format(file_path))

        # get signed url
        signed_url = blob.generate_signed_url(
            version='v4',
            expiration=datetime.timedelta(minutes=60),
            method='GET'
        )

        logging.info('Presigned-URL: {}'.format(signed_url))
        return signed_url

    except exceptions.GoogleCloudError as e:
        logging.error('Failed GCS Manipulation: {} {}'.format(file_path, gcs_bucket))
        logging.error(e)
        return None
    except Exception as e:
        logging.error(e)
        return None
