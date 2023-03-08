from news.news import News
from dotenv import load_dotenv
import json
from data.database import Database
class Main:
    def handle(self):
        news = News()
        news = news.get_news(num_news=1)

        for new in news:
            new.generate()
            print(new)

if __name__ == "__main__":
    load_dotenv()
    main = Main()
    main.handle()