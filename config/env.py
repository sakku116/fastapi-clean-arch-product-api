from dotenv import load_dotenv
from dataclasses import dataclass
from os import getenv
from pydantic import BaseModel
from utils.helper import parseBool
load_dotenv("../.env")

@dataclass(frozen=True)
class Env(BaseModel):
    HOST: str = getenv("HOST", "0.0.0.0")
    PORT: int = int(getenv("PORT", 8000))
    DEBUG: bool = parseBool(getenv("DEBUG", "false"))
    RELOAD: bool = parseBool(getenv("RELOAD", "false"))