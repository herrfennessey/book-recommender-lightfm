import pandas as pd
import pytest

from src.service.profile_service import get_genre_filtered_items


@pytest.mark.parametrize(
    "input_data, genre_list, expected_output",
    [
        # Test case 1: DataFrame and genre_list with one genre
        (
            pd.DataFrame({"genres": [["Fantasy", "Adventure"]]}),
            ["Fantasy"],
            pd.DataFrame({"genres": [["Fantasy", "Adventure"]]}),
        ),
        # Test case 2: DataFrame with multiple books and genre_list with multiple genres
        (
            pd.DataFrame(
                {
                    "genres": [
                        ["Fantasy", "Adventure"],
                        ["Fantasy", "Romance"],
                        ["Adventure", "Romance"],
                    ]
                }
            ),
            ["Fantasy", "Adventure"],
            pd.DataFrame({"genres": [["Fantasy", "Adventure"]]}),
        ),
        # Test case 3: No books match the genre_list
        (
            pd.DataFrame(
                {
                    "genres": [
                        ["Sci-Fi", "Adventure"],
                        ["Fantasy", "Romance"],
                        ["Adventure", "Romance"],
                    ]
                }
            ),
            ["Horror", "Mystery"],
            pd.DataFrame({"genres": []}, dtype=object).iloc[[]],
        ),
        # Test case 4: All books match the genre_list because it's empty
        (
            pd.DataFrame(
                {
                    "genres": [
                        ["Sci-Fi", "Adventure"],
                        ["Fantasy", "Romance"],
                        ["Adventure", "Romance"],
                    ]
                }
            ),
            [],
            pd.DataFrame(
                {
                    "genres": [
                        ["Sci-Fi", "Adventure"],
                        ["Fantasy", "Romance"],
                        ["Adventure", "Romance"],
                    ]
                }
            ),
        ),
        # Test case 5: Genre list has a subset of genres present in all books
        (
            pd.DataFrame(
                {
                    "genres": [
                        ["Sci-Fi", "Adventure", "Action"],
                        ["Action", "Adventure", "Fantasy"],
                        ["Adventure", "Action"],
                    ]
                }
            ),
            ["Action", "Adventure"],
            pd.DataFrame(
                {
                    "genres": [
                        ["Sci-Fi", "Adventure", "Action"],
                        ["Action", "Adventure", "Fantasy"],
                        ["Adventure", "Action"],
                    ]
                }
            ),
        ),
    ],
)
def test_get_genre_filtered_items(input_data, genre_list, expected_output):
    # Call the function with the test data
    result = get_genre_filtered_items(input_data, genre_list)

    # Verify the result
    pd.testing.assert_frame_equal(
        result.reset_index(drop=True), expected_output.reset_index(drop=True)
    )
