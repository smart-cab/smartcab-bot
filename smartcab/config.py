import os
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())


TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")

ACCEPTABLE_SCHEDULE_FILE_EXTENSIONS = (".xlsx", ".xls", ".csv")


DEVICES_CALLBACK_PATTERN = "button_devices"

PASSWORD_CALLBACK_PATTERN = "button_password"

STATISTICS_CALLBACK_PATTERN = "button_statistics"

SCHEDULE_CALLBACK_PATTERN = "button_schedule"
LOAD_SCHEDULE_CALLBACK_PATTERN = "botton_schedule_load"
UPLOAD_SCHEDULE_CALLBACK_PATTERN = "botton_schedule_upload"

API_HOSTNAME = "backend"
API_PREFIX = f"http://{API_HOSTNAME}:5000"

SHOW_PASSWORD_CALLBACK_PATTERN = "botton_password_show"
UPDATE_PASSWORD_CALLBACK_PATTERN = "botton_password_update"
