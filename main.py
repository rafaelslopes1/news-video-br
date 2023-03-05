from news.news import News

class Main:
    def handle(self):
        news = News()
        news = news.get_news(num_news=1)

        for new in news:
            print(new.source_title_generated)
            print('\n\n')
            print(new.source_summary_generated)
            print('\n\n')
            print(new.source_content_generated)
            print('\n\n')
            print(new.source_keywords_generated)
            print('\n\n')
            print(new.sentences)
            print('\n\n')

if __name__ == "__main__":
    main = Main()
    main.handle()