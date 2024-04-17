from .start import start, handle_user_contact
from .menu import menu
from .devices_button import devices_button
from .schedule import load_schedule, upload_schedulde, handle_schedule_file, schedule
from .upload_statistics import upload_statistics
from .hub_password import (
    hub_password,
    show_password,
    update_password,
    handle_new_password,
)
from .admins import (
    admins,
    add_admin,
    my_status,
    remove_admin,
    handle_new_admin,
    handle_remove_admin,
    show_admin_list,
)
from .webcam import (
    webcam,
    send_last_photo,
    send_photo_by_date,
    handle_for_all_photo_by_date,
)
