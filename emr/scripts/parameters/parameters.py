#!/usr/bin/env python3


import boto3
ssm_client = boto3.client('ssm')

def get_parameters():
    """Load parameter values from AWS Systems Manager (SSM) Parameter Store"""
    params = {
        'airflow_bucket': ssm_client.get_parameter(Name='/anwb-emr-member-score/airflow_bucket')['Parameter']['Value'],
        'bootstrap_bucket': ssm_client.get_parameter(Name='/anwb-emr-member-score/bootstrap_bucket')['Parameter']['Value'],
        'bronze_bucket': ssm_client.get_parameter(Name='/anwb-emr-member-score/bronze_bucket')['Parameter']['Value'],
        'cluster_id': ssm_client.get_parameter(Name='/anwb-emr-member-score/cluster_id')['Parameter']['Value'],
        'ec2_key_name': ssm_client.get_parameter(Name='/anwb-emr-member-score/ec2_key_name')['Parameter']['Value'],
        'ec2_subnet_id': ssm_client.get_parameter(Name='/anwb-emr-member-score/ec2_subnet_id')['Parameter']['Value'],
        'emr_ec2_role': ssm_client.get_parameter(Name='/anwb-emr-member-score/emr_ec2_role')['Parameter']['Value'],
        'emr_role': ssm_client.get_parameter(Name='/anwb-emr-member-score/emr_role')['Parameter']['Value'],
        'glue_db_bucket': ssm_client.get_parameter(Name='/anwb-emr-member-score/glue_db_bucket')['Parameter']['Value'],
        'gold_bucket': ssm_client.get_parameter(Name='/anwb-emr-member-score/gold_bucket')['Parameter']['Value'],
        'logs_bucket': ssm_client.get_parameter(Name='/anwb-emr-member-score/logs_bucket')['Parameter']['Value'],
        'master_public_dns': ssm_client.get_parameter(Name='/anwb-emr-member-score/master_public_dns')['Parameter']['Value'],
        'silver_bucket': ssm_client.get_parameter(Name='/anwb-emr-member-score/silver_bucket')['Parameter']['Value'],
        'sm_log_group_arn': ssm_client.get_parameter(Name='/anwb-emr-member-score/sm_log_group_arn')['Parameter']['Value'],
        'sm_role_arn': ssm_client.get_parameter(Name='/anwb-emr-member-score/sm_role_arn')['Parameter']['Value'],
        'vpc_id': ssm_client.get_parameter(Name='/anwb-emr-member-score/vpc_id')['Parameter']['Value'],
        'work_bucket': ssm_client.get_parameter(Name='/anwb-emr-member-score/work_bucket')['Parameter']['Value']
    }
    return params
