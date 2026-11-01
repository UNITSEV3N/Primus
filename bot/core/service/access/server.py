
from bot.core.exception import MemberExists
from bot.core.service.database import Database

class Server:
    def __init__(self):
            self.database = Database()
            
    