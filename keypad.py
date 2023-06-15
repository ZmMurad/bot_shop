from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from config import admin_id,channel_url
#default menu

list_start=[[types.KeyboardButton(text="АККАУНТЫ"),types.KeyboardButton(text="👨‍💼Профиль")
],[types.KeyboardButton(text="🗄Товары в наличии")]]



startmarkup=types.ReplyKeyboardMarkup(keyboard=list_start, resize_keyboard=True)
#admin menu
list_admin=[[ types.KeyboardButton(text="АККАУНТЫ"),types.KeyboardButton(text="🗄Товары в наличии"),
             types.KeyboardButton(text="👨‍💼Профиль")],
            [types.KeyboardButton(text="📨Рассылка"),
             types.KeyboardButton(text="🕹Вкл\Выкл")],[ types.KeyboardButton(text="➕Пополнить баланс"),types.KeyboardButton(text="➖Убавить баланс"),
                                                  types.KeyboardButton(text="🗳Товар")]]

admin_menu=types.ReplyKeyboardMarkup(keyboard=list_admin, resize_keyboard=True)

def check_admin(id):
    if id in admin_id:
        return admin_menu
    return startmarkup

# check sub channel
# check_sub = types.InlineKeyboardMarkup(row_width=2)
# link_sub = types.InlineKeyboardButton("Название чата", url='https://t.me/asdasdasdasdasdccz')
# check_sub_button = types.InlineKeyboardButton("Проверить", callback_data="checksub")
# check_sub.add(link_sub, check_sub_button)

# profile_more
profile_more =InlineKeyboardBuilder()
profile_more.add(types.InlineKeyboardButton(text="История заказов", callback_data="histor_order"))
profile_more.add(types.InlineKeyboardButton(text="Реферальная программа", callback_data="referral_program"))
profile_more.add(types.InlineKeyboardButton(text="Пополнить баланс", callback_data="add_balance"))
profile_more.add(types.InlineKeyboardButton(text="История пополнений", callback_data="histor_balance"))
profile_more.adjust(2)


# methods pay
methods_pay = InlineKeyboardBuilder()
methods_pay.add(types.InlineKeyboardButton(text="CryptoBot", callback_data="CryptoBot"))
methods_pay.add(types.InlineKeyboardButton(text="Cryptocloud", callback_data="crypto_cloud"))


# money_translation
money_translation = InlineKeyboardBuilder()
money_translation.add(types.InlineKeyboardButton(text="Перевести все реферальные деньги в основной баланс", callback_data="money_conclusions"))
money_translation.add(types.InlineKeyboardButton(text="Отмена", callback_data="tovar_ot"))
money_translation.adjust(1)


# brut_akk menu
brut_akk_menu = InlineKeyboardBuilder()
brut_akk_menu.add(types.InlineKeyboardButton(text="VK Play", callback_data="vk_play"))
brut_akk_menu.add(types.InlineKeyboardButton(text="Keys", callback_data="keys"))
brut_akk_menu.add(types.InlineKeyboardButton(text="Programs", callback_data="programs"))
brut_akk_menu.add(types.InlineKeyboardButton(text="Games", callback_data="games"))
brut_akk_menu.add(types.InlineKeyboardButton(text="Steam", callback_data="steam"))
brut_akk_menu.add(types.InlineKeyboardButton(text="Epic Games", callback_data="epic_games"))
brut_akk_menu.add(types.InlineKeyboardButton(text="Rockstar Games", callback_data="rockstar_games"))
brut_akk_menu.add(types.InlineKeyboardButton(text="🌏Другие сервисы🌏", callback_data="other_services"))
brut_akk_menu.adjust(1)

# other_services
other_services_menu = InlineKeyboardBuilder()
other_services_menu.add(types.InlineKeyboardButton(text="Youtube", callback_data="youtube"))
other_services_menu.add(types.InlineKeyboardButton(text="Twitch", callback_data="twitch"))
other_services_menu.add(types.InlineKeyboardButton(text="Tiktok", callback_data="tiktok"))
other_services_menu.add(types.InlineKeyboardButton(text="Instagram", callback_data="instagram"))
other_services_menu.add(types.InlineKeyboardButton(text="Twitter", callback_data="twitter"))
other_services_menu.add(types.InlineKeyboardButton(text="Facebook", callback_data="facebook"))
other_services_menu.add(types.InlineKeyboardButton(text="Roblox", callback_data="roblox"))
other_services_menu.add(types.InlineKeyboardButton(text="Genshin", callback_data="genshin"))
other_services_menu.add(types.InlineKeyboardButton(text="Amazon", callback_data="amazon"))
other_services_menu.add(types.InlineKeyboardButton(text="Netflix", callback_data="netflix"))
other_services_menu.add(types.InlineKeyboardButton(text="🔙Назад к категориям", callback_data="back_first"))
other_services_menu.adjust(1)

# category_local
category_local = InlineKeyboardBuilder()
category_local.add(types.InlineKeyboardButton(text="🔙Назад к категориям", callback_data="back_first"))
category_local.adjust(1)

buy_local_butt_vkplay_0 = InlineKeyboardBuilder()
buy_local_butt_vkplay_0.add(types.InlineKeyboardButton(text='Вернутся в меню', callback_data="tovar_ot"))
buy_local_butt_vkplay_0.add(types.InlineKeyboardButton(text="🔙Назад к категориям", callback_data="category_local"))
buy_local_butt_vkplay_0.add(types.InlineKeyboardButton(text="🔙Назад к категориям", callback_data="back_first"))
buy_local_butt_vkplay_0.adjust(1)


buy_local_butt_0 = InlineKeyboardBuilder()
buy_local_butt_0.add(types.InlineKeyboardButton(text='Вернутся в меню', callback_data="tovar_ot"))
buy_local_butt_0.add(types.InlineKeyboardButton(text="🔙Назад к категориям", callback_data="back_first"))
buy_local_butt_0.adjust(1)


#меню товар
product_menu= InlineKeyboardBuilder()
product_menu.add(types.InlineKeyboardButton(text="Товары в продаже", callback_data="get_product"))
product_menu.add(types.InlineKeyboardButton(text="Проданные товары", callback_data="get_sold_product"))
product_menu.add(types.InlineKeyboardButton(text="Добавить товар", callback_data="add_product"))
product_menu.add(types.InlineKeyboardButton(text="Удалить товар", callback_data="del_product"))
product_menu.adjust(2)


# check sub channel
check_sub = InlineKeyboardBuilder()
check_sub.adjust(1)