

def restricted_setter(*args):
    if not len(args):
        raise ValueError(
            "This method needs 1 or more arguments."
        )
    def wrapper(func):
        def setter(self, val):
            str_args = tuple(map(str, args))
            if len(str_args) > 1:
                formatted = [", ".join(str_args[:-1]), str_args[-1]]
                formatted = " or ".join(formatted)
            else:
                formatted = str_args[0]
            
            if val not in args:
                raise ValueError(
                    f"{func.__name__} must be {formatted}."
                )
            return func(self, val)
        return setter
    return wrapper
