import asyncio
from aiogram import Bot, Dispatcher
from db import BotDateBase
from config import *
from handlers import handler_main, handler_support, profile_handler, payment_handlers,handler_product_stock,handler_brut_buy,admin_handler, last_handler
from middlewares.onn_off import Onn_Off_Callback, Onn_Off_message, Follow_Check_Callback, Follow_check_message

# Запуск бота
async def main():
    bot_db = BotDateBase('C:/python/db.sqlite3')
    bot = Bot(token=token, parse_mode="HTML")
    dp = Dispatcher()
    dp.include_routers(handler_main.router, handler_support.router, profile_handler.router, payment_handlers.router,handler_product_stock.router,handler_brut_buy.router,admin_handler.router, last_handler.router)
    dp.message.middleware(Onn_Off_message())
    dp.message.middleware(Follow_check_message())
    dp.callback_query.middleware(Onn_Off_Callback())
    dp.callback_query.middleware(Follow_Check_Callback())
    # Запускаем бота и пропускаем все накопленные входящие
    # Да, этот метод можно вызвать даже если у вас поллинг
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, bot_db=bot_db)


if __name__ == "__main__":
    asyncio.run(main())
