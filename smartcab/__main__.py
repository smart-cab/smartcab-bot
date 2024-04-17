import logging
import re
from smartcab import config
from smartcab import handlers
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    ContextTypes,
)


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

COMMAND_HANDLERS = {
    "start": handlers.start,
    "menu": handlers.menu,
}

CALLBACK_QUERY_HANDLERS = {
    f"^{config.DEVICES_CALLBACK_PATTERN}$": handlers.devices_button,
    f"^{config.STATISTICS_CALLBACK_PATTERN}$": handlers.upload_statistics,
    f"^{config.LOAD_SCHEDULE_CALLBACK_PATTERN}$": handlers.load_schedule,
    f"^{config.UPLOAD_SCHEDULE_CALLBACK_PATTERN}$": handlers.upload_schedulde,
    f"^{config.SCHEDULE_CALLBACK_PATTERN}$": handlers.schedule,
    f"^{config.PASSWORD_CALLBACK_PATTERN}$": handlers.hub_password,
    f"^{config.SHOW_PASSWORD_CALLBACK_PATTERN}$": handlers.show_password,
    f"^{config.UPDATE_PASSWORD_CALLBACK_PATTERN}$": handlers.update_password,
    f"^{config.ADMINS_CALLBACK_PATTERN}$": handlers.admins,
    f"^{config.MY_STATUS_CALLBACK_PATTERN}$": handlers.my_status,
    f"^{config.NEW_ADMIN_CALLBACK_PATTERN}$": handlers.add_admin,
    f"^{config.REMOVE_ADMIN_CALLBACK_PATTERN}$": handlers.remove_admin,
    re.compile(r"^admin_phone_.*$"): handlers.handle_remove_admin,
    f"^{config.ADMIN_LIST}$": handlers.show_admin_list,
    f"^{config.WEBCAM_FRAMES}$": handlers.webcam,
    f"^{config.LAST_IMAGES_WEBCAM}$": handlers.send_last_photo,
    f"^{config.IMAGES_WEBCAM_BY_DATE}$": handlers.send_photo_by_date,
    re.compile(r"^date_group_.*$"): handlers.handle_for_all_photo_by_date,
}


# async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     print("==========CENCEL===========")


async def pull_text_handlers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handlers.handle_new_password(update, context)
    await handlers.handle_new_admin(update, context)


def main():
    application = ApplicationBuilder().token(config.TELEGRAM_BOT_TOKEN).build()

    for command_name, command_handler in COMMAND_HANDLERS.items():
        application.add_handler(CommandHandler(command_name, command_handler))

    for pattern, callback_handler in CALLBACK_QUERY_HANDLERS.items():
        application.add_handler(CallbackQueryHandler(callback_handler, pattern=pattern))

    application.add_handler(
        MessageHandler(filters.Document.ALL, handlers.handle_schedule_file)
    )
    application.add_handler(
        MessageHandler(filters.CONTACT, handlers.handle_user_contact)
    )

    # admin_conv_handler = ConversationHandler(
    #     entry_points=[CallbackQueryHandler(handlers.add_admin, config.NEW_ADMIN_CALLBACK_PATTERN)],
    #     states={
    #         0: [MessageHandler(filters.Text(), handlers.handle_new_admin)],
    #     },
    #     fallbacks=[CommandHandler('cancel', cancel)],
    # )
    # password_conv_handler = ConversationHandler(
    #     entry_points=[CallbackQueryHandler(handlers.update_password, config.UPDATE_PASSWORD_CALLBACK_PATTERN)],
    #     states={
    #         0: [MessageHandler(filters.Text() & ~filters.Command(), handlers.handle_new_password)],
    #     },
    #     fallbacks=[],
    # )
    # application.add_handler(admin_conv_handler)
    # application.add_handler(password_conv_handler)

    application.add_handler(MessageHandler(filters.Text(), pull_text_handlers))
    application.add_handler(MessageHandler(filters.Text(), handlers.handle_new_admin))

    application.run_polling()


if __name__ == "__main__":
    try:
        main()
    except Exception:
        import traceback

        logging.warning(traceback.format_exc())
