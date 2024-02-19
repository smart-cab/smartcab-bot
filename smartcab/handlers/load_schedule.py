from telegram import Update
from telegram.ext import ContextTypes 


async def load_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "in development",
    )


