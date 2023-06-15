from aiogram import types, Router, Bot, F
from db import BotDateBase
from config import *
from aiogram.filters import Text
from keypad import methods_pay, startmarkup, check_admin
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from payment import CryptoBot, CryptoCloud
from aiogram.utils.keyboard import InlineKeyboardBuilder


router = Router()


class Add_Balance(StatesGroup):
    choosing_method_pay = State()
    choosing_summ_pay = State()
    checking_bill = State()
    create_bill = State()


@router.callback_query(F.data == "add_balance")
async def add_balance_call(callback: types.CallbackQuery, bot_db: BotDateBase, bot: Bot, state: FSMContext):
    await callback.message.edit_text(text="Выберите способ пополнения: ", reply_markup=methods_pay.as_markup(), inline_message_id=callback.message.message_id)
    await callback.answer()

    await state.set_state(Add_Balance.choosing_method_pay)


@router.callback_query(F.data == "CryptoBot", Add_Balance.choosing_method_pay)
async def add_crypto_bot_payment(callback: types.CallbackQuery, bot_db: BotDateBase, bot: Bot, state: FSMContext):
    await state.update_data(choosing_method=callback.data)
    await callback.message.edit_text(text="Отправьте сумму пополнения: (в долларах)", inline_message_id=callback.message.message_id)
    await state.set_state(Add_Balance.choosing_summ_pay)
    await callback.answer()


@router.callback_query(F.data == "crypto_cloud", Add_Balance.choosing_method_pay)
async def add_crypto_cloud_payment(callback: types.CallbackQuery, bot_db: BotDateBase, bot: Bot, state: FSMContext):
    await state.update_data(choosing_method=callback.data)
    await callback.message.edit_text(text="Отправьте сумму пополнения: (в долларах)", inline_message_id=callback.message.message_id)
    await state.set_state(Add_Balance.choosing_summ_pay)
    await callback.answer()


@router.message(Add_Balance.choosing_summ_pay, F.text)
async def create_bill(message: types.Message, state: FSMContext):
    user_method = await state.get_data()
    if message.text.isdigit():
        if user_method["choosing_method"] == "CryptoBot":
            object_pay = CryptoBot(message.text)
            url_pay = object_pay.create_bill("USDT")
        elif user_method["choosing_method"] == "crypto_cloud":
            object_pay = CryptoCloud(message.text)
            url_pay = object_pay.create_bill()
        await state.update_data(object_pay=object_pay, summ=message.text)
        payend = InlineKeyboardBuilder()
        payend.add(types.InlineKeyboardButton(
            text="💵Оплатить💵", url=url_pay))
        payend.add(types.InlineKeyboardButton(
            text="💳Оплатил💳", callback_data="check"))
        payend.add(types.InlineKeyboardButton(
            text="❌Отмена❌", callback_data="tovar_ot"))
        await message.answer(f'  👉 Метод оплаты: {user_method["choosing_method"]} \n👉 К оплате: {message.text}$\n 👉СТРОГО ЖМЁМ 💵ОПЛАТИЛ💵 НЕ ПЕРЕХОДЯ В ДРУГИЕ РАЗДЕЛЫ ИНАЧЕ БАЛАНС НЕ БУДЕТ НАЧИСЛЕН НА ВАШ СЧЁТ\n',
                             reply_markup=payend.as_markup())
        await state.set_state(Add_Balance.create_bill)

    else:
        await message.reply("Введите только цифры")


@router.callback_query(Add_Balance.create_bill, F.data == "tovar_ot")
async def cancel_payment(callback: types.CallbackQuery, bot_db: BotDateBase, bot: Bot, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer("Вы вернулись в меню", reply_markup=check_admin(callback.message.from_user.id))
    await callback.answer()
    await state.clear()


@router.callback_query(Add_Balance.create_bill, F.data == "check")
async def check_bill(callback: types.CallbackQuery, bot_db: BotDateBase, bot: Bot, state: FSMContext):
    user_data = await state.get_data()
    user_method = user_data["choosing_method"]
    object_pay = user_data["object_pay"]
    if object_pay.check_bill() == "paid":
        t1=bot_db.get_balance(callback.from_user.id)[0]
        t2=int(user_data["summ"])
        new_bal = t1+t2
        bot_db.new_balance(new_bal, callback.from_user.id)
        bot_db.add_balance_history(
            callback.from_user.id, user_data["summ"], user_method, object_pay.get_invoice_id())
        user_invite_id = bot_db.check_invite_id(callback.from_user.id)
        if user_invite_id:
            ref_balance = bot_db.get_ref_balance(
                user_invite_id)+user_data["summ"]*0.05
            bot_db.proc_ref_balance(ref_balance, user_invite_id)
        await callback.message.answer(f"Баланс успешно пополнен, ваш новый баланс {new_bal} ", reply_markup=startmarkup)
        await state.clear()
    else:
        await callback.message.answer(f"Средства не поступили на счет ", reply_markup=startmarkup)

    await callback.answer()


@router.callback_query(F.data == "histor_balance")
async def history_balance_call(callback: types.CallbackQuery, bot_db: BotDateBase, bot: Bot, state: FSMContext):
    l = bot_db.get_histor_balance(callback.from_user.id)
    await callback.message.edit_text(text=f"Всего у вас пополнений: {len(l)}")
    if len(l) < 1:
        await callback.answer()
        return
    list_out_balance = [l[i:i + 2] for i in range(0, len(l), 2)]
    row_number = 0
    string = ""
    for value in list_out_balance[row_number]:
        string += f"{'➖'*12}\n💸Метод пополнения : {value[1]}\n💰Cумма: {value[2]}$\n⏳Время пополнения: {value[3]} \n{'➖'*12}\n"
    await callback.message.edit_text(f"{string}", reply_markup=get_keyboard([0, len(list_out_balance)-1]))
    await state.update_data(li=list_out_balance)
    await state.update_data(row_number=row_number)
    await callback.answer()


async def show_history(callback: types.CallbackQuery, new_value: int, li):
    string = ""
    for elem in li[new_value]:
        string += f"{'➖'*12}\n💸Метод пополнения : {elem[1]}\n💰Cумма: {elem[2]}$\n⏳Время пополнения: {elem[3]} \n{'➖'*12}\n"

    await callback.message.edit_text(f"{string}", reply_markup=get_keyboard([new_value, len(li)-1]))
    await callback.answer()


@router.callback_query(Text(startswith="num_"))
async def callbacks_num(callback: types.CallbackQuery, state: FSMContext, bot: Bot, bot_db: BotDateBase):
    user_data = await state.get_data()
    action = callback.data.split("_")[1]
    li = user_data["li"]
    row_number = user_data["row_number"]
    if action == "right" and row_number < len(li)-1:
        row_number += 1
        await state.update_data(row_number=row_number)
        await show_history(callback, row_number, li)
    elif action == "left" and row_number > 0:
        row_number -= 1
        await state.update_data(row_number=row_number)
        await show_history(callback, row_number, li)
    elif action == "finish":
        await callback.message.edit_text("🙌")
        await callback.answer()
        await state.clear()
    else:
        await callback.message.edit_text("Больше записей нет")
        await callback.answer()
        await state.clear()


def get_keyboard(state: FSMContext = None):
    buttons = [
        [],
        [types.InlineKeyboardButton(
            text="Закрыть", callback_data="num_finish")]
    ]
    if state and state[0] != 0:
        buttons[0].append(types.InlineKeyboardButton(
            text="<", callback_data="num_left"))
    if state and state[1] != state[0]:
        buttons[0].append(types.InlineKeyboardButton(
            text=">", callback_data="num_right"))

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
