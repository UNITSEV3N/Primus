
import os
import logging
from dotenv import load_dotenv
from bot import Client

if __name__ == "__main__":
    load_dotenv("dev.env", verbose=True)

    TOKEN = str(os.getenv("DISCORD_TOKEN"))

    logging.getLogger("discord").setLevel(logging.WARN)
    Client().run(TOKEN, log_level=logging.WARNING)
