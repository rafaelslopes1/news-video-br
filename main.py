from news.news import News
from dotenv import load_dotenv
import json
class Main:
    def handle(self):
        news = News()
        news = news.get_news(num_news=1)

        for new in news:
            new.generate()
            print(new.source_title_generated)
            print('\n\n')
            print(new.source_summary_generated)
            print('\n\n')
            print(new.source_content_generated)
            print('\n\n')
            print(new.source_keywords_generated)
            print('\n\n')
            print(json.dumps(new.sentences, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    load_dotenv()
    main = Main()
    main.handle()