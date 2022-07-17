from time import sleep
from requests import get


def get_articles(search, search_len=40):
    headers = {
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/103.0.0.0 Safari/537.36'
    }
    articles = []
    page_num = 0
    while len(articles) < search_len:
        url = f'https://zen.yandex.ru/api/v3/launcher/zen-search?types=video%2Carticle&query={search}&page_num={page_num}'

        req = get(url, headers=headers)

        src = req.json()

        for article in src['items']:
            title = article['title']
            url = article['link']
            url = url[:url.index('?')]
            likes = article['socialInfo']['likesCount']
            comments = article['socialInfo']['commentCount'] if article['socialInfo']['commentsEnabled'] else None
            articles.append(dict(title=title, likes=likes, comments=comments, url=url))

        sleep(0.5)
        page_num += 1

    return sorted(articles, key=lambda art: art['likes'], reverse=True)

