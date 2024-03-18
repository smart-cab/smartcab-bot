import os
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())


TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")


DEVICES_CALLBACK_PATTERN = "button_devices"
SCHEDULE_CALLBACK_PATTERN = "button_schedule"
STATISTICS_CALLBACK_PATTERN = "button_statistics"
