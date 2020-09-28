

def is_all_None(*args) -> bool:
    for arg in args:
        if arg is not None:
            return False
    else:
        return True