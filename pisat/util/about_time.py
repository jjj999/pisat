
from typing import Optional
from datetime import datetime


def get_time_stamp(tag: Optional[str] = None, ext: Optional[str] = None) -> str:
    """
    Parameters
    ----------
        tag: Optional[str], default None
            Tag name added in front of time stamp.
        ext: Optional[str], default None
            File extension.

    Examples
    --------
        >> get_time_stamp("log", "csv")
        >> "log_2020.05.15-14.38.58.csv"

        >> get_time_stamp("txt")
        >> "2020.05.15-14.38.58.txt"

        >> get_time_stamp()
        >> "2020.05.15-14.38.58"
    """

    stamp = datetime.now().strftime("%Y.%m.%d-%H.%M.%S")

    def join_ext(ext: Optional[str]) -> str:
        if ext is None:
            return stamp
        else:
            return ".".join((stamp, ext))

    if tag is None:
        return join_ext(ext)

    else:
        return "_".join((tag, join_ext(ext)))
