from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.common.services import AbstractCRUDService
from app.menu.constants import MENU_CACHE_TEMPLATE, MENUS_CACHE_KEY, MENUS_CACHE_TIME
from app.menu.schemas import MenuResponse
from app.models import Menu
from app.redis import get_cached_data_or_set_new, redis
from app.utils import is_obj_exists_or_404

MENU_NOT_FOUND_MESSAGE = 'menu not found'


class MenuService(AbstractCRUDService):
    async def retrieve(
        self, menu_id: UUID, session: AsyncSession
    ) -> Menu | MenuResponse:
        menu = await self.repository.get(menu_id, session)
        is_obj_exists_or_404(menu, MENU_NOT_FOUND_MESSAGE)
        return menu

    async def list(
        self, session: AsyncSession
    ) -> list[Menu] | list[MenuResponse]:
        return await self.repository.all(session)

    async def create(
        self, menu: Menu, session: AsyncSession
    ) -> Menu | MenuResponse:
        return await self.repository.create(menu, session)

    async def update(
        self, menu_id: UUID, updated_menu: Menu, session: AsyncSession
    ) -> Menu | MenuResponse:
        menu = await self.repository.get_by_id(menu_id, session, orm_object=True)
        is_obj_exists_or_404(menu, MENU_NOT_FOUND_MESSAGE)
        return await self.repository.update(menu, updated_menu, session)

    async def delete(self, menu_id: UUID, session: AsyncSession) -> dict:
        menu = await self.repository.get_by_id(menu_id, session, orm_object=True)
        is_obj_exists_or_404(menu, MENU_NOT_FOUND_MESSAGE)
        return await self.repository.delete(menu, session)


class CachedMenuService(MenuService):
    async def retrieve(
        self, menu_id: UUID, session: AsyncSession
    ) -> Menu | MenuResponse:
        menu = await get_cached_data_or_set_new(
            key=MENU_CACHE_TEMPLATE.format(id=menu_id),
            callback=lambda: super(CachedMenuService, self).retrieve(menu_id, session),
            expiration=MENUS_CACHE_TIME,
        )
        return menu

    async def list(
        self, session: AsyncSession
    ) -> list[Menu] | list[MenuResponse]:
        menus = await get_cached_data_or_set_new(
            key=MENUS_CACHE_KEY,
            callback=lambda: super(CachedMenuService, self).list(session),
            expiration=MENUS_CACHE_TIME,
        )
        return menus

    async def create(
        self, menu: Menu, session: AsyncSession
    ) -> Menu | MenuResponse:
        menu = await super().create(menu, session)  # type: ignore
        await CachedMenuService.clear_list_cache()
        return menu

    async def update(
        self, menu_id: UUID, updated_menu: Menu, session: AsyncSession
    ) -> Menu | MenuResponse:
        updated_menu = await super().update(menu_id, updated_menu, session)  # type: ignore
        await CachedMenuService.clear_all_cache(menu_id)
        return updated_menu

    async def delete(self, menu_id: UUID, session: AsyncSession) -> dict:
        response = await super().delete(menu_id, session)
        await CachedMenuService.clear_all_cache(menu_id)
        return response

    @staticmethod
    async def clear_retrieve_cache(menu_id: UUID) -> None:
        await redis.delete(MENU_CACHE_TEMPLATE.format(id=menu_id))

    @staticmethod
    async def clear_list_cache() -> None:
        await redis.delete(MENUS_CACHE_KEY)

    @classmethod
    async def clear_all_cache(cls, menu_id: UUID) -> None:
        await cls.clear_retrieve_cache(menu_id)
        await cls.clear_list_cache()
