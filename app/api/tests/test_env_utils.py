import os
import unittest
from unittest.mock import patch
from app.services.env_utils import get_env_variable  # Adjusted import path

class TestEnvUtils(unittest.TestCase):

    @patch.dict(os.environ, {"TEST_ENV_VAR": "value_from_env_file"})
    def test_retrieve_from_env_file(self):
        """
        Test that the function retrieves the value from the .env file.
        """
        value = get_env_variable("TEST_ENV_VAR")
        self.assertEqual(value, "value_from_env_file")

    @patch("app.services.env_utils.secretmanager.SecretManagerServiceClient")
    def test_retrieve_from_google_cloud_secrets(self, mock_secret_client):
        """
        Test that the function retrieves the value from Google Cloud Secrets Manager
        when not found in the .env file.
        """
        # Mock the response from Google Cloud Secret Manager
        mock_secret_client_instance = mock_secret_client.return_value
        mock_access_secret_version = mock_secret_client_instance.access_secret_version
        mock_access_secret_version.return_value.payload.data.decode.return_value = "value_from_google_cloud"

        # Ensure TEST_ENV_VAR is not in the environment
        if "TEST_ENV_VAR" in os.environ:
            del os.environ["TEST_ENV_VAR"]

        # Run the function
        value = get_env_variable("TEST_ENV_VAR")
        
        # Check that the mock was called (i.e., Google Cloud Secret Manager was used)
        mock_access_secret_version.assert_called_once()
        
        # Validate the returned value
        self.assertEqual(value, "value_from_google_cloud")

    @patch("app.services.env_utils.secretmanager.SecretManagerServiceClient")  # Adjusted patch path
    def test_raise_exception_when_secret_not_found(self, mock_secret_client):
        """
        Test that the function raises an exception when the secret is not found
        in both the .env file and Google Cloud Secrets Manager.
        """
        # Ensure TEST_ENV_VAR is not in the environment
        if "TEST_ENV_VAR" in os.environ:
            del os.environ["TEST_ENV_VAR"]

        # Patch Google Cloud Secret Manager to simulate an error
        mock_secret_client_instance = mock_secret_client.return_value
        mock_secret_client_instance.access_secret_version.side_effect = Exception("Secret not found")
            
        with self.assertRaises(Exception) as context:
            get_env_variable("TEST_ENV_VAR")
        
        self.assertIn("Secret not found", str(context.exception))

if __name__ == "__main__":
    unittest.main()
