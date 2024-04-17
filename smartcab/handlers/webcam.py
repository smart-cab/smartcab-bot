import json
import config
import os
from redis import Redis
import rpicam
import logging
import aiohttp
from itertools import groupby
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from smartcab import keyboards


r = Redis(host="redis", port=6379, decode_responses=True)


async def webcam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not (query := update.callback_query):
        logging.error("The callabck query could not be received")
        return

    await query.edit_message_text(
        text="Выберите:",
        reply_markup=InlineKeyboardMarkup(keyboards.WEBCAM_KEYBOARD),
    )


async def send_last_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for image in rpicam.get_last_nth_from_redis(config.LAST_PHOTO_COUNT, r):
        await context.bot.send_photo(
            chat_id=context._chat_id,  # type: ignore
            photo=image["image"],  # type: ignore
            caption=image["datetime"].strftime("%m.%d.%Y, %H:%M:%S"),  # type: ignore
        )


def key_func(x):
    return x["datetime"].strftime("%m.%d.%Y")


async def send_photo_by_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not (query := update.callback_query):
        logging.error("The callabck query could not be received")
        return

    date_group = []
    for key, group in groupby(
        sorted(rpicam.get_last_nth_from_redis(-1, r), key=key_func), key=key_func
    ):
        date_group.append(
            [InlineKeyboardButton(key, callback_data=f"date_group_{key}")]
        )

    await query.edit_message_text(
        text="Выберите дату:",
        reply_markup=InlineKeyboardMarkup(date_group),
    )


async def handle_for_all_photo_by_date(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    if not (callback := update.callback_query):
        logging.error("Can't get callback query")
        return

    showed_photo = str(callback.data).split("_")[-1]

    for key, group in groupby(
        sorted(rpicam.get_last_nth_from_redis(-1, r), key=key_func), key=key_func
    ):
        if key == showed_photo:
            for image in group:
                await context.bot.send_photo(
                    chat_id=context._chat_id,  # type: ignore
                    photo=image["image"],  # type: ignore
                    caption=image["datetime"].strftime("%m.%d.%Y, %H:%M:%S"),  # type: ignore
                )
