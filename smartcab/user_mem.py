from redis import Redis


class UserMap:
    def __init__(self):
        self._db = Redis(host="redis", port=6379, decode_responses=True)

    def add_user(self, user_id, phone_number) -> None:
        self._db.mset({user_id: phone_number})

    def user_is_already_exists(self, user_id) -> bool:
        return bool(self._db.exists(user_id))

    def get_phone(self, user_id) -> str:
        return str(self._db.get(user_id))


usermap = UserMap()
