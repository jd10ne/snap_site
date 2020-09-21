import logging
import os

import boto3
from botocore.exceptions import ClientError


def bucket_client():
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY']
    )
    return s3



def put_s3(file_path, s3_bucket):
    try:
        file_name = os.path.basename(file_path)
        s3 = bucket_client()
        print(file_path)
        s3.upload_file(file_path, s3_bucket, file_name)
        logging.info('Put-File: {}'.format(file_path))

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
