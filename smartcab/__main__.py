import logging
from smartcab import config
from smartcab import handlers
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    filters,
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
}


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
        MessageHandler(filters.Text(), handlers.handle_new_password)
    )
    application.add_handler(
        MessageHandler(filters.CONTACT, handlers.handle_user_contact)
    )

    application.run_polling()


if __name__ == "__main__":
    try:
        main()
    except Exception:
        import traceback

        logging.warning(traceback.format_exc())
