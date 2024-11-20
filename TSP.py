#!/usr/bin/env python
import click
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from random import choice, shuffle
import config

user_agent = "Test_user_agent_Aneesh"


def find_cordinates(city_list, country="Germany"):
    geolocator = Nominatim(user_agent=user_agent)

    city_cordinates = {}
    for city in city_list:
        location = geolocator.geocode(city + ", " + country)
        if location:
            city_cordinates[city] = (location.latitude, location.longitude)
        else:
            city_cordinates[city] = None
    return city_cordinates


def other_cities(city, cities):
    """ "Return all the city in the list other than the selected"""
    cities.remove(city)
    return cities


def city_with_short_distance(city, cities, geo_cordinates):
    city_location = geo_cordinates[city]

    short_distance = 10e100
    selected_city = ""
    for other_city in cities:
        other_city_location = geo_cordinates[other_city]
        distance = distance_between_cities(city_location, other_city_location)
        if distance < short_distance:
            short_distance = distance
            selected_city = other_city
    return short_distance, selected_city


def distance_between_cities(cordinate_1, cordinate_2):
    distance = geodesic(cordinate_1, cordinate_2).kilometers
    return distance


def run(cities, city_cordinates):

    # remove cities without cordinates
    for city, cordinates in city_cordinates.items():
        if cordinates is None:
            cities.remove(city)

    path = []
    total_distance = 0
    # select a random city
    first_city = choice(cities)
    city = first_city
    while len(cities) > 1:
        cities = other_cities(city, cities)
        distance, selected_city = city_with_short_distance(
            city, cities, city_cordinates
        )
        total_distance += distance
        path.append(selected_city)
        city = selected_city

    return {"first_city": first_city, "path": path, "distance": total_distance}


def runs(trials):
    # find the cordinates for the cities
    cities = config.CITIES
    shuffle(cities)
    cordinates = find_cordinates(cities)

    min_distance = 10e100
    optimal_solution = "not found"
    for _ in range(trials):
        result = run(cities.copy(), cordinates)

        if min_distance > result["distance"]:
            min_distance = result["distance"]
            optimal_solution = result

    print(optimal_solution)
    return optimal_solution


@click.command()
@click.argument("trials", type=int)
def main(trials):
    """
    Run the function n number and find the minimum value out of the trials
    Example TSP.py 10
    will run the trials 10 times and select the experiment with minimum total distance
    """
    runs(trials)


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    main()
