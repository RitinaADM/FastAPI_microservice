import pytest
from fastapi.testclient import TestClient
from src.main import app


@pytest.fixture
def client():
    return TestClient(app)


class TestCategoryAPI:
    
    def test_create_category_success(self, client):
        # Arrange
        category_data = {
            "name": "Test Category",
            "description": "Test Description"
        }
        
        # Act
        response = client.post("/categories/", json=category_data)
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == category_data["name"]
        assert data["description"] == category_data["description"]
        assert "id" in data
    
    def test_get_category_success(self, client):
        # Arrange
        # First create a category
        category_data = {
            "name": "Test Category",
            "description": "Test Description"
        }
        create_response = client.post("/categories/", json=category_data)
        created_category = create_response.json()
        
        # Act
        response = client.get(f"/categories/{created_category['id']}")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == created_category["id"]
        assert data["name"] == category_data["name"]
    
    def test_get_all_categories(self, client):
        # Act
        response = client.get("/categories/")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_update_category_success(self, client):
        # Arrange
        # First create a category
        category_data = {
            "name": "Original Name",
            "description": "Original Description"
        }
        create_response = client.post("/categories/", json=category_data)
        created_category = create_response.json()
        
        # Update data
        update_data = {
            "name": "Updated Name",
            "description": "Updated Description"
        }
        
        # Act
        response = client.put(f"/categories/{created_category['id']}", json=update_data)
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == update_data["name"]
        assert data["description"] == update_data["description"]
    
    def test_delete_category_success(self, client):
        # Arrange
        # First create a category
        category_data = {
            "name": "Test Category",
            "description": "Test Description"
        }
        create_response = client.post("/categories/", json=category_data)
        created_category = create_response.json()
        
        # Act
        response = client.delete(f"/categories/{created_category['id']}")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data