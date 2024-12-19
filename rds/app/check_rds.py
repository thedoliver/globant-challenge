import boto3
import getpass

def authenticate_aws():
    """Prompt the user for AWS credentials and create a session securely."""
    print("Please provide your AWS credentials:")
    aws_access_key_id = input("AWS Access Key ID: ").strip()
    aws_secret_access_key = getpass.getpass("AWS Secret Access Key: ").strip()  # Hide input for sensitive information
    aws_region = input("AWS Region (e.g., us-east-1): ").strip()

    try:
        # Create a session using the provided credentials
        session = boto3.session.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=aws_region,
        )
        print(f"Authenticated successfully in region: {aws_region}")
        return session
    except Exception as e:
        print(f"Error authenticating AWS session: {e}")
        return None

def check_and_remove_rds_public_access():
    # Authenticate AWS session
    session = authenticate_aws()
    if not session:
        print("AWS authentication failed. Exiting.")
        return

    # Create an RDS client from the authenticated session
    rds_client = session.client('rds')

    try:
        # Retrieve all RDS instances
        response = rds_client.describe_db_instances()
        db_instances = response['DBInstances']

        for db_instance in db_instances:
            instance_id = db_instance['DBInstanceIdentifier']
            publicly_accessible = db_instance['PubliclyAccessible']

            print(f"Checking RDS instance: {instance_id}")
            
            if publicly_accessible:
                print(f"Instance {instance_id} is publicly accessible. Removing public access...")

                # Modify the RDS instance to disable public access
                rds_client.modify_db_instance(
                    DBInstanceIdentifier=instance_id,
                    PubliclyAccessible=False,
                    ApplyImmediately=True
                )

                print(f"Public access removed for RDS instance: {instance_id}")
            else:
                print(f"Instance {instance_id} is not publicly accessible. No changes needed.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_and_remove_rds_public_access()
