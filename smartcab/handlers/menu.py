import logging
from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from smartcab import keyboards


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        logging.error("The message could not be received")
        return

    await update.message.reply_text(
        "Что будем делать?",
        reply_markup=InlineKeyboardMarkup(keyboards.MENU_INLINE_KEYBOARD),
    )
