from typing import Union, Dict, Any
from config import *
from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery


class Admin_Filter(BaseFilter):
    async def __call__(self,  message: Message) -> Union[bool, Dict[str, Any]]:
        if message.from_user.id in admin_id:
            return True

