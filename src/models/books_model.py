import logging
import pickle
from datetime import datetime
from typing import Dict, Set

import polars as pl
from pydantic import BaseModel, ConfigDict

logger = logging.getLogger(__name__)


class BooksModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    books: pl.DataFrame
    genre_inverted_index: Dict[str, Set[str]]

    @classmethod
    def load_from_pickle(cls, path):
        with open(f"{path}/genres_inverted_index.pkl", "rb") as f:
            start = datetime.now()
            inverted_index = pickle.load(f)
            logger.info(
                f"Loaded inverted_index in {round((datetime.now() - start).total_seconds() * 1000)} milliseconds"
            )

        start = datetime.now()
        book_df = pl.read_parquet(f"{path}/books.parquet")
        logger.info(
            f"Loaded book_df in {round((datetime.now() - start).total_seconds() * 1000)} milliseconds"
        )

        return cls(books=book_df, genre_inverted_index=inverted_index)
