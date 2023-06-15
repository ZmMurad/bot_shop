from aiogram import types, Router, Bot, F
from db import BotDateBase
from config import *
from aiogram.filters import Text
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from filters.filter_main import Admin_Filter
from keypad import admin_menu, product_menu


router = Router()


class Admin_State(StatesGroup):
    send_news = State()
    add_balance=State()
    typing_balance=State()
    munis_balance=State()
    typing_minus_balance=State()
    add_item=State()
    delete_item=State()
    choise_country=State()
    typing_log_pass=State()
    add_item_price=State()


@router.message(Text("📨Рассылка"), Admin_Filter())
async def newstellers(message: types.Message, bot_db: BotDateBase, bot: Bot, state: FSMContext):
    await state.clear()
    cancel_but = types.ReplyKeyboardMarkup(keyboard=[[types.KeyboardButton(text="Отмена")]],resize_keyboard=True)
    await message.answer('Можете отправить просто текст, фото с подписью, просто фото')
    await message.answer('Что отправить всем пользователям?', reply_markup=cancel_but)
    
    await state.set_state(Admin_State.send_news)
    
    
@router.message(Admin_State.send_news, Admin_Filter(), F.text=="Отмена")
async def cancel_news(message: types.Message, state:FSMContext):
    await message.answer("Вы отменили действие", reply_markup=admin_menu)
    await state.clear()
    
@router.message(Text("🕹Вкл\Выкл"), Admin_Filter())
async def on_off(message: types.Message, bot_db: BotDateBase, bot: Bot, state: FSMContext):
    on_off = bot_db.get_on_off()
    if on_off[0][0] == 'on':
        bot_db.change_on_off('off')
        await message.answer(text=f'Бот отключен', reply_markup=admin_menu)
    else:
        bot_db.change_on_off('on')
        await message.answer(text=f'Бот включен', reply_markup=admin_menu)


@router.message(Admin_State.send_news)
async def send_newsletters(message: types.Message, bot_db: BotDateBase, bot: Bot, state: FSMContext):
    await state.clear()
    type_m=message.content_type
    all_users=bot_db.get_user_id()
    if str(type_m)=="ContentType.TEXT":
        for user_row in all_users:
            await bot.send_message(user_row[0],text=message.text)
    elif str(type_m)=="ContentType.PHOTO":
        if message.caption:
            cap=message.caption
        else:
            cap=""
        for user_row in all_users:
            await bot.send_photo(user_row[0],photo=message.photo[-1].file_id,caption=cap)

    
@router.message(Text("➕Пополнить баланс"), Admin_Filter())
async def get_id_user(message: types.Message, bot_db: BotDateBase, bot: Bot, state: FSMContext):
    await state.clear()
    await message.answer("Введи id пользователя", reply_markup=admin_menu)
    await state.set_state(Admin_State.add_balance)
    
@router.message(F.text, Admin_State.add_balance)
async def add_balance(message: types.Message, bot_db: BotDateBase, bot: Bot, state: FSMContext):
    id_add_balance_user=message.text
    if id_add_balance_user.isdigit():
        get_balance=bot_db.get_balance(id_add_balance_user)
        if get_balance:
            await state.update_data(balance=get_balance[0], user_id=message.text)
            await message.answer("Введи сумму пополнения", reply_markup=admin_menu)
            await state.set_state(Admin_State.typing_balance)
        else:
            await message.answer("Пользователь не найдет", reply_markup=admin_menu)
    else:
        await message.answer("Введи только цифры", reply_markup=admin_menu)
        
@router.message(F.text, Admin_State.typing_balance)
async def typing_balance_f(message: types.Message, bot_db: BotDateBase, bot: Bot, state: FSMContext):    
    if message.text.isdigit():
        user_data=await state.get_data()
        new_balance=user_data["balance"]+int(message.text)
        bot_db.new_balance(new_balance,user_data["user_id"])
        await message.answer(f"Баланс успешно обновлен, новый баланс {new_balance}", reply_markup=admin_menu)
        await state.clear()
    else:
        await message.answer(f"Введи только цифры далбаеб", reply_markup= admin_menu)
        
        
@router.message(Text("➖Убавить баланс"), Admin_Filter())
async def get_id_user_for_minus(message: types.Message, bot_db: BotDateBase, bot: Bot, state: FSMContext):
    await state.clear()
    await message.answer("Введи id пользователя", reply_markup=admin_menu)
    await state.set_state(Admin_State.munis_balance)
    
@router.message(F.text, Admin_State.munis_balance)
async def minus_balance(message: types.Message, bot_db: BotDateBase, bot: Bot, state: FSMContext):
    id_add_balance_user=message.text
    if id_add_balance_user.isdigit():
        get_balance=bot_db.get_balance(id_add_balance_user)
        if get_balance:
            await state.update_data(balance=get_balance[0], user_id=message.text)
            await message.answer("Введи сумму убавления", reply_markup=admin_menu)
            await state.set_state(Admin_State.typing_minus_balance)
        else:
            await message.answer("Пользователь не найдет", reply_markup=admin_menu)
    else:
        await message.answer("Введи только цифры", reply_markup=admin_menu)
        
