import bcrypt
from uuid import uuid4

def parseBool(source: any) -> bool:
    if str(source).strip().lower() in ["none", 0, "", "false"]:
        return False
    return True

def hashPassword(input: str) -> str:
    return bcrypt.hashpw(input.encode(), bcrypt.gensalt()).decode("utf-8")

def generateUUID() -> str:
    return str(uuid4())