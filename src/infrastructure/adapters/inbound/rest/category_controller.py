from fastapi import APIRouter, HTTPException
from domain.value_objects.category_id import CategoryId
from domain.exceptions.category_exceptions import CategoryNotFoundError, InvalidCategoryError
from infrastructure.adapters.inbound.rest.schemas.category_schemas import (
    CategoryCreateRequest,
    CategoryUpdateRequest,
    CategoryResponse
)
from application.use_cases.category_use_case import CategoryUseCase
from typing import List
from dishka.integrations.fastapi import FromDishka, inject


router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("/", response_model=List[CategoryResponse])
@inject
async def get_all_categories(
    use_case: FromDishka[CategoryUseCase]
):
    categories = use_case.get_all_categories()
    return [
        CategoryResponse(
            id=str(category.id),
            name=category.name,
            description=category.description
        )
        for category in categories
    ]


@router.post("/", response_model=CategoryResponse)
@inject
async def create_category(
    request: CategoryCreateRequest,
    use_case: FromDishka[CategoryUseCase]
):
    try:
        category = use_case.create_category(request.name, request.description)
        return CategoryResponse(
            id=str(category.id),
            name=category.name,
            description=category.description
        )
    except InvalidCategoryError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{category_id}", response_model=CategoryResponse)
@inject
async def get_category(
    category_id: str,
    use_case: FromDishka[CategoryUseCase]
):
    try:
        category = use_case.get_category(CategoryId(category_id))
        return CategoryResponse(
            id=str(category.id),
            name=category.name,
            description=category.description
        )
    except CategoryNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{category_id}", response_model=CategoryResponse)
@inject
async def update_category(
    category_id: str,
    request: CategoryUpdateRequest,
    use_case: FromDishka[CategoryUseCase]
):
    try:
        category = use_case.update_category(
            CategoryId(category_id),
            request.name,
            request.description
        )
        return CategoryResponse(
            id=str(category.id),
            name=category.name,
            description=category.description
        )
    except CategoryNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except InvalidCategoryError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{category_id}")
@inject
async def delete_category(
    category_id: str,
    use_case: FromDishka[CategoryUseCase]
):
    try:
        result = use_case.delete_category(CategoryId(category_id))
        if result:
            return {"message": "Category deleted successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to delete category")
    except CategoryNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))