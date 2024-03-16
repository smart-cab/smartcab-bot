import logging
from telegram import CallbackQuery, Update
from telegram.ext import ContextTypes


async def devices_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if not query:
        logging.error("The callabck query could not be received")
        return
    await query.answer()
    await query.edit_message_text(text=f"Selected option: {query.data}")
