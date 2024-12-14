# Garden Planner API

## Description
The Garden Planner API is a RESTful web service built with Flask and MySQL, designed to help users manage data related to gardening, including vegetables, pests, soil types, and gardening facts. The API supports JWT authentication and role-based access control for secure and efficient management of gardening data.

## Installation
'''bash
pip install -r requirements.txt

## Configuration
Set the following environment variable:
garden_planner.db: The URL for the database connection.
API Endpoints
Below is a list of the API endpoints available in the system:

## API Endpoints
| **Endpoint**                     | **Method** | **Description**                                   |
|-----------------------------------|------------|---------------------------------------------------|
| `/api/users`                     | GET        | List all users                                   |
| `/api/users`                     | POST       | Create a new user                                |
| `/api/users/{id}`                | GET        | Retrieve a specific user                         |
| `/api/users/{id}`                | PUT        | Update an existing user                          |
| `/api/users/{id}`                | DELETE     | Delete a user                                    |
| `/api/facts`                     | GET        | List all facts                                   |
| `/api/facts`                     | POST       | Create a new fact                                |
| `/api/facts/{id}`                | GET        | Retrieve a specific fact                         |
| `/api/facts/{id}`                | PUT        | Update an existing fact                          |
| `/api/facts/{id}`                | DELETE     | Delete a fact                                    |
| `/api/pests`                     | GET        | List all pests                                   |
| `/api/pests`                     | POST       | Create a new pest                                |
| `/api/pests/{id}`                | GET        | Retrieve a specific pest                         |
| `/api/pests/{id}`                | PUT        | Update an existing pest                          |
| `/api/pests/{id}`                | DELETE     | Delete a pest                                    |
| `/api/soil_types`                | GET        | List all soil types                              |
| `/api/soil_types`                | POST       | Create a new soil type                           |
| `/api/soil_types/{id}`           | GET        | Retrieve a specific soil type                    |
| `/api/soil_types/{id}`           | PUT        | Update an existing soil type                     |
| `/api/soil_types/{id}`           | DELETE     | Delete a soil type                               |
| `/api/vegetables`                | GET        | List all vegetables                              |
| `/api/vegetables`                | POST       | Create a new vegetable                           |
| `/api/vegetables/{id}`           | GET        | Retrieve a specific vegetable                    |
| `/api/vegetables/{id}`           | PUT        | Update an existing vegetable                     |
| `/api/vegetables/{id}`           | DELETE     | Delete a vegetable                               |
| `/api/login`                     | POST       | Login to generate a JWT token                    |


## Testing
Prerequisites:
Install all dependencies using pip install -r requirements.txt.
Ensure that the database is running and the required tables are created.
Set the environment variables like DATABASE_URL for database connectivity.
Steps:
Navigate to the project directory where your test files are located.
Run the tests using pytest:
'''bash
pytest --cov=api.py
Verify the output for successful test execution and check code coverage.


## Git Commit Guidelines
Use conventional commits to maintain clarity and consistency in commit messages:

feat: New features or enhancements.
fix: Bug fixes or minor improvements.
docs: Documentation updates.
test: Adding or updating tests.

Use commit messages:
'''bash
feat: add user authentication
fix: resolve database connection issue
docs: update API documentation
test: add user registration tests
