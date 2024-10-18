import logging
import os
import argparse

import boto3
from botocore.exceptions import ClientError

logging.basicConfig(format="[%(asctime)s] %(levelname)s - %(message)s", level=logging.INFO)

s3_client = boto3.client("s3")
ssm_client = boto3.client("ssm")


def main():
    args = parse_args()
    project_name = args.project_name
    params = get_parameters(project_name)

    # upload files
    dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    path = f"{dir_path}/raw_data/"
    bucket_name = params["bronze_bucket"]
    upload_directory(path, bucket_name)


def upload_directory(path, bucket_name):
    """Uploads a directory of raw Parquet files to Amazon S3"""

    for root, dirs, files in os.walk(path):
        for file in files:
            try:
                if file.endswith(".parquet") and file not in ["_placeholder", ".DS_Store"]:
                    file_directory = os.path.basename(os.path.dirname(os.path.join(root, file)))
                    key = f"{file_directory}/{file}"
                    s3_client.upload_file(os.path.join(root, file), bucket_name, key)
                    print(f"File '{key}' uploaded to bucket '{bucket_name}' as key '{key}'")
            except ClientError as e:
                logging.error(e)


def get_parameters(project_name):
    """Load parameter values from AWS Systems Manager (SSM) Parameter Store"""

    params = {
        "bronze_bucket": ssm_client.get_parameter(Name=f"/{project_name}/bronze_bucket")[
            "Parameter"
        ]["Value"],
    }

    return params


def parse_args():
    """Parse argument values from command-line"""
    parser = argparse.ArgumentParser(description="Upload Parquet files to S3.")
    parser.add_argument("-p", "--project-name", required=True, help="Project name")
    return parser.parse_args()


if __name__ == "__main__":
    main()
