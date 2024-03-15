_DEBUG_FLAG = True


def debug(message, debug=_DEBUG_FLAG) -> None:
    if debug:
        print(">>> " + str(message))
