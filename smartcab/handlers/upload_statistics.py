import logging
from telegram import Update
from telegram.ext import ContextTypes


async def upload_statistics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not (query := update.callback_query):
        logging.error("The callabck query could not be received")
        return

    await query.answer("Данные загружаются...")
    await query.edit_message_text(
        text="Выполняется дамп базы данных. Пожалуйста подождите..."
    )
    # await asyncio.sleep(3)
    await query.edit_message_text(text="А вот и статитистика!")
    await context.bot.send_document(
        chat_id=update.effective_chat.id, document=open("path_to_file", "rb")
    )
