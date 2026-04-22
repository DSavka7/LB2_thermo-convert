from fastapi import APIRouter
from app.controllers.converter_controller import (
    index, convert, history_page, clear_history,
    api_convert, api_history, api_clear, ConvertRequest,
)

router = APIRouter()
api_router = APIRouter(prefix="/api")

router.add_api_route("/",               index,         methods=["GET"])
router.add_api_route("/",               convert,       methods=["POST"])
router.add_api_route("/history",        history_page,  methods=["GET"])
router.add_api_route("/history/clear",  clear_history, methods=["POST"])

api_router.add_api_route("/convert", api_convert, methods=["POST"])
api_router.add_api_route("/history", api_history, methods=["GET"])
api_router.add_api_route("/history", api_clear,   methods=["DELETE"])