import logging
from telegram import Update
from telegram.ext import ContextTypes


async def upload_statistics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        logging.error("The message could not be received")
        return

    await update.message.reply_text(
        "in development",
    )
