import unittest
from unittest.mock import patch, MagicMock
from check_rds_public_access import authenticate_aws, check_and_remove_rds_public_access

class TestCheckAndRemoveRDSPublicAccess(unittest.TestCase):

    @patch('boto3.session.Session')
    def test_authenticate_aws(self, mock_boto_session):
        # Mock the session
        mock_session = MagicMock()
        mock_boto_session.return_value = mock_session

        with patch('builtins.input', side_effect=['fake_key', 'fake_secret', 'us-east-1']), \
             patch('getpass.getpass', return_value='fake_secret'):
            session = authenticate_aws()

        self.assertEqual(session, mock_session)
        mock_boto_session.assert_called_once_with(
            aws_access_key_id='fake_key',
            aws_secret_access_key='fake_secret',
            region_name='us-east-1'
        )

    @patch('boto3.session.Session')
    def test_rds_public_access_removal(self, mock_boto_session):
        # Mock the RDS client and session
        mock_session = MagicMock()
        mock_rds_client = MagicMock()
        mock_boto_session.return_value = mock_session
        mock_session.client.return_value = mock_rds_client

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
        with patch('builtins.input', side_effect=['fake_key', 'fake_secret', 'us-east-1']), \
             patch('getpass.getpass', return_value='fake_secret'):
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
