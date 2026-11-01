import json
import os.path
from dataclasses import dataclass
from typing import Dict
from typing_extensions import Literal

from bot.paths import CONFIG_ROOT_FOLDER

@dataclass
class Platforms:
    platform: Dict[str, int]

class Settings:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self._config = None
        self._server = None
        self._initialized = True

    @staticmethod
    def _load_json(file: str):
        if not os.path.exists(file):
            raise FileNotFoundError(f"File not found: {file}")
        with open(file, "r", encoding="utf-8-sig") as f:
            return json.load(f)

    def initialize(self):
        self._load_config()
        self._load_server()

    def _load_config(self):
        self._config = self._load_json(os.path.join(CONFIG_ROOT_FOLDER, "config.json"))
        if self._config is None:
            raise FileNotFoundError(f"Failed to load config: {CONFIG_ROOT_FOLDER}/config.json")
        return self._config

    def _load_server(self):
        self._server = self._load_json(os.path.join(CONFIG_ROOT_FOLDER, "server.json"))
        if self._server is None:
            raise FileNotFoundError(f"Failed to load config: {CONFIG_ROOT_FOLDER}/server.json")
        return self._server

    def get_configuration(self, subkey: Literal["status", "activity"]):
        return self._load_config().get("configuration").get(str(subkey))

    def get_cogs(self):
        return list(self._load_config().get("cogs").get("core"))

    def get_server_config(self, key: str, subkey: str):
        return self._load_server().get(key).get(subkey)

    def get_platforms(self):
        platform = self._load_server().get("roles").get("platforms")
        if platform is None:
            raise ValueError('Missing "platforms" key in server.json')
        return Platforms(platform=platform)

    def get_authorized_roles(self, command: str):
        roles = self._load_server().get("commands").get("authentication").get(command)
        return list(roles)

    def get_developer(self):
        return self._load_config().get("dev").get("developer")