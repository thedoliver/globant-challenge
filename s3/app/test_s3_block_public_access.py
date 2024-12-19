import unittest
from unittest.mock import patch, MagicMock
from s3_block_public_access import (
    list_s3_buckets,
    check_block_public_access,
    disable_s3_public_access,
    authenticate_aws,
)


class TestS3BlockPublicAccess(unittest.TestCase):
    @patch("boto3.session.Session")
    def test_authenticate_aws(self, mock_session):
        """Test AWS authentication."""
        mock_session.return_value = MagicMock()
        with patch("builtins.input", side_effect=["fake-key", "fake-secret", "us-east-1"]):
            session = authenticate_aws()
            self.assertIsNotNone(session)
            mock_session.assert_called_once_with(
                aws_access_key_id="fake-key",
                aws_secret_access_key="fake-secret",
                region_name="us-east-1",
            )

    @patch("boto3.client")
    def test_list_s3_buckets(self, mock_boto3_client):
        """Test listing all S3 buckets."""
        mock_s3 = MagicMock()
        mock_s3.list_buckets.return_value = {
            "Buckets": [{"Name": "test-bucket-1"}, {"Name": "test-bucket-2"}]
        }
        mock_boto3_client.return_value = mock_s3

        buckets = list_s3_buckets()
        self.assertEqual(buckets, ["test-bucket-1", "test-bucket-2"])
        mock_s3.list_buckets.assert_called_once()

    @patch("boto3.client")
    def test_check_block_public_access(self, mock_boto3_client):
        """Test checking Block Public Access settings."""
        mock_s3 = MagicMock()
        mock_s3.get_public_access_block.return_value = {
            "PublicAccessBlockConfiguration": {
                "BlockPublicAcls": True,
                "IgnorePublicAcls": True,
                "BlockPublicPolicy": True,
                "RestrictPublicBuckets": True,
            }
        }
        mock_boto3_client.return_value = mock_s3

        settings = check_block_public_access("test-bucket")
        self.assertEqual(
            settings,
            {
                "BlockPublicAcls": True,
                "IgnorePublicAcls": True,
                "BlockPublicPolicy": True,
                "RestrictPublicBuckets": True,
            },
        )
        mock_s3.get_public_access_block.assert_called_once_with(Bucket="test-bucket")

    @patch("boto3.client")
    def test_disable_s3_public_access(self, mock_boto3_client):
        """Test disabling public access for a bucket."""
        mock_s3 = MagicMock()
        mock_boto3_client.return_value = mock_s3

        with patch("s3_block_public_access.check_block_public_access") as mock_check_block:
            mock_check_block.return_value = {
                "BlockPublicAcls": False,
                "IgnorePublicAcls": False,
                "BlockPublicPolicy": False,
                "RestrictPublicBuckets": False,
            }

            disable_s3_public_access("test-bucket")
            mock_s3.put_public_access_block.assert_called_once_with(
                Bucket="test-bucket",
                PublicAccessBlockConfiguration={
                    "BlockPublicAcls": False,
                    "IgnorePublicAcls": False,
                    "BlockPublicPolicy": False,
                    "RestrictPublicBuckets": False,
                },
            )
            mock_check_block.assert_called_once_with("test-bucket")


if __name__ == "__main__":
    unittest.main()
