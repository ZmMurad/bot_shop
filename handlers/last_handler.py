from aiogram import Router
from aiogram import types
from keypad import check_admin
router=Router()


@router.message()
async def other_message(message: types.Message):
    await message.answer("Я не распознал вашу команду", reply_markup=check_admin)