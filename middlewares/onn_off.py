from typing import Callable, Dict, Any, Awaitable
from aiogram import types
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from config import admin_id, chat_id_channel
from keypad import check_sub



class Onn_Off_message(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        # Если сегодня не суббота и не воскресенье,
        # то продолжаем обработку.
        if event.from_user.id in admin_id or data["bot_db"].get_on_off()[0][0]=="on":
            return await handler(event, data)
        # В противном случае просто вернётся None
        # и обработка прекратится
        await event.answer(
            "Бот отключен",
            show_alert=True
        )
        return

# Это будет outer-мидлварь на любые колбэки
class Onn_Off_Callback(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        # Если сегодня не суббота и не воскресенье,
        # то продолжаем обработку.
        if event.from_user.id in admin_id or data["bot_db"].get_on_off()[0][0]=="on":
            return await handler(event, data)
        # В противном случае отвечаем на колбэк самостоятельно
        # и прекращаем дальнейшую обработку
        await event.answer(
            "Бот отключен",
            show_alert=True
        )
        return
    
    
def check_follow(chat_member:types.chat_member_banned.ChatMemberBanned):
    chat_member=chat_member.dict()
    if chat_member["status"]!="left" and chat_member["status"]!="kicked":
        return True
    return False


class Follow_check_message(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        # Если сегодня не суббота и не воскресенье,
        # то продолжаем обработку.
        if check_follow(await data["bot"].get_chat_member(chat_id=chat_id_channel,user_id=event.from_user.id)):
            return await handler(event, data)
        # В противном случае просто вернётся None
        # и обработка прекратится
        await event.answer(
            "Подпишитесь на канал",reply_markup=check_sub.as_markup()
        )
        return

# Это будет outer-мидлварь на любые колбэки
class Follow_Check_Callback(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        # Если сегодня не суббота и не воскресенье,
        # то продолжаем обработку.
        if check_follow(await data["bot"].get_chat_member(chat_id=chat_id_channel,user_id=event.from_user.id)):
            return await handler(event, data)
        # В противном случае отвечаем на колбэк самостоятельно
        # и прекращаем дальнейшую обработку
        await event.message.answer(
            "Подпишитесь на канал",reply_markup=check_sub.as_markup()
            
        )
        await event.answer()
        return