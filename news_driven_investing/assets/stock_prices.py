import pandas
from typing import List, Dict

from dagster import asset
from dagster import (
    StaticPartitionsDefinition
)
from dagster import get_dagster_logger

from news_driven_investing.config.settings import settings
from news_driven_investing.utils import alpha_vantage


@asset(
    partitions_def=StaticPartitionsDefinition(
        list(settings.ALPHA_VANTAGE_SYMBOLS)
    ),
    group_name="stock_collect",
    io_manager_key="pandas_io_manager"
)
def stock_prices(context) -> pandas.DataFrame:
    """
    For the given stock symols extract all historical daily prices.
    """

    logger = get_dagster_logger()

    key = context.asset_partition_key_for_output()
    symbol = settings.ALPHA_VANTAGE_SYMBOLS[key]

    response = alpha_vantage.request_daily_prices(
        symbol,
        start_date=settings.START_DATE
    )

    msg = f"Status Code is {response.status_code}\n"
    try:
        msg += f"Json content:\n{str(response.json())[:100]}..."
    except:
        pass

    if response.status_code == 200:
        logger.info(f"Requesting activities successful!\n{msg}")
    
    else:
        error_msg = f"Requesting activities failed!\n{msg}" 
        logger.error(error_msg)

    response_json = response.json()

    result = pandas.DataFrame.from_dict(
        response_json["Time Series (Daily)"],
        orient="index"
    ).reset_index(names=["date"])

    # Add equity & symbol
    result["equity"] = key
    result["symbol"] = symbol

    # Limit result to start_date
    return result.query(f"date >= '{settings.START_DATE}'")
