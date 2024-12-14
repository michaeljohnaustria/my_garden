# Garden Planner API

## Description
Garden Planner is a web application to help gardeners manage their gardens. It allows users to store and access information about vegetables, soil types, pests, and gardening facts. Key features include managing planting and harvesting times, pest remedies, and soil recommendations. The app also offers secure authentication with role-based access, making it a useful tool for both beginner and experienced gardeners.

## Installation
 ```cmd
pip install -r requirements.txt
```

## Configuration
Set the following environment variable:
```
DATABASE_URL: The connection string to your MySQL database (e.g., mysql://user:password@localhost/garden_planner).
SECRET_KEY: A secret key for JWT encoding and decoding.
```

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
To test the app, run:
 ```cmd
pip install pytest
pytest my_test.py
```

## Git Commit Guidelines
Use commit messages:
```
feat: add user authentication
fix: resolve database connection issue
docs: update API documentation
test: add user registration tests
