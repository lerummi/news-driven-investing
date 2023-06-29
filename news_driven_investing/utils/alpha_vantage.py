import requests
import datetime
import dateutil
import time
from typing import Union
from urllib.parse import urljoin
from dagster import get_dagster_logger

from news_driven_investing.config.settings import settings


def wait_for_60_seconds_if_blocked(url: str, **params) -> requests.Response:
    """
    Alpha Vantage is limited to set of requests per minute / day. In order
    to not crash the process, just wait until a reqular result is returned."""

    logger = get_dagster_logger()

    while True:
        response = requests.get(url, params=params)

        if response.status_code == 200:
            body = response.json()
            if len(body) == 1 and "Note" in body:
                logger.info(
                    f"Detected api {url} blocked. Waiting for 60s ..."
                )
                time.sleep(60.)
            else:
                return response


def request_daily_prices(
        symbol: str, 
        start_date: Union[datetime.date, datetime.datetime, str, None] = None,
        **params
) -> requests.Response:
    """
    Request daily prices given a equity symbol and an optional start date to yesterday.
    """

    url = urljoin(settings.ALPHA_VANTAGE_ROOT, "query")

    start_date = dateutil.parser.parse(start_date)
    end_date = datetime.datetime.today()

    if start_date is None:
        params["outputsize"] = "full"
    elif (end_date - start_date).days > 100:
        params["outputsize"] = "full"
    else:
        params["outputsize"] = "compact"

    params.update(
        {
            "symbol": symbol,
            "function": "TIME_SERIES_DAILY_ADJUSTED",
            "apikey": settings.ALPHA_VANTAGE_API_KEY 

        }
    )

    return wait_for_60_seconds_if_blocked(url, **params)
