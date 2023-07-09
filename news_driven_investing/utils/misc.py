import datetime
from typing import Union


def first_day_next_month(
    date: Union[datetime.date, datetime.datetime]
) -> datetime.date:
    """
    Given a date, get the first day of the next month.
    """
    first_day_next_month = datetime.date(
        date.year + date.month // 12, date.month % 12 + 1, 1
    )

    return first_day_next_month
