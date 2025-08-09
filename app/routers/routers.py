from aiogram import Router

from .main_routers import parties, users, groups, welcome, games

router = Router()

router.include_router(router=users.router)
router.include_router(router=groups.router)
router.include_router(router=welcome.router)
router.include_router(router=parties.router)
router.include_router(router=games.router)

