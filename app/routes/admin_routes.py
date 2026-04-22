from fastapi import APIRouter
from app.controllers.admin_controller import admin_panel, clear_all_history

router = APIRouter(prefix="/admin")

router.add_api_route("/",          admin_panel,       methods=["GET"])
router.add_api_route("/clear-all", clear_all_history, methods=["POST"])