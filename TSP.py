import click
from geopy.geocoders import Nominatim
from random import choice

CITIES = [
    "Berlin",
    "Munich",
    "Hamburg",
    "Cologne",
    "Frankfurt am Main",
    "Stuttgart",
    "Düsseldorf",
    "Dortmund",
    "Essen",
    "Leipzig",
    "Bremen",
    "Dresden",
    "Hanover",
    "Nuremberg",
    "Duisburg",
    "Bochum",
    "Wuppertal",
    "Bonn",
    "Karlsruhe",
    "Mannheim"
]

user_agent = 'Test_user_agent_Aneesh'

def find_cordinates(city_list, country='Germany'):
    geolocator = Nominatim(user_agent=user_agent)

    city_cordinates = {}
    for city in city_list:
        location = geolocator.geocode(city+ ", " + country)
        if location:
            city_cordinates[city] = (location.latitude, location.longitude)
        else:
            city_cordinates[city] = None
    return city_cordinates

def other_cities(city, cities = CITIES):
    """"Return all the city in the list other than the selected"""
    cities.remove(city)
    return cities

def city_with_short_distance(city, cities, geo_cordinates):
    city_location = geo_cordinates[city]

    short_distance = 10e100
    selected_city = ''
    for other_city in cities:
        other_city_location = geo_cordinates[other_city]
        distance = distance_between_cities(city_location, other_city_location)
        if distance < short_distance:
            short_distance = distance
            selected_city = other_city
    return short_distance, selected_city

def distance_between_cities(cordinate_1, cordinate_2):
    x1, y1 = cordinate_1
    x2, y2 = cordinate_2
    distance = ((x1-x2)**2 + (y1-y2)**2)**.5
    return distance

def run(cities=CITIES):
    # find the cordinates of the city
    city_cordinates = find_cordinates(cities)

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
        distance, selected_city = city_with_short_distance(city, cities, city_cordinates)
        total_distance += distance
        path.append(selected_city)
        city = selected_city


    return {
        'first_city': first_city, 
        'path':path, 
        'distance': total_distance
    }


if __name__ == '__main__':
    print(run())