@router.message(F.text, Admin_State.typing_minus_balance)
async def typing_minus_balance_f(message: types.Message, bot_db: BotDateBase, bot: Bot, state: FSMContext):    
    if message.text.isdigit():
        user_data=await state.get_data()
        new_balance=user_data["balance"]-int(message.text)
        bot_db.new_balance(new_balance,user_data["user_id"])
        await message.answer(f"Баланс успешно обновлен, новый баланс {new_balance}", reply_markup=admin_menu)
        await state.clear()
    else:
        await message.answer(f"Введи только цифры далбаеб", reply_markup= admin_menu)


@router.message(Text("🗳Товар"), Admin_Filter())
async def menu_item(message: types.Message, bot_db: BotDateBase, bot: Bot, state: FSMContext):
    await state.clear()
    await message.answer("Меню товаров", reply_markup=product_menu.as_markup())
    
    

@router.callback_query(F.data=="get_product", Admin_Filter())
async def get_all_products(callback:types.CallbackQuery,state:FSMContext, bot_db:BotDateBase):
    await state.clear()
    l = bot_db.get_account_sale()
    if len(l) < 1:
        await callback.answer()
        return
    list_out_balance = [l[i:i + 16] for i in range(0, len(l), 16)]
    row_number = 0
    string = ""
    for value in list_out_balance[row_number]:
        string +=f"id товара - <code>{value[0]}</code>,\n Полный текст - {value[1]},\n категория - <code>{value[2]}</code>,\n локация - <code>{value[3]}</code>,\n цена - {value[4]}$ \n ➖➖➖➖➖➖➖➖➖➖➖➖\n"
    await callback.message.edit_text(f"{string}", reply_markup=get_keyboard([0, len(list_out_balance)-1]))
    await state.update_data(li=list_out_balance)
    await state.update_data(row_number=row_number)
    await callback.answer()
    

@router.callback_query(F.data=="get_sold_product", Admin_Filter())
async def get_sold_products(callback:types.CallbackQuery,state:FSMContext, bot_db:BotDateBase):
    await state.clear()
    l = bot_db.get_account_sold()
    if len(l) < 1:
        await callback.answer()
        return
    list_out_balance = [l[i:i + 16] for i in range(0, len(l), 16)]
    row_number = 0
    string = ""
    for value in list_out_balance[row_number]:
        string +=f"id товара - <code>{value[0]}</code>,\n Полный текст - {value[1]},\n категория - <code>{value[2]}</code>,\n локация - <code>{value[3]}</code>,\n цена - {value[4]}$ \n ➖➖➖➖➖➖➖➖➖➖➖➖\n"
    await callback.message.edit_text(f"{string}", reply_markup=get_keyboard([0, len(list_out_balance)-1]))
    await state.update_data(li=list_out_balance)
    await state.update_data(row_number=row_number)
    await callback.answer()
    
def get_keyboard(state: FSMContext = None):
    buttons = [
        [],
        [types.InlineKeyboardButton(
            text="Закрыть", callback_data="turn_finish")]
    ]
    if state and state[0] != 0:
        buttons[0].append(types.InlineKeyboardButton(
            text="<", callback_data="turn_left"))
    if state and state[1] != state[0]:
        buttons[0].append(types.InlineKeyboardButton(
            text=">", callback_data="turn_right"))

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


@router.callback_query(Text(startswith="turn_"))
async def callbacks_turn(callback: types.CallbackQuery, state: FSMContext, bot: Bot, bot_db: BotDateBase):
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


async def show_history(callback: types.CallbackQuery, new_value: int, li):
    string = ""
    for value in li[new_value]:
        string += f"id товара - <code>{value[0]}</code>,\n Полный текст - {value[1]},\n категория - <code>{value[2]}</code>,\n локация - <code>{value[3]}</code>,\n цена - {value[4]}$ \n ➖➖➖➖➖➖➖➖➖➖➖➖\n"

    await callback.message.edit_text(f"{string}", reply_markup=get_keyboard([new_value, len(li)-1]))
    await callback.answer()
    


@router.callback_query(F.data=="del_product", Admin_Filter())
async def delete_item(callback:types.CallbackQuery,state:FSMContext, bot_db:BotDateBase):
    await state.clear()
    await callback.message.edit_text("Введи id товара который хочешь удалить")
    await state.set_state(Admin_State.delete_item)
    await callback.answer()
    
    
@router.message(Admin_State.delete_item)
async def deleting_by_id(message: types.Message, bot_db: BotDateBase, bot: Bot, state: FSMContext):  
    id_text=message.text 
    if id_text.isdigit():
        if bot_db.check_id_item(id_text):
            bot_db.dell_product_id(id_text)
            await message.answer("Товар успешно удален")
            await state.clear()
        else:
            await message.answer("Товара с таким ID не найдено")
    else:
        await message.answer("Введите только цифры")



