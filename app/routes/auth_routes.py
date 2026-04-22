from fastapi import APIRouter
from app.controllers.auth_controller import (
    login_page, login_form, register_page, register_form, logout,
    api_register, api_login,
)

router = APIRouter(prefix="/auth")
api_router = APIRouter(prefix="/api")

router.add_api_route("/login",    login_page,    methods=["GET"])
router.add_api_route("/login",    login_form,    methods=["POST"])
router.add_api_route("/register", register_page, methods=["GET"])
router.add_api_route("/register", register_form, methods=["POST"])
router.add_api_route("/logout",   logout,        methods=["GET", "POST"])

api_router.add_api_route("/register", api_register, methods=["POST"])
api_router.add_api_route("/login",    api_login,    methods=["POST"])