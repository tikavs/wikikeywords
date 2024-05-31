import requests
import itertools

def fetch_article_content(article_title):
    # Attempt to fetch with the original title first
    article_content = fetch_content_with_title(article_title)
    if article_content:
        return article_content

    # If not found, try all possible combinations of lowercase and uppercase
    combinations = generate_case_combinations(article_title)
    for title_combination in combinations:
        article_content = fetch_content_with_title(title_combination)
        if article_content:
            return article_content

    # If none of the attempts are successful, return an empty string
    return ""

def fetch_content_with_title(article_title):
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
    except requests.RequestException:
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

def generate_case_combinations(article_title):
    # Generate all possible combinations of lowercase and uppercase letters
    combinations = [''.join(combination) for combination in itertools.product(*zip(article_title.lower(), article_title.upper()))]
    return combinations
