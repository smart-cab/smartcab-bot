from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes 
from smartcab import keyboards


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Что будем делать?",
        reply_markup=InlineKeyboardMarkup(keyboards.MENU_INLINE_KEYBOARD),
    )

