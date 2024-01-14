import logging

import numpy as np
import pandas as pd
from flask import current_app

from src.models.books_model import BooksModel
from src.models.profile_model import ProfileModel

logger = logging.getLogger(__name__)


# Add a function to identify items with any of the specified genres
def get_genre_filtered_items(book_df, genre_list):
    genre_set = set(genre_list)
    mask = book_df["genres"].map(lambda genres: genre_set.issubset(genres))
    return book_df[mask]


def get_top_n_recommendations(
    user_id: str, model: ProfileModel, book_df: BooksModel, genre_list=None, n=10
):
    # Map the user ID to the internal user ID used by LightFM
    internal_user_id = model.user_id_map.get(user_id)
    if internal_user_id is None:
        raise ValueError("User ID not found in the training set.")

    # Get the interactions mask for the user (items the user has already interacted with)
    interactions_mask = model.interactions[internal_user_id].astype(bool).toarray()[0]

    # Generate predictions across all items for this user
    scores = model.model.predict(
        user_ids=internal_user_id,
        item_ids=np.arange(model.item_features_matrix.shape[0]),
        item_features=model.item_features_matrix,
    )

    # Mask out already interacted items to avoid recommending them
    scores = np.where(interactions_mask, -np.inf, scores)

    if genre_list:
        genre_filtered_items = get_genre_filtered_items(book_df, genre_list)
        genre_filtered_item_ids = genre_filtered_items.work_id.tolist()

        # Get the internal item IDs for the filtered items
        genre_filtered_internal_item_ids = [
            model.item_id_map[work_id]
            for work_id in genre_filtered_item_ids
            if work_id in model.item_id_map
        ]

        # Create a boolean mask for all items, where True indicates the item matches the genre filter
        genre_mask = np.isin(
            np.arange(model.item_features_matrix.shape[0]),
            genre_filtered_internal_item_ids,
        )

        # Apply the genre mask to the scores, setting scores of non-matching items to -np.inf
        scores = np.where(genre_mask, scores, -np.inf)

    # Rank items by score. Use argsort in descending order while avoiding recommending already interacted items
    top_item_indices = np.argsort(scores)[-n:]

    # Translate back to original item IDs and get their scores
    reverse_item_id_map = {v: k for k, v in model.item_id_map.items()}
    top_items_scores = [
        (reverse_item_id_map[idx], scores[idx]) for idx in reversed(top_item_indices)
    ]

    # Select top N items not already interacted with
    top_n_items_scores = [
        item_score for item_score in top_items_scores if not np.isinf(item_score[1])
    ][:n]
    top_n_item_ids, top_n_scores = zip(*top_n_items_scores)
    return top_n_item_ids, top_n_scores


def get_predictions(user_id, genre_list=None, n=10):
    model = current_app.profile_model
    book_df = current_app.book_model.books

    try:
        top_work_ids, top_scores = get_top_n_recommendations(
            user_id, model, book_df, genre_list=genre_list, n=n
        )
        top_items_df = pd.DataFrame({"work_id": top_work_ids, "score": top_scores})
        # Merge with the book_df to get the book titles
        top_items_df = top_items_df.merge(
            book_df[["work_id", "book_title"]], on="work_id"
        )
        recommendations = top_items_df.to_dict(orient="records")
        return recommendations
    except ValueError as e:
        logger.info(e)
