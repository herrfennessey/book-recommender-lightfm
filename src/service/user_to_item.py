import logging
from typing import Dict, List, Set

import numpy as np
import polars as pl
from flask import current_app

from src.models.books_model import BooksModel
from src.models.user_to_item_model import UserToItemModel

logger = logging.getLogger(__name__)


# Add a function to identify items with any of the specified genres
def get_genre_filtered_items(
    inverted_index: Dict[str, Set[str]], genre_list: List[str]
):
    if not genre_list:
        return set()

    genre_set = set(genre_list)
    try:
        common_work_ids = set.intersection(
            *(inverted_index[genre] for genre in genre_set)
        )
    except KeyError as e:
        logger.warning(f"Genre not found in inverted index: {e}")
        return set()
    return common_work_ids


def get_top_n_recommendations(
    user_id: str,
    profile_model: UserToItemModel,
    book_model: BooksModel,
    genre_list=None,
    n=10,
):
    # Map the user ID to the internal user ID used by LightFM
    internal_user_id = profile_model.user_id_map.get(user_id)
    if internal_user_id is None:
        raise ValueError("User ID not found in the training set.")

    # Get the interactions mask for the user (items the user has already interacted with)
    interactions_mask = (
        profile_model.interactions[internal_user_id].astype(bool).toarray()[0]
    )

    # Generate predictions across all items for this user
    scores = profile_model.model.predict(
        user_ids=internal_user_id,
        item_ids=np.arange(profile_model.item_features_matrix.shape[0]),
        item_features=profile_model.item_features_matrix,
    )

    # Mask out already interacted items to avoid recommending them
    scores = np.where(interactions_mask, -np.inf, scores)

    if genre_list:
        genre_filtered_item_ids = get_genre_filtered_items(
            book_model.genre_inverted_index, genre_list
        )

        genre_filtered_internal_item_ids = [
            profile_model.item_id_map[work_id]
            for work_id in genre_filtered_item_ids
            if work_id in profile_model.item_id_map
        ]

        genre_mask = np.isin(
            np.arange(profile_model.item_features_matrix.shape[0]),
            genre_filtered_internal_item_ids,
        )

        scores = np.where(genre_mask, scores, -np.inf)

    # Rank items by score. Use argsort in descending order while avoiding recommending already interacted items
    top_item_indices = np.argsort(scores)[-n:]

    # Translate back to original item IDs and get their scores
    reverse_item_id_map = {v: k for k, v in profile_model.item_id_map.items()}
    top_items_scores = [
        (reverse_item_id_map[idx], scores[idx]) for idx in reversed(top_item_indices)
    ]

    top_n_items_scores = [
        item_score for item_score in top_items_scores if not np.isinf(item_score[1])
    ][:n]

    top_n_item_ids, top_n_scores = zip(*top_n_items_scores)
    return top_n_item_ids, top_n_scores


def get_user_to_item_recommendations(user_id, genre_list=None, n=10):
    model = current_app.user_to_item
    book_model = current_app.book_model

    try:
        top_work_ids, top_scores = get_top_n_recommendations(
            user_id, model, book_model, genre_list=genre_list, n=n
        )

        top_work_ids_np = np.array(top_work_ids)
        top_scores_np = np.array(top_scores)
        top_items_df = pl.DataFrame(
            {"work_id": top_work_ids_np, "score": top_scores_np}
        )

        top_items_df = top_items_df.join(
            book_model.books.select(["work_id", "book_title"]), on="work_id"
        )

        return top_items_df.to_dicts()

    except ValueError as e:
        logger.error(e)
