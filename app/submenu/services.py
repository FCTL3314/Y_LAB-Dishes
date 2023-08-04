from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.common.services import AbstractCRUDService
from app.menu.repository import MenuRepository
from app.menu.services import MENU_NOT_FOUND_MESSAGE, CachedMenuService
from app.models import Submenu
from app.redis import get_cached_data_or_set_new, redis
from app.submenu.constants import (
    SUBMENU_CACHE_TEMPLATE,
    SUBMENUS_CACHE_KEY,
    SUBMENUS_CACHE_TIME,
)
from app.submenu.schemas import SubmenuResponse
from app.utils import is_obj_exists_or_404

SUBMENU_NOT_FOUND_MESSAGE = 'submenu not found'


class SubmenuService(AbstractCRUDService):
    async def retrieve(
        self, menu_id: UUID, submenu_id: UUID, session: AsyncSession
    ) -> SubmenuResponse:
        submenu = await self.repository.get(menu_id, submenu_id, session)
        is_obj_exists_or_404(submenu, SUBMENU_NOT_FOUND_MESSAGE)
        return submenu

    async def list(
        self, menu_id: UUID, session: AsyncSession
    ) -> list[SubmenuResponse]:
        return await self.repository.all(menu_id, session)

    async def create(
        self, menu_id: UUID, submenu: Submenu, session: AsyncSession
    ) -> SubmenuResponse:
        menu = await MenuRepository.get_by_id(menu_id, session, orm_object=True)
        is_obj_exists_or_404(menu, MENU_NOT_FOUND_MESSAGE)
        return await self.repository.create(menu, submenu, session)

    async def update(
        self,
        menu_id: UUID,
        submenu_id: UUID,
        updated_submenu: Submenu,
        session: AsyncSession,
    ) -> SubmenuResponse:
        submenu = await self.repository.get_by_id(
            menu_id, submenu_id, session, orm_object=True
        )
        is_obj_exists_or_404(submenu, SUBMENU_NOT_FOUND_MESSAGE)
        return await self.repository.update(submenu, updated_submenu, session)

    async def delete(
        self, menu_id: UUID, submenu_id: UUID, session: AsyncSession
    ) -> dict:
        submenu = await self.repository.get_by_id(
            menu_id, submenu_id, session, orm_object=True
        )
        is_obj_exists_or_404(submenu, SUBMENU_NOT_FOUND_MESSAGE)
        return await self.repository.delete(submenu, session)


class CachedSubmenuService(SubmenuService):
    async def retrieve(
        self, menu_id: UUID, submenu_id: UUID, session: AsyncSession
    ) -> SubmenuResponse:
        submenu = await get_cached_data_or_set_new(
            key=SUBMENU_CACHE_TEMPLATE.format(id=submenu_id),
            callback=lambda: super(CachedSubmenuService, self).retrieve(
                menu_id, submenu_id, session
            ),
            expiration=SUBMENUS_CACHE_TIME,
        )
        return submenu

    async def list(
        self, menu_id: UUID, session: AsyncSession
    ) -> list[SubmenuResponse]:
        submenus = await get_cached_data_or_set_new(
            key=SUBMENUS_CACHE_KEY,
            callback=lambda: super(CachedSubmenuService, self).list(menu_id, session),
            expiration=SUBMENUS_CACHE_TIME,
        )
        return submenus

    async def create(
        self, menu_id: UUID, submenu: Submenu, session: AsyncSession
    ) -> SubmenuResponse:
        _submenu = await super().create(
            menu_id, submenu, session
        )
        await CachedSubmenuService.clear_list_cache()
        await CachedMenuService.clear_all_cache(menu_id)
        return _submenu

    async def update(
        self,
        menu_id: UUID,
        submenu_id: UUID,
        updated_submenu: Submenu,
        session: AsyncSession,
    ) -> SubmenuResponse:
        _updated_submenu = await super().update(
            menu_id, submenu_id, updated_submenu, session
        )
        await CachedSubmenuService.clear_all_cache(submenu_id)
        return _updated_submenu

    async def delete(
        self, menu_id: UUID, submenu_id: UUID, session: AsyncSession
    ) -> dict:
        response = await super().delete(
            menu_id, submenu_id, session
        )
        await CachedSubmenuService.clear_all_cache(submenu_id)
        await CachedMenuService.clear_all_cache(menu_id)
        return response

    @staticmethod
    async def clear_retrieve_cache(submenu_id: UUID) -> None:
        await redis.delete(SUBMENU_CACHE_TEMPLATE.format(id=submenu_id))

    @staticmethod
    async def clear_list_cache() -> None:
        await redis.delete(SUBMENUS_CACHE_KEY)

    @classmethod
    async def clear_all_cache(cls, submenu_id: UUID) -> None:
        await cls.clear_retrieve_cache(submenu_id)
        await cls.clear_list_cache()
