import pytest
from unittest.mock import Mock
from domain.entities.category import Category
from domain.value_objects.category_id import CategoryId
from domain.exceptions.category_exceptions import CategoryNotFoundError
from application.use_cases.category_read_use_case import CategoryReadUseCase


class TestCategoryReadUseCase:
    
    @pytest.fixture
    def mock_repository(self):
        return Mock()
    
    @pytest.fixture
    def use_case(self, mock_repository):
        return CategoryReadUseCase(mock_repository)
    
    def test_get_category_success_from_repository(self, use_case, mock_repository):
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
    
    def test_get_all_categories_from_repository(self, use_case, mock_repository):
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