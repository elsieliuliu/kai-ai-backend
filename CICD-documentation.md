# CI/CD Part 1 Documentation

## Overview

This document outlines the procedures and best practices for managing environment variables in our project. The system is designed to securely handle sensitive information, streamline configuration processes, and support both local development and production environments.

## Table of Content

- **Setting Up and Using the .env File During Local Development**
  1. Purpose of the .env file
  2. Creating the .env file
  3. Using the .env file
- **Adding and Updating Secrets in Google Cloud Secrets Manager**
  1. Purpose of Google Cloud Secrets Manager
  2. Adding a New Secret
- **Using Utility Function to Manage Environment Variables**
  1. Purpose of the Utility Function
  2. How the Utility Function Works
- **Best Practices and Considerations**
  1. General Best Practices
  2. Environment-specific Guidelines
  3. Troubleshooting Tips

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