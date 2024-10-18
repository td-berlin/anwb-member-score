#!/usr/bin/env python3

# Purpose: Create Step Function state machine
# Author:  Gary A. Stafford (November 2020)
# Usage Example: python3 ./create_state_machine.py \
#                   --definition-file step_function_emr_analyze.json \
#                   --state-machine EMR-Demo-Analysis \
#                   --project-name my_project_name

import argparse
import logging
import os

import boto3
from botocore.exceptions import ClientError

logging.basicConfig(format="[%(asctime)s] %(levelname)s - %(message)s", level=logging.INFO)

step_functions_client = boto3.client("stepfunctions")
ssm_client = boto3.client("ssm")


def main():
    args = parse_args()
    params = get_parameters(args.project_name)

    dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    definition_file = open(f"{dir_path}/step_functions/definitions/{args.definition_file}", "r")
    definition = definition_file.read()

    create_state_machine(
        definition,
        args.state_machine,
        params["sm_log_group_arn"],
        params["sm_role_arn"],
        args.project_name,
    )


def create_state_machine(definition, sm_name, sm_log_group_arn, sm_role_arn, project_name):
    """Creates the AWS Step Functions state machine"""

    try:
        response = step_functions_client.create_state_machine(
            name=sm_name,
            definition=definition,
            roleArn=sm_role_arn,
            type="STANDARD",
            loggingConfiguration={
                "level": "ERROR",
                "includeExecutionData": False,
                "destinations": [
                    {"cloudWatchLogsLogGroup": {"logGroupArn": sm_log_group_arn}},
                ],
            },
            tags=[
                {"key": "Project", "value": project_name},
            ],
        )
        print(f"Response: {response}")
    except ClientError as e:
        logging.error(e)
        return False
    return True


def parse_args():
    """Parse argument values from command-line"""

    parser = argparse.ArgumentParser(description="Arguments required for script.")
    parser.add_argument("-d", "--definition-file", required=True, help="Name of definition file")
    parser.add_argument(
        "-s", "--state-machine", required=True, help="Name of state machine to create"
    )
    parser.add_argument("-p", "--project-name", required=True, help="Name of the project")
    args = parser.parse_args()
    return args


def get_parameters(project_name):
    """Load parameter values from AWS Systems Manager (SSM) Parameter Store"""

    params = {
        "sm_role_arn": ssm_client.get_parameter(Name=f"/{project_name}/sm_role_arn")["Parameter"][
            "Value"
        ],
        "sm_log_group_arn": ssm_client.get_parameter(Name=f"/{project_name}/sm_log_group_arn")[
            "Parameter"
        ]["Value"],
    }

    return params


if __name__ == "__main__":
    main()
