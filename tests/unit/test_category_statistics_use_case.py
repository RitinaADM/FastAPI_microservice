import pytest
from unittest.mock import Mock
from domain.entities.category import Category
from domain.value_objects.category_id import CategoryId
from application.use_cases.category_statistics_use_case import CategoryStatisticsUseCase


class TestCategoryStatisticsUseCase:
    
    @pytest.fixture
    def mock_read_use_case(self):
        return Mock()
    
    @pytest.fixture
    def use_case(self, mock_read_use_case):
        return CategoryStatisticsUseCase(mock_read_use_case)
    
    def test_get_category_statistics(self, use_case, mock_read_use_case):
        # Arrange
        categories = [
            Category(id=CategoryId.new(), name="Electronics", description="Electronic devices"),
            Category(id=CategoryId.new(), name="Books", description="Books and literature"),
            Category(id=CategoryId.new(), name="Clothing", description="Clothing and accessories")
        ]
        mock_read_use_case.get_all_categories.return_value = categories
        
        # Act
        result = use_case.get_category_statistics()
        
        # Assert
        assert isinstance(result, dict)
        assert "total_count" in result
        assert "average_name_length" in result
        assert "longest_name" in result
        assert "shortest_name" in result
        assert result["total_count"] == 3
        assert result["longest_name"] == "Electronics"
        assert result["shortest_name"] == "Books"
        
        # Verify that get_all_categories was called
        mock_read_use_case.get_all_categories.assert_called_once()