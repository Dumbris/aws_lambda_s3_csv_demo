"""Main module contains functions for reading and writing data files"""
import os
import boto3
import shutil
from voertuigen.processor import process
import io
import logging

INPUT_FILE = os.path.join("data","Open_Data_RDW.csv")

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def read_file_s3(s3_client, bucket_name, key_name):
    response = s3_client.get_object(Bucket=bucket_name, Key=key_name)
    status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")

    if status == 200:
        logger.info(f"Successful S3 get_object response. Status - {status}")
        return  response.get("Body")
    logger.error(f"Unsuccessful S3 get_object response. Status - {status}")

def read_file_local(file_name):
    with open(file_name) as f:
        return io.StringIO(f.read())

def save_to_s3(csv_buffer, s3_client, bucket, key):
        response = s3_client.put_object(
            Bucket=bucket, Key=key, Body=csv_buffer.getvalue()
        )

        status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")

        if status == 200:
            logger.info(f"Successful S3 put_object response. Status - {status}")
        else:
            logger.error(f"Unsuccessful S3 put_object response. Status - {status}")

def save_to_local(cvs_buffer, filename):
    with open(filename, 'w') as fd:
        cvs_buffer.seek(0)
        shutil.copyfileobj(cvs_buffer, fd)

def run_local():
    content = read_file_local(INPUT_FILE)
    for name, out in process(content):
        save_to_local(out, "data/"+name)

def lambda_handler(event, context):
    s3_client = boto3.client('s3', region_name=os.environ.get('AWS_REGION','us-east-1'))
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    key_name = event['Records'][0]['s3']['object']['key']
    content = read_file_s3(s3_client, bucket_name, key_name)
    for name, out in process(content):
        save_to_s3(out, s3_client, bucket=bucket_name, key="out/"+name)
    return True

if __name__ == "__main__":
    run_local()