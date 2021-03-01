from geopy.geocoders import Nominatim


def get_current_location(latitude, longitude):
    locator = Nominatim(user_agent="myGeocoder")
    coordinates = f"{latitude}, {longitude}"
    location = locator.reverse(coordinates)
    return location.raw

