import argparse
import json
import logging
import os
import sys

import boto3
from botocore.exceptions import ClientError

sts_client = boto3.client("sts")
ssm_client = boto3.client("ssm")
cfn_client = boto3.client("cloudformation")
s3_client = boto3.client("s3", region_name="eu-central-1")
s3 = boto3.resource("s3")

logging.basicConfig(format="[%(asctime)s] %(levelname)s - %(message)s", level=logging.INFO)


def main():
    args = parse_args()
    project_name = args.project_name
    environment = args.environment
    ec2_key_name = args.ec2_key_name

    account_id = sts_client.get_caller_identity()["Account"]
    bucket_name = f"{project_name}-bootstrap-{account_id}-{region}"
    if not create_bucket(bucket_name, project_name):
        logging.error(f"Failed to create or access bucket {bucket_name}")
        sys.exit(1)
    if not tag_bucket(bucket_name, project_name):
        logging.error(f"Failed to tag bucket {bucket_name}")
        sys.exit(1)
    if not put_ssm_parameter(bucket_name, project_name, environment):
        logging.error("Failed to create or update SSM parameter")
        sys.exit(1)
    dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    if not upload_file(
        f"{dir_path}/bootstrap_emr/bootstrap_actions.sh", bucket_name, "bootstrap_actions.sh"
    ):
        logging.error("Failed to upload bootstrap_actions.sh")
        sys.exit(1)

    stack_name = f"{project_name}-{environment}"
    cfn_template_path = f"{dir_path}/cloudformation/{project_name}.yml"
    cfn_params_path = f"{dir_path}/cloudformation/{project_name}-params-{environment}.json"

    if not create_stack(
        stack_name,
        cfn_template_path,
        cfn_params_path,
        ec2_key_name,
        bucket_name,
        project_name,
        environment,
    ):
        logging.error("Failed to create CloudFormation stack")
        sys.exit(1)


def create_bucket(bucket_name, project_name):
    """Create an S3 bucket in a specified region"""
    try:
        s3_client.create_bucket(
            Bucket=bucket_name, CreateBucketConfiguration={"LocationConstraint": region}
        )
        logging.info(f"Bucket {bucket_name} created.")
    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "BucketAlreadyOwnedByYou":
            logging.info(f"Bucket {bucket_name} already exists and is owned by you.")
        else:
            logging.error(e)
            return False
    return True


def tag_bucket(bucket_name, project_name):
    """Apply the common 'Name' tag and value to the bucket"""
    try:
        bucket_tagging = s3.BucketTagging(bucket_name)
        response = bucket_tagging.put(
            Tagging={
                "TagSet": [
                    {"Key": "Name", "Value": f"{project_name} Bootstrap Bucket"},
                ]
            }
        )
        logging.info(f"Bucket {bucket_name} tagged with response: {response}")
    except ClientError as e:
        logging.error(e)
        return False
    return True


def upload_file(file_name, bucket, object_name):
    """Upload a file to an S3 bucket"""
    try:
        s3_client.upload_file(file_name, bucket, object_name)
        logging.info(f"File {file_name} uploaded to bucket {bucket} as object {object_name}")
    except ClientError as e:
        logging.error(e)
        return False
    return True


def put_ssm_parameter(bucket_name, project_name, environment):
    parameter_name = f"/{project_name}/bootstrap_bucket"
    parameter_tags = [
        {"Key": "Environment", "Value": environment.capitalize()},
    ]

    try:
        response = ssm_client.put_parameter(
            Name=parameter_name,
            Description="Bootstrap scripts bucket",
            Value=bucket_name,
            Type="String",
            Tags=parameter_tags,
        )
        logging.info(f"Created parameter {parameter_name} with response: {response}")
    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "ParameterAlreadyExists":
            logging.info(f"Parameter {parameter_name} already exists.")
            response = ssm_client.put_parameter(
                Name=parameter_name, Value=bucket_name, Type="String", Overwrite=True
            )
            logging.info(f"Updated parameter {parameter_name} value with response: {response}")

            response = ssm_client.add_tags_to_resource(
                ResourceType="Parameter", ResourceId=parameter_name, Tags=parameter_tags
            )
            logging.info(f"Updated tags for parameter {parameter_name} with response: {response}")
        else:
            logging.error(e)
            return False
    return True


def create_stack(
    stack_name, cfn_template, cfn_params_path, ec2_key_name, bucket_name, project_name, environment
):
    template_data = _parse_template(cfn_template)
    cfn_params = _parse_parameters(cfn_params_path)
    cfn_params.append({"ParameterKey": "Ec2KeyName", "ParameterValue": ec2_key_name})
    cfn_params.append({"ParameterKey": "BootstrapBucket", "ParameterValue": bucket_name})
    cfn_params.append({"ParameterKey": "ProjectName", "ParameterValue": project_name})
    cfn_params.append(
        {"ParameterKey": "EnvironmentName", "ParameterValue": environment.capitalize()}
    )

    create_stack_params = {
        "StackName": stack_name,
        "TemplateBody": template_data,
        "Parameters": cfn_params,
        "TimeoutInMinutes": 60,
        "Capabilities": [
            "CAPABILITY_NAMED_IAM",
        ],
        "Tags": [
            {"Key": "Project", "Value": project_name.capitalize()},
        ],
    }

    try:
        response = cfn_client.create_stack(**create_stack_params)
        logging.info(f"CloudFormation stack creation initiated with response: {response}")
    except ClientError as e:
        logging.error(e)
        return False
    return True


def _parse_template(template):
    with open(template) as template_file_obj:
        template_data = template_file_obj.read()
    cfn_client.validate_template(TemplateBody=template_data)
    return template_data


def _parse_parameters(parameters):
    with open(parameters) as parameter_file_obj:
        cfn_params = json.load(parameter_file_obj)
    return cfn_params


def parse_args():
    """Parse argument values from command-line"""
    parser = argparse.ArgumentParser(description="Arguments required for script.")
    parser.add_argument("-p", "--project-name", required=True, help="Project name")
    parser.add_argument(
        "-e", "--environment", required=True, choices=["dev", "test", "prod"], help="Environment"
    )
    parser.add_argument("-k", "--ec2-key-name", required=True, help="Name of EC2 Keypair")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    main()
