from aiogram import types, Router, Bot, F
from db import BotDateBase
from config import *
from aiogram.filters import Text
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from keypad import brut_akk_menu, category_local, other_services_menu, buy_local_butt_0, startmarkup, methods_pay, buy_local_butt_vkplay_0


router = Router()

class Count_buy_pro(StatesGroup):
    result_sum = State()
    other_state=State()
    nothing=State()


@router.callback_query(F.data=="back_first")
async def back_first_f(callback: types.CallbackQuery, bot_db: BotDateBase, state: FSMContext):
    await callback.message.edit_text(text=f"Наши категории", reply_markup=brut_akk_menu.as_markup())
    await state.clear()
    await callback.answer()

@router.message(Text("АККАУНТЫ"))
async def brut_acc(message: types.Message, bot_db: BotDateBase, bot: Bot, state:FSMContext):
    await message.answer('Наши категории', reply_markup=brut_akk_menu.as_markup(resize_keyboard=True))
    await state.clear()

@router.callback_query(Text(startswith="vk_play"))
async def vk_play_f(callback: types.CallbackQuery, bot_db: BotDateBase, state: FSMContext):
    type_of_vk_play=callback.data.split("_")
    await callback.message.edit_text(text=f"📋 Категория: {type_of_vk_play[2]}", reply_markup=category_local.as_markup())
    await state.update_data(category=callback.data)
    await callback.answer()

@router.callback_query(F.data=="other_services")
async def other_services_f(callback: types.CallbackQuery, bot_db: BotDateBase, state: FSMContext):
    await callback.message.edit_text(text=f"📋 Категория: другие сервисы", reply_markup=other_services_menu.as_markup())
    await state.update_data(category=callback.data)
    await state.set_state(Count_buy_pro.other_state)
    await callback.answer()


@router.callback_query(F.data=="rockstar_games")
async def depop_brute_f(callback: types.CallbackQuery, bot_db: BotDateBase, state: FSMContext):
    accounts_rockstar=bot_db.get_accounts_by_category("rockstar_games")
    if len(accounts_rockstar) == 0:
        await callback.message.edit_text(text=f"📋 Товар закончился", reply_markup=buy_local_butt_0.as_markup())
    else:
        buy_local_butt = InlineKeyboardBuilder()
        buy_local_butt.add(types.InlineKeyboardButton(text=f'|{accounts_rockstar[0][4]}$|Кол-во: {len(accounts_rockstar)}шт', callback_data="price_list"))
        buy_local_butt.add(types.InlineKeyboardButton(text="🔙Назад к категориям", callback_data="back_first"))
        buy_local_butt.adjust(1)
        await callback.message.edit_text(text=f"📋 Категории:", reply_markup=buy_local_butt.as_markup())
        await state.update_data(price=accounts_rockstar[0][4])
    await state.update_data(category=callback.data, count_items=len(accounts_rockstar),country=None)
    await callback.answer()
    
@router.callback_query(F.data=="games")
async def wallapop_brute_f(callback: types.CallbackQuery, bot_db: BotDateBase, state: FSMContext):
    accounts_games=bot_db.get_accounts_by_category("games")
    if len(accounts_games) == 0:
        await callback.message.edit_text(text=f"📋 Товар закончился", reply_markup=buy_local_butt_0.as_markup())
    else:
        buy_local_butt = InlineKeyboardBuilder()
        buy_local_butt.add(types.InlineKeyboardButton(text=f'{accounts_games[0][4]}$|Кол-во: {len(accounts_games)}шт', callback_data="price_list"))
        buy_local_butt.add(types.InlineKeyboardButton(text="🔙Назад к категориям", callback_data="back_first"))
        buy_local_butt.adjust(1)
        await callback.message.edit_text(text=f"📋 Категории:", reply_markup=buy_local_butt.as_markup())
        await state.update_data(price=accounts_games[0][4])
    await state.update_data(category=callback.data, count_items=len(accounts_games),country=None)
    await callback.answer()
    

