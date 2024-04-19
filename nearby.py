import requests
import json
import csv
import time

class GooglePlaces(object):
    def __init__(self, apiKey):
        super(GooglePlaces, self).__init__()
        self.apiKey = apiKey

    def search_places_by_coordinate(self, location, radius, types):
        endpoint_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        places = []
        params = {
            'location': location,
            'radius': radius,
            'types': types,
            'key': self.apiKey
        }
        res = requests.get(endpoint_url, params=params)
        results =  json.loads(res.content)
        places.extend(results['results'])
        time.sleep(2)
        while "next_page_token" in results:
            params['pagetoken'] = results['next_page_token']
            res = requests.get(endpoint_url, params=params)
            results = json.loads(res.content)
            places.extend(results['results'])
            time.sleep(2)
        return places

    def get_place_details(self, place_id, fields):
        endpoint_url = "https://maps.googleapis.com/maps/api/place/details/json"
        params = {
            'placeid': place_id,
            'fields': ",".join(fields),
            'key': self.apiKey
        }
        res = requests.get(endpoint_url, params=params)
        place_details = json.loads(res.content)
        
        reviews = []
        if 'result' in place_details:
            reviews.extend(place_details['result'].get('reviews', []))

            while 'next_page_token' in place_details:
                params['pagetoken'] = place_details['next_page_token']
                res = requests.get(endpoint_url, params=params)
                place_details = json.loads(res.content)
                reviews.extend(place_details['result'].get('reviews', []))
                time.sleep(2)

        return reviews

def convert_to_csv(places, output_file):
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Place Name', 'Website', 'Address', 'Phone Number', 'Author Name', 'Rating', 'Text', 'Time', 'Profile Photo'])

        for place in places:
            reviews = api.get_place_details(place['place_id'], ['reviews'])
            for review in reviews:
                place_name = place.get('name', '')
                website = place.get('website', '')
                address = place.get('formatted_address', '')
                phone_number = place.get('international_phone_number', '')

                author_name = review['author_name']
                rating = review['rating']
                text = review['text']
                time = review['relative_time_description']
                profile_photo = review.get('profile_photo_url', '')

                writer.writerow([place_name, website, address, phone_number, author_name, rating, text, time, profile_photo])

apiKey = "AIzaSyDufWxOtdW3i1cA1fJQdKtOGvr3N2WjWlM"
api = GooglePlaces(apiKey)

places = api.search_places_by_coordinate("40.819057,-73.914048", "100", "restaurant")

output_file = "places_reviews.csv"
convert_to_csv(places, output_file)

print("CSV file generated successfully:", output_file)
