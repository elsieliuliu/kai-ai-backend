# CI/CD Part 1 Documentation

## Overview

This document outlines the procedures and best practices for managing environment variables in our project. The system is designed to securely handle sensitive information, streamline configuration processes, and support both local development and production environments.

## Table of Content

## Setting Up and Using the .env File During Local Development

### Purpose of the .env file

The `.env` file is used during local development to configure environment variables. This allows developers to customize their local environment without affecting the production settings.

### Creating the .env file

- **Location**: The `.env` file should be placed in the root directory of the project.
- **Content format**: The `.env` file contains key-value pairs, with each line representing an environment variable.

```plaintext
ENV_TYPE=dev
GOOGLE_API_KEY=Your-google-key
PROJECT_ID=your-project-id
```
### Keep the `.env` file private

Ensure it is listed in your `.gitignore` file.

### Using the `.env` file

The utility function (refer to later explanation) automatically loads the environment variables from the `.env` file if it exists. No additional configuration is needed to use these variables in your local environment.

## Adding and Updating Secrets in Google Cloud Secrets Manager

### Purpose of Google Cloud Secrets Manager

Google Cloud Secrets Manager is used to securely store and manage sensitive environment variables for production. This ensures the secrets are not exposed in your codebase or version control.

### Adding a New Secret

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

### Purpose of the Utility Function

The utility function `get_env_varible` is designed to streamline the process of retrieving environment variables from both the `.env` file (for local development) and Google Cloud Secrets Manager (for production).

This function attempts to retrieve environment variables in a secure and reliable manner. It first attempts to retrieve the environment variable from a local `.env` file. If the variable is not found there, the function then tries to retrieve it from Google Cloud Secret Manager.
