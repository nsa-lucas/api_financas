from datetime import datetime


def to_datetime(date: str):
    formats = ["%d-%m-%Y", "%d/%m/%Y","%Y-%m-%d", "%Y/%m/%d"]

    for fmt in formats:
        try:
            return datetime.strptime(date, fmt)
        except ValueError:
            continue
    return None

