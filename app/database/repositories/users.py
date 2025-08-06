from typing import Optional

from .base_repository import BaseRepository
from models import UsersModel
from ..db import get_new_async_session

class UsersRepository(BaseRepository[UsersModel]):

    def __init__(self):
        self.session = get_new_async_session()


    async def create(
        self, 
        entity
    ):

        return 'ok'


 
    async def read(
        self, 
        id: int
    ):

        return 'ok'


 
    async def update(
        self, 
        entity
    ):

        return 'ok'



    async def delete(
        self, 
        id: int
    ):

        return 'ok'