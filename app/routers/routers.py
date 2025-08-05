from aiogram import Router

from .main_routers import users

router = Router()

router.include_router(router=users.router)

