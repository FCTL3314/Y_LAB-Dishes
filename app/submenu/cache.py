from uuid import UUID

from app.data_processing.cache import clear_menus_with_nested_objects_cache
from app.redis import redis
from app.submenu.constants import SUBMENU_CACHE_TEMPLATE, SUBMENUS_CACHE_TEMPLATE


async def clear_submenu_retrieve_cache(submenu_id: UUID) -> None:
    await redis.unlink(SUBMENU_CACHE_TEMPLATE.format(id=submenu_id))
    await clear_menus_with_nested_objects_cache()


async def clear_submenu_list_cache(menu_id: UUID) -> None:
    await redis.unlink(SUBMENUS_CACHE_TEMPLATE.format(menu_id=menu_id))
    await clear_menus_with_nested_objects_cache()


async def clear_submenu_cache(menu_id: UUID, submenu_id: UUID) -> None:
    await clear_submenu_retrieve_cache(submenu_id)
    await clear_submenu_list_cache(menu_id)
