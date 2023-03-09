import requests
import json
import os


class SearchEngine:
    def __init__(self):
        self.__api_key = os.getenv("GOOGLE_SEARCH_API_KEY")
        self.__search_engine_id = os.getenv("GOOGLE_SEARCH_ENGINE_ID")
        self.__base_url = f'https://www.googleapis.com/customsearch/v1?key={self.__api_key}&cx={self.__search_engine_id}'

    def search_images(self, query, num_results=2):
        images_url = []
        search_type = 'image'
        custom_query = f'&q={query}&num={num_results}&searchType={search_type}'
        url = self.__base_url+custom_query

        response = requests.get(url)
        data = json.loads(response.text)
        for item in data['items']:
            images_url.append(item['link'])

        return images_url