@router.callback_query(F.data=="add_product",Admin_Filter())
async def add_item(callback:types.CallbackQuery,state:FSMContext, bot_db:BotDateBase):
    await state.clear()
    list_categ = ['ID = 1 vk_play', 'ID = 2 keys', 'ID = 3 programs', 'ID = 4 youtube', 'ID = 5 twitch', 'ID = 6 tiktok', 'ID = 7 instagram', 'ID = 8 twitter', 'ID = 9 facebook', 'ID = 10 roblox', 'ID = 11 genshin', 'ID = 12 amazon', 'ID = 13 netflix', 'ID = 14 games', "ID = 15 steam", "ID = 16 epic_games", "ID = 17 rockstar_games"]
    list_local = '<code>de</code>', '<code>fr</code>', '<code>uk</code>', '<code>it</code>', '<code>es</code>', '<code>cz</code>', '<code>pl</code>', '<code>hu</code>', '<code>pt</code>','<code>us</code>','<code>be</code>'
    await callback.message.edit_text("Отправь номер категории:\n"+"\n".join(list_categ)+"\nВведи 0 для отмены")
    await state.set_state(Admin_State.add_item)
    await state.update_data(category=list_categ, country=list_local)
    await callback.answer()
    
@router.message(Admin_State.add_item)
async def choice_category(message: types.Message, bot_db: BotDateBase, bot: Bot, state: FSMContext): 
    user_data=await state.get_data()
    if message.text=="0":
        await message.answer("Вы вернулись в меню",reply_markup=admin_menu)
        await state.clear()
        return
    if message.text.isdigit():
        if int(message.text) in list(range(1,18)) :
            await state.update_data(choice_category_admin=message.text)
            await state.set_state(Admin_State.add_item_price)
            if 1<=int(message.text)<=2:
                await message.answer(f"Выберите страну: \n"+"\n".join(user_data['country'])+"\nВведи 0 для отмены",reply_markup=admin_menu)
                await state.set_state(Admin_State.choise_country)
                return
            await message.answer("Введите цену товара",reply_markup=admin_menu)
        else:
            await message.answer(f"Такой категории не существует",reply_markup=admin_menu)
    else:
        await message.answer("Введите цифру (ID категории)",reply_markup=admin_menu)


@router.message(Admin_State.choise_country)
async def choice_country(message: types.Message, bot_db: BotDateBase, bot: Bot, state: FSMContext): 
    list_countries=["de","fr","uk","it","es","cz","pl","hu","pt",'us','be']
    if message.text=="0":
        await message.answer("Вы вернулись в меню",reply_markup=admin_menu)
        await state.clear()
        return
    if message.text in list_countries:
        await state.update_data(choice_admin_county=message.text)
        await message.answer("Введите цену товара",reply_markup=admin_menu)
        await state.set_state(Admin_State.add_item_price)
        
    else:
        await message.answer("Такой страны нет в списке", reply_markup=admin_menu)
    
@router.message(Admin_State.typing_log_pass)
async def typing_admin_log_pass(message: types.Message, bot_db: BotDateBase, bot: Bot, state: FSMContext): 
    user_data=await state.get_data()
    if user_data.get("choice_admin_county"):
        ch=user_data["choice_admin_county"]
    else:
        ch=0
    if message.text=="0":
        await message.answer("Вы вернулись в меню",reply_markup=admin_menu)
        await state.clear()

    elif str(message.content_type) ==  "ContentType.DOCUMENT":
        text = await pars_doc(message.document, bot)
        user_data["list_items"].append(text)

    elif message.text=="!стоп":
        for value in user_data["list_items"]:
            bot_db.add_prod_admin(value, user_data["choice_category_admin"],ch, user_data["price_item"] )
        await message.answer("Все товары успешно добавлены в базу данных")
        await state.clear()
    else:
        user_data["list_items"].append(message.text)
        await message.answer("Данные получены, можете прислать еще" )




async def pars_doc(doc_name,bot:Bot):
    res= await bot.download(doc_name)
    bytes1=res.read()
    bytes1=bytes1.decode("windows-1251")
    return bytes1

@router.message(Admin_State.add_item_price)
async def typing_price_item(message: types.Message, bot_db: BotDateBase, bot: Bot, state: FSMContext): 
    if message.text=="0":
        await message.answer("Вы вернулись в меню",reply_markup=admin_menu)
        await state.clear()
        return
    if message.text.isdigit():
        await message.answer("Введи информацию об товаре в формате 'Логин:Пароль' Дополнительная информация\nИли пришлите файлы .txt\n<b>Для остановки пришлите !стоп</b>",reply_markup=admin_menu)
        await state.update_data(price_item=message.text, list_items=[])
        await state.set_state(Admin_State.typing_log_pass)
    else:
        await message.answer("Цена должна быть числом", reply_markup=admin_menu)
        