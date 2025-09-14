from domain.entities.category import Category
from application.dtos.category_dto import CategoryDTO
from infrastructure.adapters.inbound.rest.schemas.category_schemas import CategoryResponse


def category_to_dto(category: Category) -> CategoryDTO:
    """Map Category entity to CategoryDTO"""
    return CategoryDTO(
        id=category.id,
        name=category.name,
        description=category.description
    )


def dto_to_category(dto: CategoryDTO) -> Category:
    """Map CategoryDTO to Category entity"""
    return Category(
        id=dto.id,
        name=dto.name,
        description=dto.description
    )


def category_to_response(category: Category) -> CategoryResponse:
    """Map Category entity to CategoryResponse"""
    return CategoryResponse(
        id=str(category.id) if category.id else "",
        name=category.name,
        description=category.description
    )