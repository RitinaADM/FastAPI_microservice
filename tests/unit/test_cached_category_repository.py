import pytest
from unittest.mock import Mock, MagicMock
from domain.entities.category import Category
from domain.value_objects.category_id import CategoryId
from infrastructure.adapters.outbound.cache.cached_category_repository import CachedCategoryRepository


class TestCachedCategoryRepository:
    """Unit tests for CachedCategoryRepository"""
    
    @pytest.fixture
    def mock_repository(self):
        return Mock()
    
    @pytest.fixture
    def mock_cache_adapter(self):
        return Mock()
    
    @pytest.fixture
    def cached_repository(self, mock_repository, mock_cache_adapter):
        return CachedCategoryRepository(mock_repository, mock_cache_adapter)
    
    def test_find_by_id_returns_cached_category(self, cached_repository, mock_cache_adapter, mock_repository):
        """Test that find_by_id returns category from cache when available"""
        # Arrange
        category_id = CategoryId("test-id")
        cached_data = {
            'id': 'test-id',
            'name': 'Test Category',
            'description': 'Test Description'
        }
        mock_cache_adapter.get.return_value = cached_data
        
        # Act
        result = cached_repository.find_by_id(category_id)
        
        # Assert
        mock_cache_adapter.get.assert_called_once_with("category_test-id")
        mock_repository.find_by_id.assert_not_called()
        assert isinstance(result, Category)
        assert result.id == category_id
        assert result.name == "Test Category"
        assert result.description == "Test Description"
    
    def test_find_by_id_returns_repository_category_when_not_cached(self, cached_repository, mock_cache_adapter, mock_repository):
        """Test that find_by_id returns category from repository when not in cache"""
        # Arrange
        category_id = CategoryId("test-id")
        mock_cache_adapter.get.return_value = None
        category = Category(id=category_id, name="Test Category", description="Test Description")
        mock_repository.find_by_id.return_value = category
        
        # Act
        result = cached_repository.find_by_id(category_id)
        
        # Assert
        mock_cache_adapter.get.assert_called_once_with("category_test-id")
        mock_repository.find_by_id.assert_called_once_with(category_id)
        assert result == category
    
    def test_find_by_id_returns_none_when_not_found(self, cached_repository, mock_cache_adapter, mock_repository):
        """Test that find_by_id returns None when category not found"""
        # Arrange
        category_id = CategoryId("test-id")
        mock_cache_adapter.get.return_value = None
        mock_repository.find_by_id.return_value = None
        
        # Act
        result = cached_repository.find_by_id(category_id)
        
        # Assert
        assert result is None
    
    def test_find_all_returns_cached_categories(self, cached_repository, mock_cache_adapter, mock_repository):
        """Test that find_all returns categories from cache when available"""
        # Arrange
        cached_data = [
            {
                'id': 'test-id-1',
                'name': 'Test Category 1',
                'description': 'Test Description 1'
            },
            {
                'id': 'test-id-2',
                'name': 'Test Category 2',
                'description': 'Test Description 2'
            }
        ]
        mock_cache_adapter.get.return_value = cached_data
        
        # Act
        result = cached_repository.find_all()
        
        # Assert
        mock_cache_adapter.get.assert_called_once_with("all_categories")
        mock_repository.find_all.assert_not_called()
        assert len(result) == 2
        assert all(isinstance(cat, Category) for cat in result)
    
    def test_find_all_returns_repository_categories_when_not_cached(self, cached_repository, mock_cache_adapter, mock_repository):
        """Test that find_all returns categories from repository when not in cache"""
        # Arrange
        mock_cache_adapter.get.return_value = None
        categories = [
            Category(id=CategoryId("test-id-1"), name="Test Category 1", description="Test Description 1"),
            Category(id=CategoryId("test-id-2"), name="Test Category 2", description="Test Description 2")
        ]
        mock_repository.find_all.return_value = categories
        
        # Act
        result = cached_repository.find_all()
        
        # Assert
        mock_cache_adapter.get.assert_called_once_with("all_categories")
        mock_repository.find_all.assert_called_once()
        assert result == categories
    
    def test_create_invalidates_all_categories_cache(self, cached_repository, mock_cache_adapter, mock_repository):
        """Test that create invalidates all categories cache"""
        # Arrange
        category = Category(id=None, name="Test Category", description="Test Description")
        saved_category = Category(id=CategoryId("test-id"), name="Test Category", description="Test Description")
        mock_repository.create.return_value = saved_category
        
        # Act
        result = cached_repository.create(category)
        
        # Assert
        mock_repository.create.assert_called_once_with(category)
        mock_cache_adapter.delete.assert_called_once_with("all_categories")
        assert result == saved_category
    
    def test_update_invalidates_caches(self, cached_repository, mock_cache_adapter, mock_repository):
        """Test that update invalidates both specific category and all categories caches"""
        # Arrange
        category_id = CategoryId("test-id")
        category = Category(id=category_id, name="Updated Category", description="Updated Description")
        updated_category = Category(id=category_id, name="Updated Category", description="Updated Description")
        mock_repository.update.return_value = updated_category
        
        # Act
        result = cached_repository.update(category)
        
        # Assert
        mock_repository.update.assert_called_once_with(category)
        assert mock_cache_adapter.delete.call_count == 2
        mock_cache_adapter.delete.assert_any_call("category_test-id")
        mock_cache_adapter.delete.assert_any_call("all_categories")
        assert result == updated_category
    
    def test_delete_invalidates_caches(self, cached_repository, mock_cache_adapter, mock_repository):
        """Test that delete invalidates both specific category and all categories caches"""
        # Arrange
        category_id = CategoryId("test-id")
        mock_repository.delete.return_value = True
        
        # Act
        result = cached_repository.delete(category_id)
        
        # Assert
        mock_repository.delete.assert_called_once_with(category_id)
        assert mock_cache_adapter.delete.call_count == 2
        mock_cache_adapter.delete.assert_any_call("category_test-id")
        mock_cache_adapter.delete.assert_any_call("all_categories")
        assert result is True