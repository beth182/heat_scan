from geopy.geocoders import Nominatim
import time
import pandas as pd
import os
from geopy.exc import GeocoderTimedOut, GeocoderServiceError


def get_coordinates(city, country):
    """
    Function to get coordinates with retries
    :param city:
    :param country:
    :return:
    """
    # ToDo: docsring here

    query = f"{city}, {country}"
    for _ in range(5):  # Retry up to 5 times
        try:
            location = geolocator.geocode(query)
            if location:
                return (location.latitude, location.longitude)
            else:
                return None
        except (GeocoderTimedOut, GeocoderServiceError) as e:
            print(f"Error for {query}: {e}. Retrying...")
            time.sleep(5)  # Wait 5 seconds before retrying
    return None


if __name__ == '__main__':
    # read in the population csv
    current_dir = os.getcwd().replace('\\', '/') + '/'
    csv_filepath = current_dir + 'UN_2015_cities_over_300k.csv'
    # check this file exists
    assert os.path.isfile(csv_filepath)

    city_df = pd.read_csv(csv_filepath)
    city_df_temp = city_df[['Country', 'City']]
    cities_with_countries = city_df_temp.to_dict(orient='records')

    # Initialize the geolocator
    geolocator = Nominatim(user_agent="city_geocoder")

    coordinates = []

    # Iterate through the DataFrame rows
    for index, row in city_df_temp.iterrows():
        city = row['City']
        country = row['Country']
        coords = get_coordinates(city, country)
        if coords:
            coordinates.append(coords)
            print(f"{city}, {country}: {coords[0]}, {coords[1]}")
        else:
            coordinates.append((None, None))
            print(f"{city}, {country}: Not found or failed after retries")
        time.sleep(2)  # Increased delay to 2 seconds

    # Add coordinates to DataFrame
    city_df['latitude'], city_df['longitude'] = zip(*coordinates)

    city_df.to_csv(current_dir + 'UN_2015_cities_over_300k_copy.csv')

    print('end')
