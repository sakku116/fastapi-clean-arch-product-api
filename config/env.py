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

    JWT_EXP: int = int(getenv("JWT_EXP", 9)) # hours
    JWT_SECRET: str = getenv("JWT_SECRET", "secret")
    JWT_REFRESH_EXP: int = int(getenv("JWT_REFRESH_EXP", 24)) # hours
    JWT_REFRESH_SECRET: str = getenv("JWT_REFRESH_SECRET", "secret")

    MONGODB_URI: str = getenv("MONGODB_URI", "mongodb://localhost:27017")
    MONGODB_NAME: str = getenv("MONGODB_NAME", "test")