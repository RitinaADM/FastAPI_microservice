import pytest
from unittest.mock import Mock, MagicMock
from domain.entities.category import Category
from domain.value_objects.category_id import CategoryId
from domain.exceptions.category_exceptions import CategoryNotFoundError, InvalidCategoryError
from application.use_cases.category_use_case import CategoryUseCase


class TestCategoryUseCase:
    
    @pytest.fixture
    def mock_repository(self):
        return Mock()
    
    @pytest.fixture
    def mock_event_publisher(self):
        return Mock()
    
    @pytest.fixture
    def use_case(self, mock_repository, mock_event_publisher):
        return CategoryUseCase(mock_repository, mock_event_publisher)
    
    def test_create_category_success(self, use_case, mock_repository, mock_event_publisher):
        # Arrange
        name = "Test Category"
        description = "Test Description"
        category_id = CategoryId.new()
        expected_category = Category(id=category_id, name=name, description=description)
        mock_repository.save.return_value = expected_category
        
        # Act
        result = use_case.create_category(name, description)
        
        # Assert
        assert result.name == name
        assert result.description == description
        mock_repository.save.assert_called_once()
        mock_event_publisher.publish_category_created.assert_called_once_with(expected_category)
    
    def test_create_category_invalid_name_raises_exception(self, use_case):
        # Arrange
        invalid_name = ""
        
        # Act & Assert
        with pytest.raises(InvalidCategoryError):
            use_case.create_category(invalid_name)
    
    def test_get_category_success(self, use_case, mock_repository):
        # Arrange
        category_id = CategoryId.new()
        expected_category = Category(id=category_id, name="Test", description="Test")
        mock_repository.find_by_id.return_value = expected_category
        
        # Act
        result = use_case.get_category(category_id)
        
        # Assert
        assert result == expected_category
        mock_repository.find_by_id.assert_called_once_with(category_id)
    
    def test_get_category_not_found_raises_exception(self, use_case, mock_repository):
        # Arrange
        category_id = CategoryId.new()
        mock_repository.find_by_id.return_value = None
        
        # Act & Assert
        with pytest.raises(CategoryNotFoundError):
            use_case.get_category(category_id)
    
    def test_get_all_categories(self, use_case, mock_repository):
        # Arrange
        categories = [
            Category(id=CategoryId.new(), name="Category 1", description="Desc 1"),
            Category(id=CategoryId.new(), name="Category 2", description="Desc 2")
        ]
        mock_repository.find_all.return_value = categories
        
        # Act
        result = use_case.get_all_categories()
        
        # Assert
        assert result == categories
        mock_repository.find_all.assert_called_once()
    
    def test_update_category_success(self, use_case, mock_repository, mock_event_publisher):
        # Arrange
        category_id = CategoryId.new()
        name = "Updated Name"
        description = "Updated Description"
        
        existing_category = Category(id=category_id, name="Old Name", description="Old Desc")
        updated_category = Category(id=category_id, name=name, description=description)
        
        mock_repository.find_by_id.return_value = existing_category
        mock_repository.update.return_value = updated_category
        
        # Act
        result = use_case.update_category(category_id, name, description)
        
        # Assert
        assert result.name == name
        assert result.description == description
        mock_repository.find_by_id.assert_called_once_with(category_id)
        mock_repository.update.assert_called_once()
        mock_event_publisher.publish_category_updated.assert_called_once_with(updated_category)
    
    def test_update_category_not_found_raises_exception(self, use_case, mock_repository):
        # Arrange
        category_id = CategoryId.new()
        mock_repository.find_by_id.return_value = None
        
        # Act & Assert
        with pytest.raises(CategoryNotFoundError):
            use_case.update_category(category_id, "Name", "Desc")
    
    def test_delete_category_success(self, use_case, mock_repository, mock_event_publisher):
        # Arrange
        category_id = CategoryId.new()
        existing_category = Category(id=category_id, name="Test", description="Test")
        mock_repository.find_by_id.return_value = existing_category
        mock_repository.delete.return_value = True
        
        # Act
        result = use_case.delete_category(category_id)
        
        # Assert
        assert result is True
        mock_repository.find_by_id.assert_called_once_with(category_id)
        mock_repository.delete.assert_called_once_with(category_id)
        mock_event_publisher.publish_category_deleted.assert_called_once_with(category_id)
    
    def test_delete_category_not_found_raises_exception(self, use_case, mock_repository):
        # Arrange
        category_id = CategoryId.new()
        mock_repository.find_by_id.return_value = None
        
        # Act & Assert
        with pytest.raises(CategoryNotFoundError):
            use_case.delete_category(category_id)