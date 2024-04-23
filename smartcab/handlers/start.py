import logging
from telegram import (
    KeyboardButton,
    MenuButton,
    MenuButtonCommands,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
)
import telegram
from smartcab.user_mem import usermap
from telegram.ext import ContextTypes
from smartcab.keyboards import ACCES_TO_CONTACT_KEYBOARD


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        logging.error("The message could not be received")
        return

    await update.message.reply_text(
        "Привет! Для продолжения работы, поделитесь, "
        "пожалуйста, своим номером телефона. Затем если "
        "вы являетесь администратором вы сможете "
        "воспользоваться командой /menu и получить доступ "
        "ко всему функционалу бота",
        reply_markup=ACCES_TO_CONTACT_KEYBOARD,
    )


async def handle_user_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        logging.error("The message could not be received")
        return

    if not (contact := update.message.contact):
        logging.error("Can't get contact")
        return

    if not (phone := contact.phone_number):
        logging.error("Can't get phone number")
        return

    if not (message := update.message):
        logging.error("The message could not be received")
        return

    if not (user := message.from_user):
        logging.error("Can't get message user")
        return

    if not usermap.user_is_already_exists(phone):
        if not phone.startswith("+") and not phone.startswith("8"):
            usermap.add_user(user.id, f"+{phone.replace(" ", "")}")
        else:
            usermap.add_user(user.id, f"{phone.replace(" ", "")}")

    await update.message.reply_text(
        "Отлично! Приятно познакомиться.", reply_markup=ReplyKeyboardRemove()
    )

    # await context.bot.set_chat_menu_button(
    #     update.effective_chat.id,
    #     MenuButtonCommands()
    # )
