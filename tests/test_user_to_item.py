import pytest

from src.service.user_to_item import get_genre_filtered_items


@pytest.mark.parametrize(
    "input_data, genre_list, expected_output",
    [
        # Test case 1: Single work of genres with one genre in genre_list
        (
            {"Fantasy": {"work1"}, "Adventure": {"work1"}},
            ["Fantasy"],
            {"work1"},
        ),
        # Test case 2: Multiple works and the genre_list has multiple genres
        (
            {
                "Fantasy": {"work1", "work2"},
                "Adventure": {"work1"},
                "Romance": {"work2", "work3"},
            },
            ["Fantasy", "Adventure"],
            {"work1"},
        ),
        # Test case 3: No works match the genre_list
        (
            {
                "Sci-Fi": {"work1"},
                "Adventure": {"work1", "work3"},
                "Romance": {"work2", "work3"},
            },
            ["Horror", "Mystery"],
            set(),
        ),
        # Test case 4: Empty genre_list should match nothing
        (
            {
                "Sci-Fi": {"work1"},
                "Adventure": {"work1", "work3"},
                "Romance": {"work2", "work3"},
            },
            [],
            set(),
        ),
        # Test case 5: Genre list has a subset of genres present in all works
        (
            {
                "Sci-Fi": {"work1"},
                "Adventure": {"work1", "work2", "work3"},
                "Action": {"work1", "work2", "work3"},
                "Fantasy": {"work2"},
            },
            ["Action", "Adventure"],
            {"work1", "work2", "work3"},
        ),
    ],
)
def test_get_genre_filtered_items(input_data, genre_list, expected_output):
    # Call the function with the test data
    result = get_genre_filtered_items(input_data, genre_list)

    # Verify the result
    assert result == expected_output
