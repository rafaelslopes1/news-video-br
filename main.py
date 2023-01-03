from news.headlines import Headlines
from news.content import NewsContent
from newspaper import ArticleException

news = Headlines('BR', 'pt-BR', 5)
headlines = news.get_headlines()
articles = []

i = 0
while i < len(headlines) and len(articles) < 5:
    headline = headlines[i]
    i += 1
    try:
        articles.append(NewsContent(headline))
    except ArticleException:
        continue

for article in articles:
    print(article.url)
