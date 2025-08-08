from aiogram import Router

from .main_routers import users, groups, welcome, dice_game

router = Router()

router.include_router(router=users.router)
router.include_router(router=groups.router)
router.include_router(router=welcome.router)
router.include_router(router=dice_game.router)

