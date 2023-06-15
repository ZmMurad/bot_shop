from aiogram import types, Router, Bot, F
from db import BotDateBase
from config import *
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from keypad import profile_more, money_translation, startmarkup,check_admin
from aiogram.types import BufferedInputFile

router = Router()


@router.message(Text("👨‍💼Профиль"))
async def profile_call(message: types.Message, bot_db: BotDateBase, bot: Bot, state: FSMContext):
    get_balance = bot_db.get_balance(message.from_user.id)
    await message.answer(
        text=f'👨‍💼 Никнеймы: {message.from_user.full_name}\n🔑 Ваш id:  <code>{message.from_user.id}</code>  \n💰 Ваш баланс: {get_balance[0]}$',
        reply_markup=profile_more.as_markup(resize_keyboard=True))
    s=await state.get_state()
    if not str(s)=="Add_Balance:create_bill":

        await state.clear()


@router.callback_query(F.data == "referral_program")
async def get_ref_program(callback: types.CallbackQuery, bot_db: BotDateBase):
    await callback.message.edit_text(text=f"👥Ваша реферальная ссылка:\n <code>https://t.me/{bot_name}/?start={callback.from_user.id}</code>\n\
💰 Заработано на рефералах: {bot_db.get_ref_balance(callback.from_user.id)}$\n\
👨‍💼 Количество рефералов: {bot_db.count_reeferals(callback.from_user.id)}\n\
➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\
💬Вы будете получать на баланс 5% от пополнений ваших рефералов.", reply_markup=money_translation.as_markup())
    await callback.answer()


@router.callback_query(F.data == "tovar_ot")
async def cancel_payment(callback: types.CallbackQuery, bot_db: BotDateBase, bot: Bot, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer("Вы вернулись в меню", reply_markup=check_admin(callback.message.from_user.id))
    await callback.answer()
    await state.clear()


@router.callback_query(F.data=="money_conclusions")
async def add_balance_from_ref_balance(callback: types.CallbackQuery, bot_db: BotDateBase):
    ref_balance=bot_db.get_ref_balance(callback.from_user.id)
    if ref_balance<1:
        await callback.message.answer("На реферальном балансе мало денег", reply_markup=startmarkup)
        await callback.answer()
        return
    user_balance=bot_db.get_balance(callback.from_user.id)[0]
    new_balance=ref_balance+user_balance
    bot_db.new_balance(new_balance,callback.from_user.id)
    await callback.message.answer("Деньги переведены на основной счет", reply_markup=startmarkup)
    await callback.answer()
    
    
@router.callback_query(F.data=="histor_order")
async def history_order_call(callback:types.CallbackQuery,bot_db: BotDateBase, bot: Bot, state:FSMContext):
    l=bot_db.get_histor_order(callback.from_user.id)
    user_data= await state.get_data()
    if user_data.get("delete"):
        await callback.message.answer(text=f"Всего у вас заказов: {len(l)}\n")   
    else:
        await callback.message.edit_text(text=f"Всего у вас заказов: {len(l)}\n")
    if len(l)<1:
        await callback.answer("")
        return
    
    row_number=0
    list_out_balance=[l[i:i + 2] for i in range(0, len(l), 2)]
    string=""
    
    orders_num=[]
    for value in list_out_balance[row_number]:
        orders_num.append(value[0])
        string+=f"{'➖'*12}\n#️⃣Номер заказа {value[0]} Цена : {value[1]}\n⏳Время пополнения:: {value[2]}$\n {'➖'*12}\n"
    await callback.message.answer(f"{string}",reply_markup=get_keyboard([0, len(list_out_balance)-1,orders_num]))
    await state.update_data(li=list_out_balance)
    await state.update_data(row_number=row_number)
    await callback.answer()







def get_keyboard(state:FSMContext=None):
    buttons = [
        [],
        [types.InlineKeyboardButton(text="Закрыть", callback_data="history_finish")],
    ]
    if state and state[0]!=0:
        buttons[0].append(types.InlineKeyboardButton(text="<", callback_data="history_left"))
    if state and state[1]!=state[0]:
        buttons[0].append(types.InlineKeyboardButton(text=">", callback_data="history_right"))
    for order_num in state[2]:
        buttons.insert(-1,[types.InlineKeyboardButton(text=f"#{order_num}", callback_data=f"history_{order_num}")])
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


async def show_history_order(callback: types.CallbackQuery, new_value: int,li):
    string=""
    orders_num=[]
    for elem in li[new_value]:
        orders_num.append(elem[0])
        string+=f"{'➖'*12}\nНомер заказа {elem[0]} Цена : {elem[1]}\n⏳Время пополнения:: {elem[2]}$\n {'➖'*12}\n"
    await callback.message.edit_text(f"{string}", reply_markup=get_keyboard([new_value,len(li)-1,orders_num]))
    await callback.answer()
    
    
@router.callback_query(Text(startswith="history_"))
async def callbacks_num(callback: types.CallbackQuery,state:FSMContext, bot:Bot,bot_db:BotDateBase):
    user_data=await state.get_data()
    action = callback.data.split("_")[1]
    li= user_data["li"]
    row_number=user_data["row_number"]
    if action=="right" and row_number<len(li)-1:
        row_number+=1
        await state.update_data(row_number=row_number)
        await show_history_order(callback, row_number, li)
    elif action=="left" and row_number>0:
        row_number-=1
        await state.update_data(row_number=row_number)
        await show_history_order(callback, row_number, li)
    elif  action=="finish":    
        await callback.message.edit_text("🙌")
        await callback.answer()
        await state.clear()
    else:
        result=bot_db.get_inside_order(action)
        string=f"{'➖'*12}\nКоличество товаров в заказе: {len(result)}"
        total_price=0
        for item in result:
            total_price+=item[4]
            string+=f"\nТовар: {item[3]} {item[2]}| Описание: {item[5]}\nЦена: {item[4]}\n"
        string+=f"\n#️⃣Заказ: {item[0]}\n💸Итоговая сумма: {total_price}\n📅Дата заказа: {item[7]}\n{'➖'*12}\n"
        await callback.message.edit_text(f"{string}",reply_markup=keyboard_history_back())
        await callback.answer()
        await state.update_data(string=string)


@router.callback_query(F.data=="download_order")
async def download_order(callback:types.CallbackQuery,bot_db: BotDateBase, bot: Bot, state:FSMContext):
    user_data=await state.get_data()
    string=user_data["string"]
    file=BufferedInputFile(bytes(string,"utf-8"),filename="file.txt")
    await callback.message.delete()
    await callback.message.answer_document(document=file,reply_markup=keyboard_history_back())
    del file
    await state.update_data(delete=True)
    await callback.answer()

def keyboard_history_back():
    buttons=[
        [types.InlineKeyboardButton(text=" ⬇️Загрузить ⬇️", callback_data="download_order")],
        [types.InlineKeyboardButton(text="🧾История заказов🧾", callback_data="histor_order")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


