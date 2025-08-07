from aiogram import Router

from .main_routers import users, groups, welcome, games, play

router = Router()

router.include_router(router=users.router)
router.include_router(router=groups.router)
router.include_router(router=welcome.router)
router.include_router(router=games.router)
router.include_router(router=play.router)
