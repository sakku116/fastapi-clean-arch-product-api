from uuid import uuid4

import bcrypt
import jwt


def parseBool(source: any) -> bool:
    if str(source).strip().lower() in ["none", 0, "", "false"]:
        return False
    return True


def generateUUID() -> str:
    return str(uuid4())


def encodeJWT(payload: dict, secret: str) -> str:
    return jwt.encode(payload, secret, algorithm="HS256")
