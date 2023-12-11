def parseBool(source: any) -> bool:
    if str(source).strip().lower() in ["none", 0, "", "false"]:
        return False
    return True