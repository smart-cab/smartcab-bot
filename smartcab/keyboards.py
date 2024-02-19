from telegram import InlineKeyboardButton
from smartcab import config


MENU_INLINE_KEYBOARD = [
    [InlineKeyboardButton("Девайсы 💡", callback_data=config.DEVICES_CALLBACK_PATTERN), ],
    [
        InlineKeyboardButton("Обновить рассписание 🗓️", callback_data="load_schedule_"), 
        InlineKeyboardButton("Выгрузить статистику 📊", callback_data="upload_statistics_")],
]


