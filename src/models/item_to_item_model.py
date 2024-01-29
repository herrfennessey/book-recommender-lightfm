import datetime
import logging

import polars as pl
from pydantic import BaseModel, ConfigDict

logger = logging.getLogger(__name__)


class ItemToItemModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    precomputed_recs: pl.DataFrame

    @classmethod
    def load_from_compressed_files(cls, path):
        start = datetime.datetime.now()
        precomputed_recs = pl.read_parquet(f"{path}/item_to_item_precomputed.parquet")
        logger.info(
            f"Loaded precomputed item to item recommendations in "
            f"{round((datetime.datetime.now() - start).total_seconds() * 1000)} milliseconds"
        )
        return cls(
            precomputed_recs=precomputed_recs,
        )
