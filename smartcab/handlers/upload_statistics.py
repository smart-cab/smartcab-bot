import logging
import aiohttp
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

    url = "http://localhost:5000/export_statistics"
    async with aiohttp.ClientSession(trust_env=True) as session:
        async with session.get(url) as response:
            excel_file_content = await response.read()
            with open("dumb.xlsx", "wb") as f:
                f.write(excel_file_content)

    await query.edit_message_text(text="А вот и статитистика!")
    if effective_chat := update.effective_chat:
        await context.bot.send_document(
            chat_id=effective_chat.id, document=open("dumb.xlsx", "rb")
        )
