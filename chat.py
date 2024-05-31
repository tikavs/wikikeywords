import os
from groq import Groq

api_key = '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'

def get_groq_response(prompt, model="llama3-8b-8192"):
    client = Groq(api_key=api_key)
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model=model,
    )
    return chat_completion.choices[0].message.content

def perform_ai_search(article_title, ai_keyword):
    # Read article content from file
    try:
        with open('article.txt', 'r', encoding='utf-8') as file:
            article_content = file.read()
    except IOError:
        return "Error reading article content."

    # Construct prompt including article content
    prompt = (
        "Please find all keywords related to " + ai_keyword + " in the article titled '" + article_title + "'.\n"
        "Article content:\n" + article_content + "\n\n"
        "Now, find all keywords related to " + ai_keyword + " in a list format. "
        "Please only return the list with no additional info. "
        "If no keywords related to " + ai_keyword + " are found in the article, return 'Not Found'."
    )

    # Get response from GROQ API
    return get_groq_response(prompt)
