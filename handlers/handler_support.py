from aiogram import types, Router, Bot, F
from db import BotDateBase
from config import *
from aiogram.filters import Text
from aiogram.utils.keyboard import InlineKeyboardBuilder


router = Router()


@router.message(Text("Поддержка"))
async def support_call(message: types.Message, bot_db: BotDateBase, bot: Bot):
    sup_button = InlineKeyboardBuilder()
    sup_button.add(types.InlineKeyboardButton(
        text=f"Написать админу", url=f"https://t.me/{support_name}"))
    await message.answer(f"По всем вопросам писать {support_name}", reply_markup=sup_button.as_markup())
