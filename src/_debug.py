_DEBUG_FLAG = True


def debug(message: str, debug=_DEBUG_FLAG) -> None:
    if _DEBUG_FLAG:
        print(">>> " + message)
