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
        InlineKeyboardButton("Админы 👤", callback_data=config.ADMINS_CALLBACK_PATTERN),
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
        InlineKeyboardButton("Снимки с камеры 📸", callback_data=config.WEBCAM_FRAMES),
    ],
]

WEBCAM_KEYBOARD = [
    [
        InlineKeyboardButton(
            "Последние фото 🏞", callback_data=config.LAST_IMAGES_WEBCAM
        ),
    ],
    [
        InlineKeyboardButton("По дате 🗓", callback_data=config.IMAGES_WEBCAM_BY_DATE),
    ],
]


ADMINS_KEYBOARD = [
    [
        InlineKeyboardButton(
            "Добавить 👥", callback_data=config.NEW_ADMIN_CALLBACK_PATTERN
        ),
        InlineKeyboardButton(
            "Удалить 🚫", callback_data=config.REMOVE_ADMIN_CALLBACK_PATTERN
        ),
    ],
    [
        InlineKeyboardButton("Список админов 📜", callback_data=config.ADMIN_LIST),
    ],
    [
        InlineKeyboardButton(
            "Мой статус 👑", callback_data=config.MY_STATUS_CALLBACK_PATTERN
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
