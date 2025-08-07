from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import UsersModel


router = Router()



