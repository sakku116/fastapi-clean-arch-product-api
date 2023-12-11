from dotenv import load_dotenv
from dataclasses import dataclass
from os import getenv
from utils.helper import parseBool
load_dotenv()

@dataclass(frozen=True)
class Env:
    HOST: str = getenv("HOST", "0.0.0.0")
    PORT: int = int(getenv("PORT", 8000))
    DEBUG: bool = parseBool(getenv("DEBUG", "false"))
    RELOAD: bool = parseBool(getenv("RELOAD", "false"))
    TIMEZONE: str = getenv("TIMEZONE", "Asia/Jakarta")

    MONGODB_URI: str = getenv("MONGODB_URI", "mongodb://localhost:27017")
    MONGODB_NAME: str = getenv("MONGODB_NAME", "test")