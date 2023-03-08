from newspaper import Config
from newspaper import Article
from newspaper import ArticleException
import requests
from text.gpt import Gpt
import nltk
from typing import List
from text.watson import Watson
from data.database import Database
import json

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'
config = Config()
config.browser_user_agent = USER_AGENT
config.request_timeout = 15

nltk.download('punkt')


class NewsContent:
    def __init__(self, news_data: dict):
        print("[NewsContent] Initialization NewsContent...")

        if not hasattr(news_data, 'link'):
            raise ValueError(
                "The news_data object must have a 'link' attribute.")

        self.__database = Database()
        self.__stored_content = self.__database.load()

        self.url = self.__get_expanded_url(news_data.link)

        self.__is_the_same = "url" in self.__stored_content and self.__stored_content[
            "url"] == self.url

        self.__article = self.__get_article()

        self.source_title_original = self.__article.title
        self.source_content_original = self.__article.text
        self.source_title_generated = ''
        self.source_content_generated = ''
        self.source_summary_generated = ''
        self.source_keywords_generated = []
        self.sentences = []

        # self.images = self.__get_images_urls()

    def __get_article(self):
        try:
            article = Article(self.url.strip(), config=config)
            article.download()
            article.parse()
            article.nlp()
            return article
        except ArticleException:
            raise ArticleException(
                f"Failed to download article from URL {self.url}")

    def __get_expanded_url(self, shorted_url):
        response = requests.head(shorted_url, allow_redirects=True)
        expanded_url = response.url
        return expanded_url

    def __get_images_urls(self):
        return self.__article.images

    def generate(self):
        without_blank_lines = self.__remove_blank_lines(
            self.source_content_original)

        have_content = "source_content_generated" in self.__stored_content and self.__stored_content["source_content_generated"] != ""
        have_title = "source_title_generated" in self.__stored_content and self.__stored_content["source_title_generated"] != ""
        have_summary = "source_summary_generated" in self.__stored_content and self.__stored_content["source_summary_generated"] != ""
        have_keywords = "source_keywords_generated" in self.__stored_content and self.__stored_content["source_keywords_generated"] != ""

        if not (have_content and have_title and have_summary and have_keywords):
            chat = self.__generate_chat()

            self.__generate_article(chat, without_blank_lines)
            self.__generate_title(chat)
            self.__generate_summary(chat)
            self.__generate_keywords(chat)

        self.__split_sentences()

    def __remove_blank_lines(self, content):
        all_lines = content.split('\n')
        without_blank_lines = list(filter(
            lambda line: len(line.strip()) != 0, all_lines))
        return without_blank_lines

    def __generate_chat(self) -> Gpt:
        bot_description = "You are a helpful assistant who sanitizes news \
        articles. The response cannot have escape characters, and must be \
        plain text, with no line breaks."

        return Gpt(bot_description)

    def __generate_article(self, chat: Gpt, base_text: str) -> str:
        article_query = "Reescreva a notícia abaixo em português brasileiro. \
                O novo texto deve ser otimizado para uma narração de vídeo de \
                notícia no Youtube, de forma a aumentar a retenção do público, \
                contendo uma linguagem de fácil compreenssão, dividido em parágrafos,\
                e mantendo riqueza de informações e o tom de seriedade. \
                Ele deve conter no mínimo 1300 caracteres (não precisa citar \
                essa informação no título), e deve ser pouco redundante. \
                Remova, do novo texto, qualquer referência ao jornal \
                que publicou a notícia. \
                O novo texto deve ser limpo, removendo quaisquer informações fora \
                do contexto da notícia, como propagandas, chamadas para ação, \
                descrição de imagens e links, mas sem encurtando-lo tanto. O novo \
                texto também deve ser escrito de forma a diminuir as chances de \
                problemas com o algoritmo do Youtube: \n{}".format(base_text)

        self.source_content_generated = chat.completion(article_query, 0.4)

        self.__database.save(self)

        return self.source_content_generated

    def __generate_title(self, chat: Gpt) -> str:
        title_query = "Escreva um título baseado no texto. \
        O título deve ser chamativo para um vídeo do Youtube, com no máximo \
        70 caracteres (não precisa citar essa informação no título). O título precisa \
        ser o mais específico possível, contendo números, quando houverem \
        números relevantes na notícia, e deve possuir adjetivos fortes."

        self.source_title_generated = chat.completion(title_query, 0.8)

        self.__database.save(self)

        return self.source_title_generated

    def __generate_summary(self, chat: Gpt) -> str:
        summary_query = "Escreva uma descrição de vídeo do Youtube, \
        baseada no texto. Ela deve ser um resumo conciso do texto, com no \
        máximo 300 caracteres (não precisa citar essa informação no título)"

        self.source_summary_generated = chat.completion(summary_query, 0.8)

        self.__database.save(self)

        return self.source_summary_generated

    def __generate_keywords(self, chat: Gpt) -> str:
        keywords_qyery = "Responda com as palavras-chave dessa notícia, em \
        um texto simples, com as palavras-chave separadas por vírgula"

        self.source_keywords_generated = chat.completion(
            keywords_qyery, 0.8).split(',')

        self.__database.save(self)

        return self.source_keywords_generated

    def __split_sentences(self) -> List[str]:
        sentences = nltk.sent_tokenize(self.source_content_generated)
        structured_sentences = []

        watson = Watson()

        for sentence in sentences:
            keywords = watson.get_keywords(sentence)
            structured_sentences.append({
                'text': sentence,
                'keywords': keywords,
                'images': []
            })

        self.sentences = structured_sentences

        self.__database.save(self)

        return self.sentences

    def __str__(self):
        return json.dumps({
            "source_title_original": self.source_title_original,
            "source_content_original": self.source_content_original,
            "source_title_generated": self.source_title_generated,
            "source_content_generated": self.source_content_generated,
            "source_summary_generated": self.source_summary_generated,
            "source_keywords_generated": self.source_keywords_generated,
            "sentences": self.sentences
        }, indent=2, ensure_ascii=False)
