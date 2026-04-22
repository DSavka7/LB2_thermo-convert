from .converter_controller import index, convert, history_page, clear_history
from .auth_controller import login_page, login_form, register_page, register_form, logout
from .admin_controller import admin_panel, clear_all_history

__all__ = [
    "index", "convert", "history_page", "clear_history",
    "login_page", "login_form", "register_page", "register_form", "logout",
    "admin_panel", "clear_all_history",
]