import logging
from telegram import Update
import telegram
from telegram.ext import ContextTypes
from smartcab import message_text


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        logging.error("The message could not be received")
        return

    await update.message.reply_text(
        message_text.START_GREETINGS, parse_mode=telegram.constants.ParseMode.HTML
    )
