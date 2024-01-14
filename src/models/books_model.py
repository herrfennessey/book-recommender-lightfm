import logging
from datetime import datetime

import pandas
from pydantic import BaseModel, ConfigDict

logger = logging.getLogger(__name__)


class BooksModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    books: pandas.DataFrame

    @classmethod
    def load_from_pickle(cls, path):
        with open(f"{path}/books.pkl", "rb") as f:
            start = datetime.now()
            book_df = pandas.read_pickle(f)
            book_df["genres"] = book_df["genres"].apply(set)
            logger.info(
                f"Loaded book_df in {(datetime.now() - start).microseconds / 1000} milliseconds"
            )
        return cls(books=book_df)
