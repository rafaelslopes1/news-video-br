from news.headlines import Headlines
from news.content import NewsContent
from newspaper import ArticleException
from typing import List


class News:
    def get_news(self, country='BR', language='pt-BR', num_news=5) -> List[NewsContent]:
        print(f"[News] Requesting {num_news} News...")
        self.num_news = num_news
        headlines = Headlines(country, language, num_news*2)
        headlines = headlines.get_headlines()
        news = self.__get_structured_news(headlines)
        return news

    def __get_structured_news(self, headlines) -> List[NewsContent]:
        print("[News] Structuring Headlines as NewsContent")
        articles = []
        i = 0
        while i < len(headlines) and len(articles) < self.num_news:
            headline = headlines[i]
            i += 1
            try:
                articles.append(NewsContent(headline))
            except ArticleException:
                continue

        return articles
