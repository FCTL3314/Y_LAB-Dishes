from app.menu.services import MENU_NOT_FOUND_MESSAGE
from app.models import Submenu, Menu
from app.services import BaseCRUDService
from app.utils import get_first_or_404

SUBMENU_NOT_FOUND_MESSAGE = "submenu not found"


class SubmenuService(BaseCRUDService):
    @staticmethod
    def retrieve(menu_id, submenu_id, session):
        return get_first_or_404(
            Submenu.select_by_id(menu_id, submenu_id),
            session,
            SUBMENU_NOT_FOUND_MESSAGE,
        )

    @staticmethod
    def list(menu_id, session):
        return session.exec(Submenu.select_all(menu_id)).all()

    @staticmethod
    def create(menu_id, submenu, session):
        menu = get_first_or_404(
            Menu.select_by_id(menu_id),
            session,
            MENU_NOT_FOUND_MESSAGE,
        )
        menu.submenus.append(submenu)
        session.add(submenu)
        session.commit()
        session.refresh(submenu)
        return submenu

    @staticmethod
    def update(menu_id, submenu_id, updated_submenu, session):
        submenu = get_first_or_404(
            Submenu.select_by_id(menu_id, submenu_id),
            session,
            SUBMENU_NOT_FOUND_MESSAGE,
        )
        updated_submenu_dict = updated_submenu.dict(exclude_unset=True)
        for key, val in updated_submenu_dict.items():
            setattr(submenu, key, val)
        session.add(submenu)
        session.commit()
        session.refresh(submenu)
        return submenu

    @staticmethod
    def delete(menu_id, submenu_id, session):
        submenu = get_first_or_404(
            Submenu.select_by_id(menu_id, submenu_id),
            session,
            SUBMENU_NOT_FOUND_MESSAGE,
        )
        session.delete(submenu)
        session.commit()
        return {"status": True, "message": "The submenu has been deleted"}