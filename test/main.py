
from bot.core.service.database import Database
from bot.core.service.settings import Settings
from dotenv import load_dotenv
from bot.core.exception import MemberExists

load_dotenv(verbose=True)

if __name__ == "__main__":
    try:
        setting = Settings()
        print(setting.get_authorized_roles("command"))
    except MemberExists as e:
        print(str(e))