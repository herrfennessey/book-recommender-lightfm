import logging

import polars as pl
from flask import current_app

logger = logging.getLogger(__name__)


def get_item_to_item_recommendations(work_id, n=10):
    model = current_app.item_to_item.precomputed_recs
    book_model = current_app.book_model

    candidates = model.filter(pl.col("work_id") == work_id)
    if len(candidates) == 0:
        raise ValueError("Work ID not found in the training set.")

    # Join with additional book information and sort by score
    top_items_df = (
        candidates.join(
            book_model.books.select(["work_id", "book_title"]),
            left_on="recommended_work_id",
            right_on="work_id",
        )
        .sort(by="score", descending=True)
        .head(n)
    )

    return top_items_df.to_dicts()
