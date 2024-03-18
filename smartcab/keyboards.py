from telegram import InlineKeyboardButton
from smartcab import config


MENU_INLINE_KEYBOARD = [
    [
        InlineKeyboardButton(
            "Девайсы 💡", callback_data=config.DEVICES_CALLBACK_PATTERN
        ),
    ],
    [
        InlineKeyboardButton(
            "Обновить рассписание 🗓️", callback_data=config.SCHEDULE_CALLBACK_PATTERN
        ),
        InlineKeyboardButton(
            "Выгрузить статистику 📊", callback_data=config.STATISTICS_CALLBACK_PATTERN
        ),
    ],
]
