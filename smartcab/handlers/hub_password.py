import json
import os
import logging
import aiohttp
import config
from telegram import InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from smartcab import keyboards


PASSWORD_WAS_REQUESTED = False


async def hub_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not (query := update.callback_query):
        logging.error("The callabck query could not be received")
        return

    await query.edit_message_text(
        text="Выберите:",
        reply_markup=InlineKeyboardMarkup(keyboards.PASSWORD_INLINE_KEYBOARD),
    )


async def update_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global PASSWORD_WAS_REQUESTED
    if not (query := update.callback_query):
        logging.error("The callabck query could not be received")
        return

    await query.edit_message_text(text="Пришлите пароль:")
    PASSWORD_WAS_REQUESTED = True


async def handle_new_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global PASSWORD_WAS_REQUESTED
    if not PASSWORD_WAS_REQUESTED:
        return

    if not update.message:
        logging.error("The update message could not be received")
        return

    if not update.message.text:
        await update.message.reply_text("Пожалуйста проверьте корректность данных")
        logging.error("The message document could not be received")
        return

    new_password = update.message.text

    async with aiohttp.ClientSession(trust_env=True) as session:
        async with session.post(
            f"{config.API_PREFIX}/update_password", json={"password": new_password}
        ) as response:
            response_text = await response.text()

    await update.message.reply_text("Устанавливаем пароль...")

    if json.loads(response_text)["status"] == "ok":
        await update.message.reply_text("Отлично! Пароль успешно обнавлён")
        PASSWORD_WAS_REQUESTED = False
    else:
        await update.message.reply_text(
            "Не удалось установить пароль. Проверьте корректнотсь данных"
        )


async def show_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not (query := update.callback_query):
        logging.error("The callabck query could not be received")
        return

    await query.answer("Данные загружаются...")

    url = f"{config.API_PREFIX}/get_password"
    async with aiohttp.ClientSession(trust_env=True) as session:
        async with session.get(url, server_hostname=config.API_HOSTNAME) as response:
            actually_password = json.loads(await response.read())["password"]

    await query.edit_message_text(
        text=f"`{actually_password}`", parse_mode=ParseMode.MARKDOWN_V2
    )
