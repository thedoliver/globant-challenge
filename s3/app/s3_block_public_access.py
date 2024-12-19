import boto3
import getpass

def authenticate_aws():
    """Prompt the user for AWS credentials and create a session."""
    print("Please provide your AWS credentials:")
    aws_access_key_id = input("AWS Access Key ID: ")
    aws_secret_access_key = getpass.getpass("AWS Secret Access Key: ")
    aws_region = input("AWS Region (e.g., us-east-1): ")

    # Create a session using the provided credentials
    session = boto3.session.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region,
    )
    return session


def list_s3_buckets(session):
    """List all S3 buckets."""
    s3 = session.client('s3')
    try:
        response = s3.list_buckets()
        print("Raw bucket response:", response)  # Debugging
        print("Response type:", type(response))  # Debugging
        return [bucket['Name'] for bucket in response['Buckets']]
    except Exception as e:
        print(f"Error listing buckets: {e}")
        return []


def check_block_public_access(session, bucket_name):
    """Check Block Public Access settings for a specific bucket."""
    s3 = session.client('s3')
    try:
        response = s3.get_public_access_block(Bucket=bucket_name)
        block_settings = response['PublicAccessBlockConfiguration']
        print(f"Block Public Access settings for bucket '{bucket_name}':")
        print(f"  BlockPublicAcls: {block_settings['BlockPublicAcls']}")
        print(f"  IgnorePublicAcls: {block_settings['IgnorePublicAcls']}")
        print(f"  BlockPublicPolicy: {block_settings['BlockPublicPolicy']}")
        print(f"  RestrictPublicBuckets: {block_settings['RestrictPublicBuckets']}")
        return block_settings
    except Exception as e:
        print(f"Error checking bucket '{bucket_name}': {e}")
        return None


def disable_s3_public_access(session, bucket_name):
    """
    Disable public access for a specific S3 bucket
    by enabling Block Public Access settings.
    """
    s3 = session.client('s3')
    try:
        print(f"Disabling public access for bucket: {bucket_name}")
        s3.put_public_access_block(
            Bucket=bucket_name,
            PublicAccessBlockConfiguration={
                'BlockPublicAcls': False,
                'IgnorePublicAcls': False,
                'BlockPublicPolicy': False,
                'RestrictPublicBuckets': False,
            },
        )
        print(f"Public access disabled for bucket '{bucket_name}'.")
        print("Updated Block Public Access settings:")
        check_block_public_access(session, bucket_name)
    except Exception as e:
        print(f"Error disabling public access for bucket '{bucket_name}': {e}")


if __name__ == "__main__":
    # Authenticate AWS session
    session = authenticate_aws()

    # List all buckets
    buckets = list_s3_buckets(session)

    if buckets:
        print("Buckets found:")
        for bucket in buckets:
            print(f"- {bucket}")

        print("\nChecking Block Public Access settings for each bucket:\n")
        for bucket in buckets:
            settings = check_block_public_access(session, bucket)
            print("Settings:", settings)  # Debugging all setting should return all True or all False
            print("Type:", type(settings))  # Debugging
            print("-" * 40)

            # Disable public access if any Block Public Access setting is True
            if settings is not None and any(settings.values()): #Lambda Integraded function
                print(
                    f"Public access detected for bucket '{bucket}'. "
                    f"Disabling public access..."
                )
                disable_s3_public_access(session, bucket)
                print("-" * 40)
            else:
                print(f"Bucket '{bucket}' already has public access disabled.")
    else:
        print("No buckets found.")
