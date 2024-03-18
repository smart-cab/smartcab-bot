import logging
from smartcab import fetch_data
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
    # url = 'http://localhost:5000/status'
    # data = await fetch_data(url)
    # print(data)
    await query.edit_message_text(text="А вот и статитистика!")
    if effective_chat := update.effective_chat:
        await context.bot.send_document(
            chat_id=effective_chat.id, document=open("path_to_file", "rb")
        )
