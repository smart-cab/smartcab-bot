import json
import os
import logging
import aiohttp
import config
from telegram import InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from smartcab import keyboards


async def schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not (query := update.callback_query):
        logging.error("The callabck query could not be received")
        return

    await query.edit_message_text(
        text="Выберите:",
        reply_markup=InlineKeyboardMarkup(keyboards.SCHEDULE_INLINE_KEYBOARD),
    )


async def load_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not (query := update.callback_query):
        logging.error("The callabck query could not be received")
        return

    await query.edit_message_text(text="Присылайте файл таблицы, в формате .xlsx:")


async def upload_schedulde(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not (query := update.callback_query):
        logging.error("The callabck query could not be received")
        return

    await query.answer("Данные загружаются...")
    await query.edit_message_text(text="Выгружаем...")

    url = f"{config.API_PREFIX}/export_schedule"
    async with aiohttp.ClientSession(trust_env=True) as session:
        async with session.get(url, server_hostname=config.API_HOSTNAME) as response:
            excel_file_content = await response.read()
            with open("schedule.xlsx", "wb") as f:
                f.write(excel_file_content)

    await query.edit_message_text(text="Вот актаульное расписание уроков!")

    if effective_chat := update.effective_chat:
        await context.bot.send_document(
            chat_id=effective_chat.id, document=open("schedule.xlsx", "rb")
        )


async def handle_schedule_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        logging.error("The update message could not be received")
        return

    if not update.message.document:
        await update.message.reply_text("Пожалуйста пришлите excel файл")
        logging.error("The message document could not be received")
        return

    schedule_file = await update.message.document.get_file()

    if not (schedule_file):
        await update.message.reply_text("Что-то пошло не так :(")
        return

    if not schedule_file.file_path:
        logging.error("The message document could not be received")
        return

    file_extension = os.path.splitext(schedule_file.file_path)[-1].lower()
    if file_extension not in config.ACCEPTABLE_SCHEDULE_FILE_EXTENSIONS:
        await update.message.reply_text("Пожалуйста пришлите excel файл")
        return

    file_data = await schedule_file.download_as_bytearray()
    async with aiohttp.ClientSession(trust_env=True) as session:
        form_data = aiohttp.FormData()
        form_data.add_field("file", file_data)
        async with session.post(
            f"{config.API_PREFIX}/load_schedule", data=form_data
        ) as response:
            response_text = await response.text()

    await update.message.reply_text("Устанавливаем расписание...")
    if json.loads(response_text)["status"] == "ok":
        await update.message.reply_text("Отлично! Расписание успешно установлено")
    else:
        await update.message.reply_text(
            "Не удалось установить расписание. Проверить содержимое файла."
            "\n Вы всегда можете выгрузить текущее расписание и проверить в "
            "правильном ли вы формате всё указали"
        )
