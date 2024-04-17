import json
import os
import logging
import aiohttp
import config
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from smartcab import keyboards
from smartcab.user_mem import usermap


PHONE_WAS_REQUESTED = False


async def admins(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not (query := update.callback_query):
        logging.error("The callabck query could not be received")
        return

    await query.edit_message_text(
        "Выберите",
        reply_markup=InlineKeyboardMarkup(keyboards.ADMINS_KEYBOARD),
    )


async def show_admin_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not (query := update.callback_query):
        logging.error("The callabck query could not be received")
        return

    url = f"{config.API_PREFIX}/get_admins"
    async with aiohttp.ClientSession(trust_env=True) as session:
        async with session.get(url, server_hostname=config.API_HOSTNAME) as response:
            admins = await response.json()
            admins = admins["admins"]

    await query.edit_message_text(
        "\n\n".join([f"☎️   `{phone}`" for phone in admins]),
        parse_mode=ParseMode.MARKDOWN_V2,
    )


async def my_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not (query := update.callback_query):
        logging.error("The callabck query could not be received")
        return

    if not (user := query.from_user):
        logging.error("Can't get user")
        return

    url = f"{config.API_PREFIX}/get_my_status"
    async with aiohttp.ClientSession(trust_env=True) as session:
        async with session.get(
            url,
            server_hostname=config.API_HOSTNAME,
            json={"phone_number": usermap.get_phone(user.id)},
        ) as response:
            response_data = await response.json()
            is_prime = response_data["is_prime"]

    if is_prime:
        await query.edit_message_text(
            "Вы являетесь главным администратром. Вам доступны все функции, такие как: \n"
            " - добавление новых администраторов\n"
            " - удаление администраторов\n"
            " - а так же все остальные функции бота\n"
        )
    else:
        await query.edit_message_text(
            "Вы являетесь обычным администратрам. "
            "Вам доступны практически все функции бота, за исключением "
            "добавления и удаления администраторов"
        )


async def add_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global PHONE_WAS_REQUESTED

    if not (query := update.callback_query):
        logging.error("The callabck query could not be received")
        return

    if not (user := query.from_user):
        logging.error("Can't get user")
        return

    await query.answer("Проверяем данные...")

    url = f"{config.API_PREFIX}/get_my_status"
    async with aiohttp.ClientSession(trust_env=True) as session:
        async with session.get(
            url,
            server_hostname=config.API_HOSTNAME,
            json={"phone_number": usermap.get_phone(user.id)},
        ) as response:
            response_data = await response.json()
            is_prime = response_data["is_prime"]

    if is_prime:
        await query.edit_message_text(text="Пришлите номер телефона нового админа:")
        PHONE_WAS_REQUESTED = True
    else:
        await query.edit_message_text(
            text="Только главные админы могут добавлять новых"
        )
        PHONE_WAS_REQUESTED = False


async def handle_new_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global PHONE_WAS_REQUESTED
    if not PHONE_WAS_REQUESTED:
        return

    if not update.message:
        logging.error("The update message could not be received")
        return

    if not update.message.text:
        await update.message.reply_text("Пожалуйста проверьте корректность данных")
        logging.error("The message document could not be received")
        return

    phone = update.message.text

    async with aiohttp.ClientSession(trust_env=True) as session:
        async with session.post(
            f"{config.API_PREFIX}/add_admin", json={"phone_number": phone}
        ) as response:
            response_data = await response.json()

    await update.message.reply_text("Добавляем администратора ...")
    if response_data["status"] == "ok":
        await update.message.reply_text(
            f"Отлично! Админимтратор с номером {phone} успешно добавлен ✅"
        )
    else:
        await update.message.reply_text(
            "Не удалось установить пароль. Проверьте корректнотсь данных"
        )


async def remove_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not (query := update.callback_query):
        logging.error("The callabck query could not be received")
        return

    if not (user := query.from_user):
        logging.error("Can't get user")
        return

    await query.answer("Проверяем данные...")

    url = f"{config.API_PREFIX}/get_my_status"
    async with aiohttp.ClientSession(trust_env=True) as session:
        async with session.get(
            url,
            server_hostname=config.API_HOSTNAME,
            json={"phone_number": usermap.get_phone(user.id)},
        ) as response:
            response_data = await response.json()
            is_prime = response_data["is_prime"]

    if is_prime:
        url = f"{config.API_PREFIX}/get_admins"
        async with aiohttp.ClientSession(trust_env=True) as session:
            async with session.get(
                url, server_hostname=config.API_HOSTNAME
            ) as response:
                admins = await response.json()
                admins = admins["admins"]

        admins.remove(usermap.get_phone(user.id))

        admins_numbers_keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(number, callback_data=f"admin_phone_{number}")]
                for number in admins
            ]
        )

        await query.edit_message_text(
            text="Выберите кого вы хотите исключить из списка администраторов:",
            reply_markup=admins_numbers_keyboard,
        )
    else:
        await query.edit_message_text(
            text="Только главные админы могут добавлять новых"
        )


async def handle_remove_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not (callback := update.callback_query):
        logging.error("Can't get callback query")
        return

    deleted_phone = str(callback.data).split("_")[-1]

    url = f"{config.API_PREFIX}/remove_admin"
    async with aiohttp.ClientSession(trust_env=True) as session:
        async with session.delete(
            url,
            server_hostname=config.API_HOSTNAME,
            json={"phone_number": deleted_phone},
        ) as response:
            response_data = await response.json()

    if not callback.message:
        logging.error("Can't get message from callback")
        return

    if response_data["status"] == "ok":
        await callback.answer("Успех")
        await callback.message.reply_text("Администратор успешно удалён ✅")  # type: ignore
    else:
        await callback.answer()
        await callback.message.reply_text("Что-то пошло не так. Повторите попытку")  # type: ignore
