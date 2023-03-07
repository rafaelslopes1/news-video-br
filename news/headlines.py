import feedparser

class Headlines:
    def __init__(self, country, language, num_news):
        print("[Headlines] Initiaization...")
        self.__headlines_rss = 'https://news.google.com/news/rss'
        self.country = country
        self.language = language
        self.num_news = num_news
        self.__country_lang_params = 'hl={}&gl={}&ceid={}%3A{}'.format(
            self.language, self.country, self.country, self.language)

    def __get_rss_dict(self):
        rss_url = '{}?{}'.format(self.__headlines_rss, self.__country_lang_params)
        feed = feedparser.parse(rss_url)
        return feed

    def get_headlines(self):
        print(f"[Headlines] Requesting {self.num_news} headlines...")
        feed = self.__get_rss_dict()
        headlines = feed.entries[0:self.num_news]
        return headlines