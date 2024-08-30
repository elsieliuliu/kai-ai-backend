# CI/CD Part 1 Documentation

## Overview

This document outlines the procedures and best practices for managing environment variables in our project. The system is designed to securely handle sensitive information, streamline configuration processes, and support both local development and production environments.

## Table of Content

## Setting Up and Using the .env File During Local Development

### 1. Purpose of the .env file

The `.env` file is used during local development to configure environment variables. This allows developers to customize their local environment without affecting the production settings.

### 2. Creating the .env file

- **Location**: The `.env` file should be placed in the root directory of the project.
- **Content format**: The `.env` file contains key-value pairs, with each line representing an environment variable.

```plaintext
ENV_TYPE=dev
GOOGLE_API_KEY=Your-google-key
PROJECT_ID=your-project-id
```
- **Keep the `.env` file private**: Ensure it is listed in your `.gitignore` file.

### 3. Using the `.env` file

The utility function (refer to later explanation) automatically loads the environment variables from the `.env` file if it exists. No additional configuration is needed to use these variables in your local environment.

## Adding and Updating Secrets in Google Cloud Secrets Manager

### 1. Purpose of Google Cloud Secrets Manager

Google Cloud Secrets Manager is used to securely store and manage sensitive environment variables for production. This ensures the secrets are not exposed in your codebase or version control.

### 2. Adding a New Secret

1. **Access Secrets Manager**:
   - Navigate to the Google Cloud Console and go to `Security > Secrets Manager`.
2. **Create a New Secret**:
   - Click on **Create Secret**.
3. **Name the Secret**:
   - Use a descriptive name, such as `GOOGLE_API_KEY` and `PROJECT_ID`.
4. **Enter the Secret Value**:
   - Paste the value of the environment variable.
5. **Click Create**:
   - Save the secret.

## Using Utility Function to Manage Environment Variables

### 1. Purpose of the Utility Function

The utility function `get_env_varible` is designed to streamline the process of retrieving environment variables from both the `.env` file (for local development) and Google Cloud Secrets Manager (for production).

This function attempts to retrieve environment variables in a secure and reliable manner. It first attempts to retrieve the environment variable from a local `.env` file. If the variable is not found there, the function then tries to retrieve it from Google Cloud Secret Manager.

### 2. How the Utility Function Works

- **Function Signature:**
  ```python
  def get_env_variable(var_name):
  ```
- **Parameters:** `var_name('str')`
  - the name of the environment variable to retrieve. This is the key used to look up the variable in the .env file or in Google Cloud Secret Manager.

- **Return Value:** 
   - ‘str’, the value of the requested environment variable.


- **Exceptions:**
  - **ValueError:** Raised in the following scenarios: The environment variable is not found in Google Cloud Secret Manager; Data corruption is detected when verifying the checksum of the secret retrieved from Google Cloud Secret Manager.
  - **RuntimeError:** Raised if: Google Cloud credentials are not configured properly; Any other unexpected error occurs during the retrieval process.

## Detailed Description of the Function

### 1. Loading Environment Variable from `.env` file

The function starts by loading environment variables from a `.env` file if it exists. This is done using the load_dotenv and find_dotenv functions from the python-dotenv library:

```python
load_dotenv(find_dotenv())
```

After loading the `.env` file, the function attempts to retrieve the requested environment variable using Python's built-in `os.getenv`:

```python
value = os.getenv(var_name)
```

If the variable is found, the function logs the success and returns the value:

```python
logger.debug(f"Successfully retrieved the environment variable '{var_name}' from .env file")
return value
```
