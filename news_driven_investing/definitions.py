from dagster import Definitions
from dagster import load_assets_from_modules

from .assets import youtube_transcript, stock_prices
from .io import PartionedPandasIOManager


defs = Definitions(
    assets=load_assets_from_modules(
        modules=[
            youtube_transcript, 
            stock_prices
        ],
    ),
    resources={"pandas_io_manager": PartionedPandasIOManager()}
)
