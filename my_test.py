import pytest
from unittest.mock import patch, MagicMock
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

# Mock Database Connection for Tests
@pytest.fixture
def mock_db_connection():
    with patch("app.get_db_connection") as mock_connection:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        yield mock_conn

# Test for Valid Email
def test_is_valid_email():
    assert app.is_valid_email("test@example.com")
    assert not app.is_valid_email("invalid-email")

# Test for Valid Date
def test_is_valid_date():
    assert app.is_valid_date("2024-12-12")
    assert not app.is_valid_date("2024-12-32")

# Test for creating a fact (POST /api/facts)
def test_create_fact(client, mock_db_connection):
    mock_cursor = mock_db_connection.cursor.return_value
    mock_cursor.lastrowid = 1

    # Sample input data
    data = {
        "vegetable_ID": 1,
        "soil_type_ID": 2,
        "best_time_to_sow": "2024-01-01",
        "best_time_to_harvest": "2024-12-01"
    }

    response = client.post("/api/facts", json=data)
    
    assert response.status_code == 201
    assert response.json['success'] is True
    assert response.json['data']['fact_ID'] == 1

# Test for missing required fields when creating a fact
def test_create_fact_missing_fields(client):
    data = {"vegetable_ID": 1}
    response = client.post("/api/facts", json=data)
    assert response.status_code == 400
    assert response.json['success'] is False
    assert "required" in response.json['error']

# Test for getting a fact (GET /api/facts/{fact_id})
def test_get_fact(client, mock_db_connection):
    mock_cursor = mock_db_connection.cursor.return_value
    mock_cursor.fetchone.return_value = {
        "fact_ID": 1,
        "vegetable_ID": 1,
        "soil_type_ID": 2,
        "best_time_to_sow": "2024-01-01",
        "best_time_to_harvest": "2024-12-01"
    }
    
    response = client.get("/api/facts/1")
    assert response.status_code == 200
    assert response.json['success'] is True
    assert response.json['data']['fact_ID'] == 1

# Test for updating a fact (PUT /api/facts/{fact_id})
def test_update_fact(client, mock_db_connection):
    mock_cursor = mock_db_connection.cursor.return_value
    mock_cursor.rowcount = 1  # Simulate update success

    data = {
        "vegetable_ID": 2,
        "soil_type_ID": 3,
        "best_time_to_sow": "2024-02-01",
        "best_time_to_harvest": "2024-11-01"
    }

    response = client.put("/api/facts/1", json=data)
    assert response.status_code == 200
    assert response.json['success'] is True
    assert "updated successfully" in response.json['message']

# Test for deleting a fact (DELETE /api/facts/{fact_id})
def test_delete_fact(client, mock_db_connection):
    mock_cursor = mock_db_connection.cursor.return_value
    mock_cursor.rowcount = 1  # Simulate delete success

    response = client.delete("/api/facts/1")
    assert response.status_code == 200
    assert response.json['success'] is True
    assert "deleted" in response.json['message']

# Test for token required decorator
def test_token_required(client):
    response = client.get("/api/facts")
    assert response.status_code == 401
    assert "Token is missing" in response.json['error']

# Test for role-based access control
def test_requires_role(client):
    # Simulate a valid token with 'admin' role
    headers = {'Authorization': 'Bearer valid_token_with_admin_role'}
    response = client.get("/api/facts", headers=headers)
    assert response.status_code == 200

    # Simulate a user with invalid role
    headers = {'Authorization': 'Bearer valid_token_with_user_role'}
    response = client.get("/api/facts", headers=headers)
    assert response.status_code == 403
    assert "Access denied" in response.json['error']
    
# Test for successful login (POST /api/login)
def test_login_success(client):
    # Sample login data
    data = {"username": "mich", "password": "pass"}
    
    # Send POST request to login endpoint
    response = client.post("/api/login", json=data)
    
    assert response.status_code == 200
    assert response.json['success'] is True
    assert 'token' in response.json  # Ensure token is returned

# Test for invalid login (POST /api/login)
def test_login_invalid_credentials(client):
    # Invalid login data
    data = {"username": "invalid_user", "password": "wrong_pass"}
    
    # Send POST request to login endpoint
    response = client.post("/api/login", json=data)
    
    assert response.status_code == 401  # Unauthorized
    assert response.json['success'] is False
    assert response.json['error'] == "Invalid credentials!"  # Ensure error message is correct

# Test for missing username (POST /api/login)
def test_login_missing_username(client):
    # Missing username in login data
    data = {"password": "pass"}
    
    # Send POST request to login endpoint
    response = client.post("/api/login", json=data)
    
    assert response.status_code == 400  # Bad Request
    assert response.json['success'] is False
    assert 'username' in response.json['error']  # Ensure missing username is handled

# Test for missing password (POST /api/login)
def test_login_missing_password(client):
    # Missing password in login data
    data = {"username": "mich"}
    
    # Send POST request to login endpoint
    response = client.post("/api/login", json=data)
    
    assert response.status_code == 400  # Bad Request
    assert response.json['success'] is False
    assert 'password' in response.json['error']  # Ensure missing password is handled

    
if __name__ == "__main__":
    pytest.main()