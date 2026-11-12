# Microservice User Service

A Python Flask REST API microservice for managing user accounts in CS361

## Purpose

The User Service handles user account creation, retrieval, and updates. It communicates with a MySQL database and provides JSON responses to other application components.

## Environment Configuration

The User Service uses environment variables to configure its MySQL database connection and service-to-service authentication.

### Setup

1. Clone the repository and install the Python dependencies from `requirements.txt`.
2. Create a local `.env` file using `.env.example` as a template.
3. Configure the MySQL connection variables for your local database.
4. Generate a unique service API key.
5. Configure the calling application to use the same API key.
6. Start the User Service.

### Creating the environment file

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Edit `.env` and replace the placeholder values with your local configuration.

### Generating a service API key

Run:

```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

Copy the generated value into `SERVICE_API_KEY` in the User Service's `.env` file.

The calling application's backend must be configured with the same key to make authenticated requests.

**Never include the API key in client-side JavaScript or HTML.**

### Security

The `.env` file contains sensitive information and must not be committed to version control.

Only `.env.example`, which contains placeholder values, should be committed.

For deployed applications, configure secrets using the deployment environment's secret-management system rather than storing production credentials in the repository.

## Planned Features

- Create new user accounts
- Retrieve user information by user ID
- Update existing user profiles
- Validate user information
- Securely store password hashes
- Authenticate users

## Technology Stack

- Python
- Flask
- MySQL
- REST API / JSON

## Development Status

In development. Initial API implementation and database integration are pending.
