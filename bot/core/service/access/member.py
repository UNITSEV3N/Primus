
from bot.core.exception import MemberExists
from bot.core.service.database import Database

class Member:
    def __init__(self):
        self.database = Database()

    def does_exist(self, conn, user_id: str) -> bool:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT 1 FROM members WHERE id = %s", (user_id, ))
            return cursor.fetchone() is not None
        finally:
            cursor.close()

    def add_member(self, user_id: int, username: str, platform: str, registry: str) -> bool:
        with Database.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT 1 FROM members WHERE id = %s", (user_id,))
                if cursor.fetchone() is not None:
                    raise MemberExists("Member already exists", username)

                cursor.execute(
                    "INSERT INTO members (id, username, platform, joined, registry) "
                    "VALUES (%s, %s, %s, NOW(), %s)",
                    (user_id, username, platform, registry),
                )
            finally:
                cursor.close()
                return True
            return False

    def update_name(self, user_id: int, new_name: str):
        with Database.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "UPDATE members SET username = %s WHERE id = %s",
                    (new_name, user_id),
                )
                return cursor.rowcount > 0
            finally:
                cursor.close()
                return True
            return False

    def get_members(self) -> list:
        with Database.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT id FROM members")
                return cursor.fetchall()
            finally:
                cursor.close()
