# Garden Planner API

The Garden Planner API provides endpoints for managing data related to gardening, including information about vegetables, pests, soil types, and facts related to gardening. The API is built with Flask and MySQL, and supports JWT authentication and role-based access control.

## Features

- **Vegetables**: Manage vegetable data, including name, recommended soil type, and sowing/harvest times.
- **Pests**: Manage pest descriptions and remedies.
- **Soil Types**: Manage different soil types used for gardening.
- **Facts**: Manage gardening facts, associating vegetables with soil types and optimal sowing/harvest times.
- **Authentication**: Secure API with JWT token-based authentication.
- **Role-Based Access Control**: Restrict access to certain routes based on user roles.

## API Endpoints

### General Endpoints

- `GET /api/facts`: Retrieve all facts.
- `GET /api/facts/<fact_id>`: Retrieve a specific fact by ID.
- `POST /api/facts`: Create a new fact.
- `PUT /api/facts/<fact_id>`: Update an existing fact.
- `DELETE /api/facts/<fact_id>`: Delete a fact by ID.

- `GET /api/pests`: Retrieve all pests.
- `GET /api/pests/<pest_id>`: Retrieve a specific pest by ID.
- `POST /api/pests`: Create a new pest.
- `PUT /api/pests/<pest_id>`: Update an existing pest.
- `DELETE /api/pests/<pest_id>`: Delete a pest by ID.

- `GET /api/soil_types`: Retrieve all soil types.
- `GET /api/soil_types/<soil_type_id>`: Retrieve a specific soil type by ID.
- `POST /api/soil_types`: Create a new soil type.
- `PUT /api/soil_types/<soil_type_id>`: Update an existing soil type.
- `DELETE /api/soil_types/<soil_type_id>`: Delete a soil type by ID.

- `GET /api/vegetables`: Retrieve all vegetables.
- `GET /api/vegetables/<vegetable_id>`: Retrieve a specific vegetable by ID.
- `POST /api/vegetables`: Create a new vegetable.
- `PUT /api/vegetables/<vegetable_id>`: Update an existing vegetable.
- `DELETE /api/vegetables/<vegetable_id>`: Delete a vegetable by ID.

### Authentication and Authorization

The API uses JWT (JSON Web Token) for authentication. A valid JWT token must be provided in the `Authorization` header for routes requiring authentication.

#### Token Required Example:
```bash
Authorization: Bearer <your_token>
