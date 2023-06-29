import os
import pandas
from pathlib import Path
from dagster import ConfigurableIOManager


class PartionedPandasIOManager(ConfigurableIOManager):

    _base_dir = Path(os.environ["STORAGE_DIR"])

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
