from sqlalchemy.ext.asyncio import AsyncSession

from app.data_processing.services.admin.updating_services import BaseAdminService


class AdminService:

    def __init__(self, updating_services: list[BaseAdminService]):
        self.services = updating_services

    async def handle(self, session: AsyncSession):
        for updating_service in self.services:
            await updating_service.update(session)
