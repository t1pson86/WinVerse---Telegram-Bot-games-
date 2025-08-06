from aiogram import Router

from .main_routers import users, groups

router = Router()

router.include_router(router=users.router)
router.include_router(router=groups.router)
