from news.news import News

news = News()
news = news.get_news(num_news=5)
for new in news:
    print(new.title)
    print(new.url)
    print('\n')
