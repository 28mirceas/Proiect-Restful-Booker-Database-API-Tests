# Restful Booker – Python & MySQL Database Testing

## Project Overview

This project demonstrates automated testing of Python functions that interact with a MySQL database.

The application contains functions for user management, password verification, authentication token handling, and booking CRUD operations. The tests are written with Pytest and verify function behavior, including database state where applicable.

The project aims to demonstrate:
- Python testing with Pytest
- MySQL database interaction and SQL verification
- CRUD operation testing
- Password hashing and verification
- Authentication and token handling
- A clear and maintainable project structure

## Technologies Used

- Python 3
- Pytest
- MySQL
- `mysql-connector-python`
- `bcrypt`
- SQL
- GitHub Actions (workflow configuration)

## Project Structure

```text
RestfulBooker/
├── .github/
│   └── workflows/
│       └── api_tests.yml
├── db/
│   ├── __init__.py
│   ├── mysql_connector.py
│   ├── booking_db.py
│   └── schema.sql
├── tests/
│   └── test_booking_db.py
├── requirements.txt
└── README.md
```

## Project Features

- User creation
- Password hashing and verification
- User authentication
- Authentication token generation and storage
- Booking creation
- Booking retrieval
- Booking updates
- Booking deletion
- Database-state verification using SQL queries
- Automated tests using Pytest

## Database Structure

The project uses a MySQL database named `booker`, containing the following tables:

- **`users`** — stores user records and password hashes.
- **`tokens`** — stores authentication tokens associated with users.
- **`bookings`** — stores booking details and associates each booking with a user.

The tables use primary keys and foreign-key relationships. The foreign keys from `tokens` and `bookings` to `users` use `ON DELETE CASCADE` and `ON UPDATE CASCADE`.

The database schema is provided in `db/schema.sql`.

### Create the database schema

1. Make sure MySQL Server is installed and running.
2. Open the `db/schema.sql` file in MySQL Workbench, or execute it using a MySQL client.
3. Run the script to create the `booker` database and its tables.

The script creates the database and tables if they do not already exist. It does not insert application or test data, and it does not alter tables that already exist.

## Installation and Configuration

### Prerequisites

- Python 3
- MySQL Server
- Access to a MySQL user that can create and use the `booker` database

### Install Python dependencies

From the project root, run:

```bash
pip install -r requirements.txt
```

### Configure the database connection

Review `db/mysql_connector.py` and configure the connection settings for your local MySQL environment.

Do not commit real passwords or other secrets to GitHub. For a public repository, use environment variables or another appropriate secrets-management approach rather than publishing credentials.

## Test Execution

Run all tests from the project root:

```bash
pytest -v
```

Or run the database test module directly:

```bash
pytest tests/test_booking_db.py -v
```

**Note:** The tests use a MySQL database. Make sure the database schema and connection settings are configured before running them. Some tests may change or delete database records, so review the test code and test data before running the suite against any database containing data you need to keep.

## Continuous Integration

The repository includes a GitHub Actions workflow at:

```text
.github/workflows/api_tests.yml
```

The workflow configuration should be checked to ensure that the GitHub Actions runner starts or connects to a MySQL instance, creates the required schema, configures database credentials securely, and then runs the tests. The workflow should be considered verified only after a successful run in GitHub Actions.

## Test Coverage

The test suite covers the implemented database functions, including:

- User creation
- Password verification
- User login and token handling
- Booking creation
- Booking retrieval
- Booking updates
- Booking deletion

Tests use assertions and, where applicable, SQL queries to check the resulting database state. Refer to `tests/test_booking_db.py` for the exact test cases.

## Author

**QA Tester**
