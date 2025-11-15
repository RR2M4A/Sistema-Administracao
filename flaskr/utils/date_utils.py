from datetime import timedelta, timezone, datetime


BRAZIL_TZ = timezone(timedelta(hours=-3))


def to_start_of_day(date_str: str) -> datetime:
    """
    Transforms a DD/MM/YYYY string into a datetime object
    set to the beginning of that day (00:00:00).
    """

    try:
        return datetime.strptime(date_str, "%d/%m/%Y").replace(
            hour=0, minute=0, second=0, microsecond=0
        )
    except ValueError:
        raise ValueError(
            f"The data format should be DD/MM/YYYY, not {date_str}."
        )


def to_end_of_day(date_str: str) -> datetime:
    """
    Transforms a DD/MM/YYYY string into a datetime object
    set to the end of that day (23:59:59).
    """

    try:
        return datetime.strptime(date_str, "%d/%m/%Y").replace(
            hour=23, minute=59, second=59, microsecond=999999
        )
    except ValueError:
        raise ValueError(
            f"The data format should be DD/MM/YYYY, not {date_str}."
        )
