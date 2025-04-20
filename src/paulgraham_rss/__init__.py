import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup


def create_rss_feed():
    # Fetch the articles page
    url = "https://paulgraham.com/articles.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all links to articles
    links = soup.find_all('a')
    articles = []

    # Filter for actual article links and extract info
    for link in links:
        href = link.get('href')
        if (href and href.endswith('.html') and
            href != 'index.html' and not href.startswith('http')):
            title = link.text.strip()
            if title:  # Only include links with text
                article_url = f"https://paulgraham.com/{href}"
                articles.append({
                    'title': title,
                    'url': article_url,
                    # Try to extract date from the article page
                    'date': get_article_date(article_url)
                })

    # Generate RSS feed
    rss = generate_rss_xml(articles)

    # Save to file
    with open('paulgraham_articles.xml', 'w', encoding='utf-8') as f:
        f.write(rss)

    print(f"RSS feed created with {len(articles)} articles")

def get_article_date(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()

        # Look for date patterns like "March 2025" or "January 2022"
        months = ["January", "February", "March", "April", "May", "June",
                 "July", "August", "September", "October", "November", "December"]
        for month in months:
            pattern = f"{month} \\d{{4}}"
            match = re.search(pattern, text)
            if match:
                date_str = match.group(0)
                try:
                    date = datetime.strptime(date_str, "%Y-%m-%d")
                    return date.strftime("%a, %d %b %Y 12:00:00 +0000")
                except (ValueError, TypeError):
                    pass

        # Return current date if no date found
        return datetime.now().strftime("%a, %d %b %Y 12:00:00 +0000")
    except Exception:
        # Return current date if any error occurs
        return datetime.now().strftime("%a, %d %b %Y 12:00:00 +0000")

def generate_rss_xml(articles):
    # Create RSS header
    rss = '<?xml version="1.0" encoding="UTF-8" ?>\n'
    rss += '<rss version="2.0">\n'
    rss += '<channel>\n'
    rss += '  <title>Paul Graham Essays</title>\n'
    rss += '  <link>https://paulgraham.com/articles.html</link>\n'
    rss += '  <description>Essays by Paul Graham</description>\n'
    rss += (
        f'  <lastBuildDate>{datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0000")}'
        '</lastBuildDate>\n'
    )

    # Add items for each article
    for article in articles:
        rss += '  <item>\n'
        rss += f'    <title>{article["title"]}</title>\n'
        rss += f'    <link>{article["url"]}</link>\n'
        rss += f'    <guid>{article["url"]}</guid>\n'
        rss += f'    <pubDate>{article["date"]}</pubDate>\n'
        rss += '    <description><![CDATA[' + article["title"] + ']]></description>\n'
        rss += '  </item>\n'

    # Close RSS tags
    rss += '</channel>\n'
    rss += '</rss>\n'

    return rss

if __name__ == "__main__":
    create_rss_feed()
