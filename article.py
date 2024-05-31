import requests

def fetch_article_content(article_title):
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        'action': 'query',
        'prop': 'extracts',
        'titles': article_title,
        'format': 'json',
        'explaintext': True
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
    except requests.RequestException as e:
        return ""

    data = response.json()
    pages = data.get('query', {}).get('pages', {})
    if not pages:
        return ""
    
    page = next(iter(pages.values()), {})
    if 'missing' in page:
        return ""

    article_content = page.get('extract', '')
    if not article_content:
        return ""

    try:
        with open('article.txt', 'w', encoding='utf-8') as file:
            file.write(article_content)
    except IOError:
        return ""

    return article_content
