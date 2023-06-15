from aiogram import types, Router, Bot, F
from db import BotDateBase
from config import *
from aiogram.filters import Text
from aiogram.utils.keyboard import InlineKeyboardBuilder
from keypad import check_admin
from aiogram.fsm.context import FSMContext


router = Router()


@router.message(Text("🗄Товары в наличии"))
async def product_stock(message: types.Message, bot_db: BotDateBase, bot: Bot, state:FSMContext):
    get_account_sale_tovar_vnalichii = bot_db.get_account_sale_tovar_vnalichii()
    await state.clear()
    get_account_vk_play = []
    get_account_keys = []
    get_account_programs = []
    get_account_youtube = []
    get_account_twitch = []
    get_account_tiktok = []
    get_account_instagram = []
    get_account_twitter = []
    get_account_facebook = []
    get_account_roblox = []
    get_account_genshin = []
    get_account_amazon = []
    get_account_netflix = []
    get_account_games=[]
    get_account_steam=[]
    get_account_epic_games=[]
    get_account_rockstar_games=[]

    # Разделение на категории
    for get_acc in get_account_sale_tovar_vnalichii:
        if get_acc[0] == 'keys':
            get_account_keys.append(get_acc)
        elif get_acc[0] == 'programs':
            get_account_programs.append(get_acc)
        elif get_acc[0]=="games":
            get_account_games.append(get_acc)
        elif get_acc[0]=="steam":
            get_account_steam.append(get_acc)
        elif get_acc[0]=="rockstar_games":
            get_account_rockstar_games.append(get_acc)
        elif get_acc[0]=="epic_games":
            get_account_epic_games.append(get_acc)
        elif get_acc[0] == 'vk_play':
            get_account_vk_play.append(get_acc)
        elif get_acc[0] == 'youtube':
            get_account_youtube.append(get_acc)
        elif get_acc[0] == 'twitch':
            get_account_twitch.append(get_acc)
        elif get_acc[0] == 'tiktok':
            get_account_tiktok.append(get_acc)
        elif get_acc[0] == 'instagram':
            get_account_instagram.append(get_acc)
        elif get_acc[0] == 'twitter':
            get_account_twitter.append(get_acc)
        elif get_acc[0] == 'facebook':
            get_account_facebook.append(get_acc)
        elif get_acc[0] == 'roblox':
            get_account_roblox.append(get_acc)
        elif get_acc[0] == 'genshin':
            get_account_genshin.append(get_acc)
        elif get_acc[0] == 'amazon':
            get_account_amazon.append(get_acc)
        elif get_acc[0] == 'netflix':
            get_account_netflix.append(get_acc)

    if get_account_programs:
        new_get_account_programs = f"Программы |{get_account_programs[0][2]}$|Кол-во: {len(get_account_programs)}шт\n"
    else:
        new_get_account_programs = ""

    if get_account_games:
        new_get_account_games= f"Игры |{get_account_games[0][2]}$|Кол-во: {len(get_account_games)}шт\n"
    else:
        new_get_account_games=""
    if get_account_steam:
        new_get_account_steam= f"Аккаунты стим |{get_account_steam[0][2]}$|Кол-во: {len(get_account_steam)}шт\n"
    else:
        new_get_account_steam=""
    if get_account_epic_games:
        new_get_account_epic_games= f"Аккаунты Епик |{get_account_epic_games[0][2]}$|Кол-во: {len(get_account_epic_games)}шт\n"
    else:
        new_get_account_epic_games=""
    if get_account_rockstar_games:
        new_get_account_rockstar_games= f"Аккаунты Epic |{get_account_rockstar_games[0][2]}$|Кол-во: {len(get_account_rockstar_games)}шт\n"
    else:
        new_get_account_rockstar_games=""
    
    
    if get_account_youtube:
        new_get_account_youtube = f" Youtube {get_account_youtube[0][2]}$|Кол-во: {len(get_account_youtube)}шт\n"
    else:
        new_get_account_youtube = ""

    if get_account_twitch:
        new_get_account_twitch = f"Twitch |{get_account_twitch[0][2]}$|Кол-во: {len(get_account_twitch)}шт\n"
    else:
        new_get_account_twitch = ""

    if get_account_tiktok:
        new_get_account_tiktok = f"Tiktok |{get_account_tiktok[0][2]}$|Кол-во: {len(get_account_tiktok)}шт\n"
    else:
        new_get_account_tiktok = ""

    if get_account_instagram:
        new_get_account_instagram = f"Instagram |{get_account_instagram[0][2]}$|Кол-во: {len(get_account_instagram)}шт\n"
    else:
        new_get_account_instagram = ""

    if get_account_twitter:
        new_get_account_twitter = f"Twitter |{get_account_twitter[0][2]}$|Кол-во: {len(get_account_twitter)}шт\n"
    else:
        new_get_account_twitter = ""

    if get_account_facebook:
        new_get_account_facebook = f"Facebook |{get_account_facebook[0][2]}$|Кол-во: {len(get_account_facebook)}шт\n"
    else:
        new_get_account_facebook = ""

    if get_account_roblox:
        new_get_account_roblox = f"Roblox |{get_account_roblox[0][2]}$|Кол-во: {len(get_account_roblox)}шт\n"
    else:
        new_get_account_roblox = ""

    if get_account_genshin:
        new_get_account_genshin = f"Genshin |{get_account_genshin[0][2]}$|Кол-во: {len(get_account_genshin)}шт\n"
    else:
        new_get_account_genshin = ""

    if get_account_amazon:
        new_get_account_amazon = f"Amazon gift |{get_account_amazon[0][2]}$|Кол-во: {len(get_account_amazon)}шт\n"
    else:
        new_get_account_amazon = ""

    if get_account_netflix:
        new_get_account_netflix = f"Netflix |{get_account_netflix[0][2]}$|Кол-во: {len(get_account_netflix)}шт\n"
    else:
        new_get_account_netflix = ""

    await message.answer(f'➖➖➖➖➖➖➖➖➖➖➖➖\n\
\nPrograms\n\
{new_get_account_programs}\
\n🌐games\n\
{new_get_account_games}\
\nSteam\n\
{new_get_account_steam}\
\nRockstar\n\
{new_get_account_rockstar_games}\
\n🧸Epic Games\n\
{new_get_account_epic_games}\
➖➖➖➖➖➖➖➖➖➖➖➖', reply_markup=check_admin(message.from_user.id))
                         
    await message.answer(f'➖➖➖➖➖➖➖➖➖➖➖➖\n\
📌YouTube\n\
{new_get_account_youtube}\
📌Twitch\n\
{new_get_account_twitch}\
📌TikTok\n\
{new_get_account_tiktok}\
📌Instagram\n\
{new_get_account_instagram}\
📌Twitter\n\
{new_get_account_twitter}\
📌Facebook\n\
{new_get_account_facebook}\
📌Roblox\n\
{new_get_account_roblox}\
📌Genshin\n\
{new_get_account_genshin}\
📌Amazon\n\
{new_get_account_amazon}\
📌Netflix\n\
{new_get_account_netflix}\
➖➖➖➖➖➖➖➖➖➖➖➖', reply_markup=check_admin(message.from_user.id))
    