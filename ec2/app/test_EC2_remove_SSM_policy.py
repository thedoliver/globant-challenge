import boto3
import unittest
from unittest.mock import patch, MagicMock

# Initialize clients for EC2 and IAM

ec2_client = None

iam_client = None

# Define the SSM policy ARN (adjust as needed)
SSM_POLICY_ARN = "arn:aws:iam::aws:policy/AmazonSSMFullAccess"


def authenticate_aws():
    """Prompt the user for AWS credentials and create a session."""
    print("Please provide your AWS credentials:")
    aws_access_key_id = input("AWS Access Key ID: ")
    aws_secret_access_key = input("AWS Secret Access Key: ")
    aws_region = input("AWS Region (e.g., us-east-1): ")

    # Create a session using the provided credentials
    session = boto3.session.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region,
    )
    return session


def initialize_clients(session):
    """Initialize EC2 and IAM clients using the provided session."""
    global ec2_client, iam_client
    ec2_client = session.client('ec2')
    iam_client = session.client('iam')


def get_instance_profiles():
    """Retrieve all instance profiles and their associated roles."""
    paginator = iam_client.get_paginator('list_instance_profiles')
    profiles = []
    for page in paginator.paginate():
        profiles.extend(page['InstanceProfiles'])
    return profiles


def list_ec2_instances():
    """List all EC2 instances in the specified region."""
    instances = ec2_client.describe_instances()['Reservations']
    for reservation in instances:
        for instance in reservation['Instances']:
            print(f"Instance ID: {instance['InstanceId']}, "
                  f"State: {instance['State']['Name']}")


def check_ec2_ssm_role(role_name):
    """Check if the IAM role has any SSM-related policies."""
    try:
        attached_policies = iam_client.list_attached_role_policies(
            RoleName=role_name
        )['AttachedPolicies']
        print(f"Attached policies for role {role_name}: "
              f"{[policy['PolicyName'] for policy in attached_policies]}")

        for policy in attached_policies:
            # Check for any SSM-related policy
            if "SSM" in policy['PolicyName'] or "AmazonSSM" in policy['PolicyArn']:
                return True
        return False
    except Exception as e:
        print(f"Error retrieving policies for role {role_name}: {e}")
        return False


def detach_ssm_policy_from_role(role_name):
    """Detach all SSM-related policies from the specified IAM role."""
    try:
        attached_policies = iam_client.list_attached_role_policies(
            RoleName=role_name
        )['AttachedPolicies']
        for policy in attached_policies:
            # Dynamically detect and detach any SSM-related policy
            if "SSM" in policy['PolicyName'] or "AmazonSSM" in policy['PolicyArn']:
                iam_client.detach_role_policy(
                    RoleName=role_name,
                    PolicyArn=policy['PolicyArn']
                )
                print(f"Detached policy {policy['PolicyName']} from role: {role_name}")
    except Exception as e:
        print(f"Error detaching policies from role {role_name}: {e}")


def remove_ec2_ssm_roles():
    """Remove all SSM-related policies from roles associated with EC2 instances."""
    print("Retrieving EC2 instances...")
    instances = ec2_client.describe_instances()['Reservations']

    for reservation in instances:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            iam_role = instance.get('IamInstanceProfile')

            if iam_role:
                # Debug: Print the full IAM instance profile details
                print(f"IAM Instance Profile for {instance_id}: {iam_role}")

                profile_arn = iam_role['Arn']
                profile_name = profile_arn.split('/')[-1]
                print(f"Extracted profile name: {profile_name}")

                profiles = get_instance_profiles()

                for profile in profiles:
                    if profile['InstanceProfileName'] == profile_name:
                        for role in profile['Roles']:
                            role_name = role['RoleName']
                            print(f"Found role {role_name} for profile {profile_name}")
                            if check_ec2_ssm_role(role_name):
                                print(f"Instance {instance_id} role {role_name} "
                                      "has an SSM-related policy. Removing it...")
                                detach_ssm_policy_from_role(role_name)
                            else:
                                print(f"Instance {instance_id} role {role_name} "
                                      "does not have any SSM-related policy.")
            else:
                print(f"No IAM Instance Profile found for instance {instance_id}.")


def main():
    """Main function to process EC2 instances."""
    session = authenticate_aws()
    initialize_clients(session)

    print("Listing EC2 instances...")
    list_ec2_instances()

    remove_ec2_ssm_roles()


if __name__ == "__main__":
    main()


class TestEC2SSMPolicy(unittest.TestCase):

    @patch('boto3.client')
    def test_check_ec2_ssm_role(self, mock_boto_client):
        mock_iam_client = MagicMock()
        mock_boto_client.return_value = mock_iam_client

        # Simulate attached policies
        mock_iam_client.list_attached_role_policies.return_value = {
            'AttachedPolicies': [
                {'PolicyName': 'AmazonSSMManagedInstanceCore', 'PolicyArn': 'arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore'},
                {'PolicyName': 'AnotherPolicy', 'PolicyArn': 'arn:aws:iam::aws:policy/AnotherPolicy'}
            ]
        }

        global iam_client
        iam_client = mock_iam_client

        result = check_ec2_ssm_role('TestRole')
        self.assertTrue(result)

    @patch('boto3.client')
    def test_detach_ssm_policy_from_role(self, mock_boto_client):
        mock_iam_client = MagicMock()
        mock_boto_client.return_value = mock_iam_client

        # Simulate attached policies
        mock_iam_client.list_attached_role_policies.return_value = {
            'AttachedPolicies': [
                {'PolicyName': 'AmazonSSMManagedInstanceCore', 'PolicyArn': 'arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore'}
            ]
        }

        global iam_client
        iam_client = mock_iam_client

        detach_ssm_policy_from_role('TestRole')

        mock_iam_client.detach_role_policy.assert_called_once_with(
            RoleName='TestRole',
            PolicyArn='arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore'
        )

if __name__ == '__main__':
    unittest.main()
