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
            "Рассписание 🗓️", callback_data=config.SCHEDULE_CALLBACK_PATTERN
        ),
        InlineKeyboardButton(
            "Выгрузить статистику 📊", callback_data=config.STATISTICS_CALLBACK_PATTERN
        ),
    ],
]

SCHEDULE_INLINE_KEYBOARD = [
    [
        InlineKeyboardButton(
            "Загрузить новое ⬆️", callback_data=config.LOAD_SCHEDULE_CALLBACK_PATTERN
        ),
        InlineKeyboardButton(
            "Выгрузить текущее ⬇️", callback_data=config.UPLOAD_SCHEDULE_CALLBACK_PATTERN
        ),
    ],
]
