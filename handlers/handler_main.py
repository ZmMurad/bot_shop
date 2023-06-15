import logging
from aiogram import types, Router, Bot, F
from db import BotDateBase
from aiogram.filters.command import Command
from config import *
from filters.filter_main import Admin_Filter
from keypad import admin_menu, startmarkup

logging.basicConfig(level=logging.INFO)
# Объект бота


router = Router()


@router.message(Command("start"), Admin_Filter())
async def cmd_start_admin(message: types.Message, bot_db: BotDateBase, bot: Bot):
    await message.answer(f"Приветсвтвую вас, {message.from_user.first_name}, о великий Админ", reply_markup=admin_menu)
    if not bot_db.user_exists(message.from_user.id):
        bot_db.add_user(message.from_user.id, message.from_user.id)
# Диспетчер


@router.message(Command("start"))
async def cmd_start(message: types.Message, bot_db: BotDateBase, bot: Bot):
    await message.answer(f"Приветсвтвую вас, {message.from_user.first_name}", reply_markup=startmarkup)
    if not bot_db.user_exists(message.from_user.id):
        if message.text[7:] == "":
            invite_id = None
        else:
            invite_id = message.text[7:]
            if invite_id == message.from_user.id:
                await message.answer("Нельзя регистрироваться по своей ссылке")
                bot_db.add_user(message.from_user.id, message.from_user.id)
                return
            try:
                await bot.send_message(invite_id, "<b>По вашей ссылке зарегистрировался пользователь</b>")
            except:
                for admin in admin_id:
                    await bot.send_message(admin, f"ошибка реферальной ссылки, {message.text}")
        bot_db.add_user(message.from_user.id, message.from_user.id, invite_id)
