import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import logging
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def create_rss_feed():
    start_time = time.time()
    logging.info("Starting RSS feed generation")
    
    # Fetch the articles page
    url = "https://paulgraham.com/articles.html"
    logging.info(f"Fetching articles from {url}")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all links to articles
    links = soup.find_all('a')
    articles = []

    # Filter for actual article links and extract info
    logging.info("Processing article links")
    for link in links:
        href = link.get('href')
        if href and href.endswith('.html') and href != 'index.html' and not href.startswith('http'):
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
    logging.info("Generating RSS feed")
    rss = generate_rss_xml(articles)

    # Save to file
    output_file = 'rss.xml'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(rss)
    logging.info(f"Feed saved to {output_file}")

    end_time = time.time()
    execution_time = end_time - start_time
    
    logging.info(f"RSS feed generation completed in {execution_time:.2f} seconds")
    logging.info(f"Created feed with {len(articles)} articles")
    logging.info(f"Process completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

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
                    # Convert to proper date format for RSS
                    date_obj = datetime.strptime(date_str, "%B %Y")
                    return date_obj.strftime("%a, %d %b %Y 12:00:00 +0000")
                except:
                    pass

        # Return current date if no date found
        return datetime.now().strftime("%a, %d %b %Y 12:00:00 +0000")
    except:
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
    rss += f'  <lastBuildDate>{datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0000")}</lastBuildDate>\n'

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
