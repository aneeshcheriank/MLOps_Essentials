import pytest
from unittest.mock import patch, MagicMock
from geopy.distance import geodesic
from TSP import (
    find_cordinates,
    other_cities,
    city_with_short_distance,
    distance_between_cities,
    run,
    runs,
)

@pytest.fixture
def mock_geolocator():
    """Fixture to mock geolocator for consistent results."""
    with patch("TSP.Nominatim") as mock_nominatim:
        mock_instance = MagicMock()
        mock_instance.geocode.side_effect = [
            MagicMock(latitude=52.52, longitude=13.405),  # Berlin
            None,  # UnknownCity
        ]
        mock_nominatim.return_value = mock_instance
        yield mock_instance


def test_find_cordinates(mock_geolocator):
    city_list = ["Berlin", "UnknownCity"]
    expected = {
        "Berlin": (52.52, 13.405),
        "UnknownCity": None,
    }
    assert find_cordinates(city_list) == expected


def test_other_cities():
    cities = ["Berlin", "Munich", "Hamburg"]
    current_city = "Berlin"
    result = other_cities(current_city, cities.copy())
    assert current_city not in result
    assert result == ["Munich", "Hamburg"]


def test_city_with_short_distance():
    geo_cordinates = {
        "Berlin": (52.52, 13.405),
        "Munich": (48.1351, 11.582),
        "Hamburg": (53.5511, 9.9937),
    }
    city = "Berlin"
    cities = ["Munich", "Hamburg"]

    distance, selected_city = city_with_short_distance(city, cities, geo_cordinates)

    # Expecting the closest city to Berlin to be Hamburg
    assert selected_city == "Hamburg"
    assert distance < geodesic((52.52, 13.405), (48.1351, 11.582)).kilometers


def test_distance_between_cities():
    coords_1 = (52.52, 13.405)  # Berlin
    coords_2 = (48.1351, 11.582)  # Munich
    calculated_distance = distance_between_cities(coords_1, coords_2)

    expected_distance = geodesic(coords_1, coords_2).kilometers
    assert pytest.approx(calculated_distance, 0.01) == expected_distance


@patch("TSP.find_cordinates")
def test_run(mock_find_cordinates):
    cities = ["Berlin", "Munich", "Hamburg"]
    mock_find_cordinates.return_value = {
        "Berlin": (52.52, 13.405),
        "Munich": (48.1351, 11.582),
        "Hamburg": (53.5511, 9.9937),
    }

    result = run(cities, mock_find_cordinates.return_value)

    # Validate result structure
    assert "first_city" in result
    assert "path" in result
    assert "distance" in result

    # Validate that the path and distance are non-trivial
    assert len(result["path"]) > 0
    assert result["distance"] > 0


@patch("TSP.run")
def test_runs(mock_run):
    mock_run.return_value = {"distance": 100, "path": ["Berlin", "Hamburg"]}
    trials = 5

    result = runs(trials)

    # Validate result structure
    assert result["distance"] == 100
    assert "path" in result
