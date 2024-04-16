from telegram import InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from smartcab import config


ACCES_TO_CONTACT_KEYBOARD = ReplyKeyboardMarkup(
    [[KeyboardButton("Поделиться номером телефона", request_contact=True)]],
    one_time_keyboard=True,
)


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
    [
        InlineKeyboardButton(
            "Пароль хаба 🔑", callback_data=config.PASSWORD_CALLBACK_PATTERN
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

PASSWORD_INLINE_KEYBOARD = [
    [
        InlineKeyboardButton(
            "Посмотреть текущий 👁", callback_data=config.SHOW_PASSWORD_CALLBACK_PATTERN
        ),
        InlineKeyboardButton(
            "Обновить пароль ⬆️", callback_data=config.UPDATE_PASSWORD_CALLBACK_PATTERN
        ),
    ],
]
