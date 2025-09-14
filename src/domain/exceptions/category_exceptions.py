class CategoryNotFoundError(Exception):
    """Raised when a category is not found"""
    pass


class CategoryAlreadyExistsError(Exception):
    """Raised when trying to create a category that already exists"""
    pass


class InvalidCategoryError(Exception):
    """Raised when category data is invalid"""
    pass