@router.callback_query(F.data=="steam")
async def gumtree_brute_f(callback: types.CallbackQuery, bot_db: BotDateBase, state: FSMContext):
    accounts_steam=bot_db.get_accounts_by_category("steam")
    if len(accounts_steam) == 0:
        await callback.message.edit_text(text=f"📋 Товар закончился", reply_markup=buy_local_butt_0.as_markup())
    else:
        buy_local_butt = InlineKeyboardBuilder()
        buy_local_butt.add(types.InlineKeyboardButton(text=f'{accounts_steam[0][4]}$|Кол-во: {len(accounts_steam)}шт', callback_data="price_list"))
        buy_local_butt.add(types.InlineKeyboardButton(text="🔙Назад к категориям", callback_data="back_first"))
        buy_local_butt.adjust(1)
        await callback.message.edit_text(text=f"📋 Категории:", reply_markup=buy_local_butt.as_markup())
        await state.update_data(price=accounts_steam[0][4])
    await state.update_data(category=callback.data, count_items=len(accounts_steam),country=None)
    await callback.answer()
    
@router.callback_query(F.data=="epic_games")
async def grailed_brute_f(callback: types.CallbackQuery, bot_db: BotDateBase, state: FSMContext):
    accounts_epic=bot_db.get_accounts_by_category("epic_games")
    if len(accounts_epic) == 0:
        await callback.message.edit_text(text=f"📋 Товар закончился", reply_markup=buy_local_butt_0.as_markup())
    else:
        buy_local_butt = InlineKeyboardBuilder()
        buy_local_butt.add(types.InlineKeyboardButton(text=f'{accounts_epic[0][4]}$|Кол-во: {len(accounts_epic)}шт', callback_data="price_list"))
        buy_local_butt.add(types.InlineKeyboardButton(text="🔙Назад к категориям", callback_data="back_first"))
        buy_local_butt.adjust(1)
        await callback.message.edit_text(text=f"📋 Категории:", reply_markup=buy_local_butt.as_markup())
        await state.update_data(price=accounts_epic[0][4])
    await state.update_data(category=callback.data, count_items=len(accounts_epic),country=None)
    await callback.answer()

@router.callback_query(F.data=="programs")
async def ebay_kleinanzeigen_brute(callback: types.CallbackQuery, bot_db: BotDateBase, state: FSMContext):
    programs=bot_db.get_accounts_by_category("programs")
    if len(programs) == 0:
        await callback.message.edit_text(text=f"📋 Товар закончился", reply_markup=buy_local_butt_0.as_markup())
    else:
        buy_local_butt = InlineKeyboardBuilder()
        buy_local_butt.add(types.InlineKeyboardButton(text=f'{programs[0][4]}$|Кол-во: {len(programs)}шт', callback_data="price_list"))
        buy_local_butt.add(types.InlineKeyboardButton(text="🔙Назад к категориям", callback_data="back_first"))
        buy_local_butt.adjust(1)
        await callback.message.edit_text(text=f"📋 Категории:", reply_markup=buy_local_butt.as_markup())
        await state.update_data(price=programs[0][4])
    await state.update_data(category=callback.data, count_items=len(programs),country=None)
    await callback.answer()




@router.callback_query(Text(startswith="keys"))
async def vk_play_f2(callback: types.CallbackQuery, bot_db: BotDateBase, state: FSMContext):
    type_of_vk_play=callback.data.split("_")
    category_vk= await state.get_data()
    vk_play_ac=bot_db.get_vkplay_by_country(category_vk["category"], type_of_vk_play[1])
    if len(vk_play_ac) == 0:
        await callback.message.edit_text(text=f"📋 Товара нету в наличии:", reply_markup=buy_local_butt_vkplay_0.as_markup())
    else:
        buy_local_butt = InlineKeyboardBuilder()
        buy_local_butt.add(types.InlineKeyboardButton(text=f'{vk_play_ac[0][4]}$|Кол-во: {len(vk_play_ac)}шт', callback_data="price_list"))
        buy_local_butt.add(types.InlineKeyboardButton(text="🔙Назад к странам", callback_data="category_local"))
        buy_local_butt.add(types.InlineKeyboardButton(text="🔙Назад к категориям", callback_data="back_first"))
        buy_local_butt.adjust(1)
        await callback.message.edit_text(f"📋 Товар", reply_markup=buy_local_butt.as_markup())
        await state.update_data(price=vk_play_ac[0][4])
    await state.update_data(country= type_of_vk_play[1],count_items=len(vk_play_ac))
    await callback.answer() 

