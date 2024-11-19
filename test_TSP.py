from TSP import distance_between_cities, other_cities

def test_distance_between_cities():
    assert distance_between_cities((1, 1), (2, 2)) == (2)**.5

def test_other_cities():
    assert other_cities('c', ['a', 'b', 'c']) == ['a', 'b']