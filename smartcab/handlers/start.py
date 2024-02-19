from telegram import Update
import telegram
from telegram.ext import ContextTypes 
from smartcab import message_text


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        message_text.START_GREETINGS,
        parse_mode=telegram.constants.ParseMode.HTML
    )



