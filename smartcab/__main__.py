import logging
from smartcab import config
from smartcab import handlers
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler
from telegram import Update


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
    f"^{config.SCHEDULE_CALLBACK_PATTERN}$": handlers.load_schedule,
}


def main():
    application = ApplicationBuilder().token(config.TELEGRAM_BOT_TOKEN).build()

    for command_name, command_handler in COMMAND_HANDLERS.items():
        application.add_handler(CommandHandler(command_name, command_handler))

    for pattern, callback_handler in CALLBACK_QUERY_HANDLERS.items():
        application.add_handler(CallbackQueryHandler(callback_handler, pattern=pattern))

    application.run_polling()


if __name__ == "__main__":
    try:
        main()
    except Exception:
        import traceback

        logging.warning(traceback.format_exc())
