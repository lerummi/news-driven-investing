import os
import pandas
from pathlib import Path
from dagster import ConfigurableIOManager


STORAGE_DIR = Path(os.environ["STORAGE_DIR"])


class PartionedPandasIOManager(ConfigurableIOManager):
    _base_dir = STORAGE_DIR

    def _get_path(self, context) -> str:
        if context.has_partition_key:
            asset_dir = self._base_dir / "_".join(context.asset_key.path)
            asset_dir.mkdir(exist_ok=True)
            return asset_dir / f"{context.asset_partition_key}.parquet"

        else:
            self._base_dir.mkdir(exist_ok=True)
            return self._base_dir / f"{context.asset_key.path}.parquet"

    def handle_output(self, context, obj: pandas.DataFrame):
        obj.to_parquet(self._get_path(context))

    def load_input(self, context):
        return pandas.read_parquet(self._get_path(context))


def read_partitioned_pandas_asset(asset: str) -> pandas.DataFrame:
    """
    Read all partitions associcated with a specific asset and concatenate
    to pandas.DataFrame
    """

    directory = STORAGE_DIR / asset
    if not directory.exists():
        raise IOError(
            f"Apparently and asset '{asset}' is not available in the storage "
            f"directory {STORAGE_DIR}"
        )

    return pandas.concat(
        pandas.read_parquet(file) for file in directory.glob("**/*.parquet")
    )
