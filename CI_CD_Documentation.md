---
title: "[]{#_y4svjxfciiws .anchor}CI/CD Part 1 Documentation "
---

# Overview {#overview .unnumbered}

# This document outlines the procedures and best practices for managing environment variables in our project. The system is designed to securely handle sensitive information, streamline configuration processes, and support both local development and production environments. {#this-document-outlines-the-procedures-and-best-practices-for-managing-environment-variables-in-our-project.-the-system-is-designed-to-securely-handle-sensitive-information-streamline-configuration-processes-and-support-both-local-development-and-production-environments. .unnumbered}

# Table of Content {#table-of-content .unnumbered}

'''

# Setting Up and Using the .env File During Local Development {#setting-up-and-using-the-.env-file-during-local-development .unnumbered}

## Purpose of the .env file

> The .env file is used during local development to configure
> environment variables. This allows developers to customize their local
> environment without affecting the production settings.

## Creating the .env fine

### Location:

> the .env file should be placed in the root directory of the project.

### Content format: 

> the .env file contains key-value pairs, each line representing an
> environment variable.
>
> ENV_TYPE=dev
>
> GOOGLE_API_KEY=Your-google-key
>
> PROJECT_ID=you-project-id

### Keep the .env file private: 

> Ensure it is listed in your '.gitignore' file.

## Using the .env file

> The utility function (refer to later explanation) automatically loads
> the environment variables from the .env file if it exists. No
> additional configuration is needed to use these variables in your
> local environment.

# Adding and Updating Secrets in Google Cloud Secrets Manager {#adding-and-updating-secrets-in-google-cloud-secrets-manager .unnumbered}

## Purpose of Google Cloud Secrets Manager

> Google Cloud Secrets Manager is used to securely store and manage
> sensitive environment variables for production. This ensures the
> secrets are not exposed in your codebase or version control.

## Adding a New Secret

### Access Secrets Manager:

i.  Navigate to the Google Cloud Console and go to **Security \> Secrets
    Manager.**

### Create a New Secret:

ii. Click on **Create Secret**.

iii. Name the Secret: Use a descriptive name, such as GOOGLE_API_KEY and
     PROJECT_ID.

iv. Enter the Secret Value: Paste the value of the environment variable

v.  Click Create: save the secret.

# Using Utility Function to Manage Environment Variables {#using-utility-function-to-manage-environment-variables .unnumbered}

## Purpose of the Utility Function

> The utility function 'get_env_varible' is designed to streamline the
> process of retrieving environment variables from both the .env file
> (for local development) and Google Cloud Secrets Manager (for
> production).
>
> This function attempts to retrieve environment variables in a secure
> and reliable manner. It first attempts to retrieve the environment
> variable from a local .env file. If the variable is not found there,
> the function then tries to retrieve it from Google Cloud Secret
> Manager.

### How the Utility Function Works

### **Function Signature:** 

> def get_env_variable(var_name):

### **Parameters:** 'var_name'('str'): 

> the name of the environment variable to retrieve. This is the key used
> to look up the variable in the .env file or in Google Cloud Secret
> Manager.

### **Return Value**: 

> 'str', the value of the requested environment variable.

### **Exceptions:**

i.  **ValueError**: Raised in the following scenarios: The environment
    variable is not found in Google Cloud Secret Manager; Data
    corruption is detected when verifying the checksum of the secret
    retrieved from Google Cloud Secret Manager.

ii. **RuntimeError**: Raised if: Google Cloud credentials are not
    configured properly; Any other unexpected error occurs during the
    retrieval process.

## Detailed Description of the Function

### Loading Environment Variable from '.env' file

> The function starts by loading environment variables from a .env file
> if it exists. This is done using the load_dotenv and find_dotenv
> functions from the python-dotenv library:
>
> load_dotenv(find_dotenv())
>
> After loading the .env file, the function attempts to retrieve the
> requested environment variable using Python\'s built-in os.getenv:
>
> value = os.getenv(var_name)
>
> If the variable is found, the function logs the success and returns
> the value:
>
> logger.debug(f\"Successfully retrieved the environment variable
> \'{var_name}\' from .env file\")
>
> return value

### Retrieving Environment Variables from Google Cloud Secret Manager 

> If the variable is not found in the .env file, the function attempts
> to retrieve it from Google Cloud Secret Manager

#### **Initialize the Secret Manager Client:**  {#initialize-the-secret-manager-client .unnumbered}

> The function initializes the Google Cloud Secret Manager client to
> interact with Google Cloud:\
> \
> client = secretmanager.SecretManagerServiceClient()

#### **Build the Secret Name:**  {#build-the-secret-name .unnumbered}

> The secret\'s name is constructed using the format
> secrets/{var_name}/versions/latest:\
> \
> secret_name = f\"secrets/{var_name}/versions/latest\"

#### **Access the Secret:**  {#access-the-secret .unnumbered}

> The secret is accessed using the access_secret_version method:
>
> response = client.access_secret_version(name=secret_name)

#### **Verify Payload Checksum:** {#verify-payload-checksum .unnumbered}

> The function verifies the integrity of the retrieved secret by
> checking its CRC32C checksum:\
> \
> crc32c = google_crc32c.Checksum()
>
> crc32c.update(response.payload.data)
>
> if response.payload.data_crc32c != int(crc32c.hexdigest(), 16):
>
> error_message = \"Data corruption detected: The checksum of the
> retrieved secret does not match.\"
>
> logger.error(error_message)
>
> raise ValueError(error_message)

#### **Decode and Return the Secret:**  {#decode-and-return-the-secret .unnumbered}

> If the checksum is valid, the secret is decoded and returned:
>
> secret_payload = response.payload.data.decode(\'UTF-8\')
>
> logger.debug(f\"Successfully retrieved the environment variable
> \'{var_name}\' from Google Secrets\")
>
> return secret_payload

## Error Handling

> The function includes comprehensive error handling to manage various
> scenarios.

### Secret Not Found: {#secret-not-found .unnumbered}

> If the secret is not found in Google Cloud Secret Manager, a
> ValueError is raised:
>
> except google.api_core.exceptions.NotFound as e:
>
> error_message = f\"Secret \'{var_name}\' not found in Google Cloud
> Secrets Manager: {e}\"
>
> logger.error(error_message)
>
> raise ValueError(error_message)

### Google Cloud Credentials Error: {#google-cloud-credentials-error .unnumbered}

> If the Google Cloud credentials are not configured correctly, a
> RuntimeError is raised:
>
> except google.auth.exceptions.DefaultCredentialsError as e:
>
> error_message = \"Google Cloud credentials are not configured
> properly.\"
>
> logger.error(error_message)
>
> raise RuntimeError(error_message)

### Unexpected Errors: {#unexpected-errors .unnumbered}

> Any other unexpected errors during the process are caught and logged,
> and a RuntimeError is raised:
>
> except Exception as e:
>
> error_message = f\"An unexpected error occurred while retrieving
> \'{var_name}\' from Google Cloud Secrets Manager: {str(e)}\"
>
> logger.error(error_message)
>
> raise RuntimeError(error_message)

## Conclusion:

> The get_env_variable function provides a robust solution for securely
> retrieving environment variables, first from a local .env file and, if
> unavailable, from Google Cloud Secret Manager. It incorporates
> thorough error handling and logging, making it a reliable choice for
> managing sensitive configuration data in various environments. This
> function is well-suited for applications requiring secure and
> consistent access to environment variables across different deployment
> scenarios.

# Testing and Validation for the Utility Function {#testing-and-validation-for-the-utility-function .unnumbered}

## Unit test

a.  **Overview:** The 'TestGetEnvVatiable' class contains unit tests for
    the 'get_env_variable' function from the 'app.services.env_manager'
    module. The function is responsible for retrieving environment
    variables, either from a '.env' file or from Google Cloud's Secret
    Manager if the variable is not found locally.

b.  **Framework:** These tests use the 'unittest' framework along with
    'unittest.mock' to simulate the environment and verify that the
    function behaves correctly in different scenarios.

c.  **Test Methods:**

    i.  'Test_env_variable_from_env_file'： this test verifies that the
        'get_env_variable' function correctly retrieves environment
        variables from a '.env' file.

        1.  'os.getenv' simulates retrieving an environment variable;

        2.  'load_dotenv' simulates loading the '.env' file.

        3.  Assertions are made to verify:

            a.  The '.env' file is loaded

            b.  The environment variable is retrieved using 'os.getenv'

            c.  The returned value from the function is 'test_value'.

    ii. 'test_env_variable \_from_google_secrets': this test checks that
        the 'get_env_variable' function correctly retrieve environment
        variables from Google Cloud's Secret Manager when the variable
        is not found in the '.env' file.

        1.  'os.getenv' simulates retrieving an environment variable,
            returning 'None' as if the variable is not in the '.env'
            file.

        2.  'load_dotenv' simulates loading the '.env' file.

        3.  'SecretManagerServiceClient' Mocks the Google Cloud Secret
            Manager client.

        4.  'google_crc32c.Checksum' Mocks the CRC32C checksum
            verification [to determine if there is a difference between
            the version of an object found at the source and the version
            found at the destination.]{.mark}

        5.  Assertions are made to verify:

            a.  the Google Cloud Secret Manager client is instantiated
                and called correctly;

            b.  The returned value from the function is
                \'secret_value\'.

d.  **[Running the test:]{.mark}**

> **[(? how to run the test, run directly?)]{.mark}**

# Best Practices and Considerations {#best-practices-and-considerations .unnumbered}

## General Best Practices

a.  **Consistency:** Maintain consistency in how environment variables
    are named and accessed across the project.

b.  **Security:** Always store sensitive information in secure locations
    (e.g., Secrets Manager) and avoid hardcoding secrets in your code.

c.  **Documentation:** Keep documentation up-to-date with the latest
    environment variable configurations and usage guidelines.

## Environment-specific Guidelines

d.  **Local Development:**

    i.  Use the .env file to manage environment variables specific to
        your development environment.

    ii. Avoid including production secrets in the .env file.

e.  **Production:**

    i.  Rely on Google Cloud Secrets Manager for managing sensitive
        environment variables.

    ii. Regularly review and update secrets to maintain security.

## Troubleshooting Tips 

f.  **Missing Environment Variables:**

    i.  If an environment variable is not found, check that it is
        correctly defined in the .env file or Google Cloud Secrets
        Manager.

g.  **Access Issues:**

    i.  Ensure that the service account used in the CI/CD pipeline has
        the necessary permissions to access Google Cloud Secrets
        Manager.
