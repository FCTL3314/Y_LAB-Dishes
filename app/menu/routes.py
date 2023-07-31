from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter

from app.dependencies import ActiveMenuService
from app.menu.services import MenuService
from app.menu.schemas import MenuResponse
from app.models import Menu

router = APIRouter()


@router.get("/{menu_id}/", response_model=MenuResponse)
async def menu_retrieve(menu_id: UUID, menu_service: MenuService = ActiveMenuService):
    response = await menu_service.retrieve(menu_id)
    return response


@router.get("/", response_model=list[MenuResponse])
async def menu_list(menu_service: MenuService = ActiveMenuService):
    response = await menu_service.list()
    return response


@router.post("/", response_model=MenuResponse, status_code=HTTPStatus.CREATED)
async def menu_create(menu: Menu, menu_service: MenuService = ActiveMenuService):
    response = await menu_service.create(menu)
    return response


@router.patch("/{menu_id}/", response_model=MenuResponse)
async def menu_patch(
    menu_id: UUID, updated_menu: Menu, menu_service: MenuService = ActiveMenuService
):
    response = await menu_service.update(menu_id, updated_menu)
    return response


@router.delete("/{menu_id}/")
async def menu_delete(menu_id: UUID, menu_service: MenuService = ActiveMenuService):
    response = await menu_service.delete(menu_id)
    return response
