from telegram import Update
from telegram.ext import ContextTypes


async def devices_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    print("-------------", query.data)

    await query.answer()

    await query.edit_message_text(text=f"Selected option: {query.data}")
