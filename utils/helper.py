import time
from uuid import uuid4

from bson import Int64


def parseBool(source: any) -> bool:
    if str(source).strip().lower() in ["none", 0, "", "false"]:
        return False
    return True


def generateUUID() -> str:
    return str(uuid4())


def generateTimeNowEpoch() -> Int64:
    return Int64(time.time())
