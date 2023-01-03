from newspaper import Config
from newspaper import Article
from newspaper import ArticleException
from news_request import News
import requests

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'
config = Config()
config.browser_user_agent = USER_AGENT
config.request_timeout = 10

class NewsContent:
    def __init__(self, news_data):
        self.__article = self.__get_article(news_data.link)
        self.url = self.__get_expanded_url()
        self.title = self.__article.title
        self.source_content = self.__article.text.replace('\n', ' ')
        self.images = self.__get_images_urls()

    def __get_article(self, url):
        try:
            article = Article(url.strip(), config=config)
            article.download()
            article.canonical_link
            article.parse()
            return article
        except ArticleException:
            print('***FAILED TO DOWNLOAD***', article.url)

    def __get_expanded_url(self):
        # Enviar uma requisição HEAD para a URL encurtada
        response = requests.head(self.__article.url)
        expanded_url = ''

        # Verificar se a resposta foi bem-sucedida
        if response.status_code == 301:
            # Obter a URL "expandida" do cabeçalho Location da resposta
            expanded_url = response.headers['Location']

        return expanded_url

    def __get_images_urls(self):
        return self.__article.images