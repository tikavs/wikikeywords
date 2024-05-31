import requests
from flask import Flask, render_template, request
from article import fetch_article_content
from chat import perform_ai_search

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    keyword = request.form['keyword']
    exact_phrase = 'exact' in request.form
    num_results = int(request.form['num_results'])

    if exact_phrase:
        keyword = f'"{keyword}"'
    
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        'action': 'query',
        'list': 'search',
        'srsearch': keyword,
        'srlimit': num_results,
        'format': 'json'
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    search_results = data.get('query', {}).get('search', [])
    
    return render_template('index.html', keyword=keyword, search_results=search_results)

@app.route('/ai_search', methods=['POST'])
def ai_search():
    article_title = request.form['article_title']
    ai_keyword = request.form['ai_keyword']

    # Fetch and save the article content
    article_content = fetch_article_content(article_title)
    
    if not article_content:
        ai_search_results = f"Error fetching the article content for '{article_title}'. The article might be missing on Wikipedia."
    else:
        # Call perform_ai_search from chat.py
        ai_search_results = perform_ai_search(article_title, ai_keyword)

    return render_template('index.html', ai_search_results=ai_search_results)

if __name__ == '__main__':
    app.run(debug=True)
