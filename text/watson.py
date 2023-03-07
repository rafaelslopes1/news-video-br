from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 \
    import Features, KeywordsOptions

from typing import List
import os


class Watson:
    def __init__(self) -> None:
        self.__api_key = os.getenv("IBM_WATSON_API_KEY")
        self.__api_url = os.getenv("IBM_WATSON_API_URL")
        self.__authenticator = IAMAuthenticator(self.__api_key)

        self.nlu = NaturalLanguageUnderstandingV1(
            version='2022-04-07',
            authenticator=self.__authenticator,
        )
        self.nlu.set_service_url(self.__api_url)

    def get_keywords(self, sentence: str) -> List[str]:
        try:
            response = self.nlu.analyze(
                text=sentence,
                features=Features(
                    keywords=KeywordsOptions()
                )
            ).get_result()
        except ConnectionError as error:
            raise ConnectionError(error)

        return [keyword['text'] for keyword in response['keywords']]
