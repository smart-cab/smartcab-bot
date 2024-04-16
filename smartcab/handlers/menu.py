import logging
from smartcab import config
import aiohttp
from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from smartcab import keyboards
from smartcab.user_mem import usermap


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not (message := update.message):
        logging.error("The message could not be received")
        return

    if not (user := message.from_user):
        logging.error("Can't get message user")
        return

    user_id = user.id

    if not (usermap.user_is_already_exists(user_id)):
        await update.message.reply_text(
            "Чтобы воспользоваться функционалом нам нужно убедиться "
            "что вы администратор. Для этого в команде /start подлеитьесь с ботом контактом"
        )
        return

    url = f"{config.API_PREFIX}/get_admins"
    async with aiohttp.ClientSession(trust_env=True) as session:
        async with session.get(url, server_hostname=config.API_HOSTNAME) as response:
            admins = await response.json()
            admins = admins["admins"]

    if usermap.get_phone(user_id) in admins:
        await update.message.reply_text(
            "Что будем делать?",
            reply_markup=InlineKeyboardMarkup(keyboards.MENU_INLINE_KEYBOARD),
        )
    else:
        await update.message.reply_text(
            text="Извините, доступ к боту разрешен только для администраторов."
        )
