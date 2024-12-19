import unittest
from unittest.mock import patch, MagicMock
from rds.app.check_rds import check_and_remove_rds_public_access

class TestCheckAndRemoveRDSPublicAccess(unittest.TestCase):

    @patch('boto3.client')
    def test_rds_public_access_removal(self, mock_boto_client):
        # Mock the RDS client and its responses
        mock_rds_client = MagicMock()
        mock_boto_client.return_value = mock_rds_client

        # Mock describe_db_instances response
        mock_rds_client.describe_db_instances.return_value = {
            'DBInstances': [
                {
                    'DBInstanceIdentifier': 'test-instance-1',
                    'PubliclyAccessible': True
                },
                {
                    'DBInstanceIdentifier': 'test-instance-2',
                    'PubliclyAccessible': False
                }
            ]
        }

        # Call the function
        check_and_remove_rds_public_access()

        # Verify modify_db_instance was called for the public instance
        mock_rds_client.modify_db_instance.assert_called_once_with(
            DBInstanceIdentifier='test-instance-1',
            PubliclyAccessible=False,
            ApplyImmediately=True
        )

        # Verify describe_db_instances was called
        mock_rds_client.describe_db_instances.assert_called_once()

if __name__ == "__main__":
    unittest.main()
