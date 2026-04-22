from .converter_routes import router as converter_router, api_router as converter_api_router
from .auth_routes import router as auth_router, api_router as auth_api_router
from .admin_routes import router as admin_router

all_routers = [
    converter_router,
    converter_api_router,
    auth_router,
    auth_api_router,
    admin_router,
]

__all__ = ["all_routers"]