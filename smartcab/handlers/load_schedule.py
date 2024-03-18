import logging
from telegram import Update
from telegram.ext import ContextTypes


async def load_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not (query := update.callback_query):
        logging.error("The callabck query could not be received")
        return

    await query.edit_message_text(text="schedule in development")
