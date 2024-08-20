import os
from dotenv import load_dotenv
from google.cloud import secretmanager

# Load environment variables from a .env file if it exists
load_dotenv()

def get_env_variable(var_name):
    """
    Retrieves an environment variable from the .env file or Google Cloud Secrets Manager.

    Args:
        var_name (str): The name of the environment variable to retrieve.

    Returns:
        str: The value of the environment variable.
    """
    # Check if the variable is in the .env file or already set in the environment
    value = os.getenv(var_name)
    if value:
        return value
    
    # If not found in .env, fallback to Google Cloud Secrets Manager
    try:
        client = secretmanager.SecretManagerServiceClient()
        project_id = os.getenv("Kai-new-feature")  # Replace with your project ID retrieval method
        secret_name = f"projects/{project_id}/secrets/{var_name}/versions/latest"
        response = client.access_secret_version(name=secret_name)
        value = response.payload.data.decode("UTF-8")
        return value
    except Exception as e:
        raise Exception(f"Error retrieving secret {var_name}: {str(e)}")

    return None