@router.callback_query(F.data=="price_list")
async def price_list_f(callback: types.CallbackQuery, bot_db: BotDateBase, state: FSMContext):
    user_data=await state.get_data()
    count_items=user_data["count_items"]
    await state.set_state(Count_buy_pro.result_sum)   
    await callback.message.edit_text(text=f"Отправь количество товара, которое хотите купить:  \n Доступно: {count_items}")
    await callback.answer()
    
    
    
@router.callback_query(F.data=="category_local")
async def category_local_f(callback: types.CallbackQuery, bot_db: BotDateBase, state: FSMContext):
    await callback.message.edit_text(text=f"📋 Наши категории:", reply_markup=category_local.as_markup())
    await callback.answer()

            
@router.message(Count_buy_pro.result_sum, F.text)
async def buy_part(message: types.Message, state: FSMContext, bot_db: BotDateBase):
    user_count = message.text
    user_data=await state.get_data()   
    items_count=user_data["count_items"]
    if user_data["country"] is not None:
        get_accounts_for_sale=bot_db.get_vinted_by_country(user_data["category"],user_data["country"])
    else:
        get_accounts_for_sale=bot_db.get_accounts_by_category(user_data["category"])
    
    if user_count.isdigit():
        user_count=int(user_count)
        if user_count > items_count:
            await message.answer(f'Недостаточно товара. Доступно: {len(get_accounts_for_sale)}', reply_markup=startmarkup)
            await state.clear()

        elif user_count == 0:
            await message.answer(f'Покупка отменена',
                                    reply_markup=startmarkup)
            await state.clear()
        else:
            ge_bala = bot_db.get_balance(message.from_user.id)[0]
            sum_bal = user_count*user_data["price"]
            if ge_bala < sum_bal:
                await message.answer(f'Недостаточно средств для оплаты\n Пополните баланс', reply_markup=methods_pay.as_markup())
            else:
                order_id=bot_db.add_order(message.from_user.id)[0][0]
                for i in range(user_count):
                    id_change = int(get_accounts_for_sale[i][5])
                    bot_db.add_buy_finish(id_change)
                    bot_db.add_items_inside_order(order_id, user_data["category"], user_count, user_data["price"],id_change)
                    await message.answer(f'{get_accounts_for_sale[i][0]}', reply_markup=startmarkup)
                new_balan = ge_bala - sum_bal
                bot_db.new_balance(new_balan, message.from_user.id)
                
                await message.answer(f'Поздравляем с покупкой', reply_markup=startmarkup)
                await state.clear()

            await state.clear()
    else:
        await message.answer(f'Введи только цифры', reply_markup=startmarkup)
        await state.clear()
        
        

@router.callback_query(Count_buy_pro.other_state)
async def other_category_f(callback: types.CallbackQuery, bot_db: BotDateBase, state: FSMContext):
    items_other=bot_db.get_accounts_by_category(callback.data)
    if len(items_other) == 0:
        await callback.message.edit_text(text=f"📋 Товара нету в наличии:", reply_markup=buy_local_butt_0.as_markup())
    else:
        buy_local_butt = InlineKeyboardBuilder()
        buy_local_butt.add(types.InlineKeyboardButton(text=f'{items_other[0][4]}$|Кол-во: {len(items_other)}шт', callback_data="price_list"))
        buy_local_butt.add(types.InlineKeyboardButton(text="🔙Назад к категориям", callback_data="back_first"))
        buy_local_butt.adjust(1)
        await callback.message.edit_text(f"📋 Товар", reply_markup=buy_local_butt.as_markup())
        await state.update_data(price=items_other[0][4])
    await state.update_data(category=callback.data,count_items=len(items_other),country=None)
    await state.set_state(Count_buy_pro.nothing)
    await callback.answer()