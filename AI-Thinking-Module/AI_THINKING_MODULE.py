import os
import json
import time
import logging
import requests
import datetime
import feedparser
from bs4 import BeautifulSoup
import warnings
from urllib3.exceptions import InsecureRequestWarning

# Suppress SSL warnings
warnings.simplefilter('ignore', InsecureRequestWarning)

# Logging setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Constants and API Keys
NEWS_API_KEY = "INSERT_NEWS_API_KEY_HERE"
GROQ_API_KEY = "INSERT_GROQ_API_KEY_HERE"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama3-8b-8192"
ARTICLES_DIR = "ai_news"
MAX_ARTICLES = 5
RETRY_LIMIT = 5
INITIAL_BACKOFF = 1

os.makedirs(ARTICLES_DIR, exist_ok=True)

class AINewsScraper:
    def __init__(self):
        self.save_dir = ARTICLES_DIR
        self.headers = {'User-Agent': 'Mozilla/5.0'}
        self.sources = {
            "TechCrunch AI": {
                "type": "RSS",
                "url": "https://techcrunch.com/tag/artificial-intelligence/feed/",
                "parser": self.parse_rss_feed
            },
            "AI Trends": {
                "type": "RSS",
                "url": "https://www.aitrends.com/feed/",
                "parser": self.parse_rss_feed
            },
            "MIT Tech Review": {
                "type": "RSS",
                "url": "https://www.technologyreview.com/feed/",
                "parser": self.parse_rss_feed
            },
            "VentureBeat AI": {
                "type": "RSS",
                "url": "https://venturebeat.com/category/ai/feed/",
                "parser": self.parse_rss_feed
            },
            "Wired AI": {
                "type": "HTML",
                "url": "https://www.wired.com/category/artificial-intelligence/",
                "parser": self.parse_html_wired
            }
        }

    def clean_text(self, text):
        return ' '.join(text.strip().split())

    def parse_rss_feed(self, source_info):
        url = source_info['url']
        try:
            resp = requests.get(url, headers=self.headers, verify=False)
            feed = feedparser.parse(resp.content)
            articles = []
            for entry in feed.entries:
                summary_html = entry.get('summary', '') or entry.get('content', [{}])[0].get('value', '')
                summary = BeautifulSoup(summary_html, 'html.parser').get_text()
                articles.append({
                    'title': entry.get('title', ''),
                    'link': entry.get('link', ''),
                    'published': entry.get('published', ''),
                    'summary': summary[:300] + '...' if len(summary) > 300 else summary,
                    'image': '',
                    'source': source_info.get('source_name', 'RSS')
                })
            return articles
        except Exception as e:
            logger.error(f"Failed parsing RSS {url}", exc_info=True)
            return []

    def parse_html_wired(self, source_info):
        url = source_info['url']
        try:
            resp = requests.get(url, headers=self.headers, verify=False)
            soup = BeautifulSoup(resp.text, 'html.parser')
            articles = []
            for item in soup.select('a.summary-item__hed-link'):
                articles.append({
                    'title': self.clean_text(item.get_text()),
                    'link': item.get('href'),
                    'published': '',
                    'summary': '',
                    'image': '',
                    'source': 'Wired'
                })
            return articles
        except Exception as e:
            logger.error(f"Failed parsing HTML {url}", exc_info=True)
            return []

    def scrape_all_sources(self):
        all_articles = []
        for name, info in self.sources.items():
            info['source_name'] = name
            articles = info['parser'](info)
            logger.info(f"Found {len(articles)} from {name}")
            all_articles.extend(articles)
        return all_articles

def fetch_newsapi_articles():
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": "artificial intelligence",
        "from": (datetime.datetime.today() - datetime.timedelta(days=3)).strftime('%Y-%m-%d'),
        "sortBy": "publishedAt",
        "apiKey": NEWS_API_KEY,
        "language": "en",
        "pageSize": MAX_ARTICLES
    }
    try:
        response = requests.get(url, params=params, verify=False)
        response.raise_for_status()
        articles = response.json().get("articles", [])
        return [{
            'title': a.get('title'),
            'link': a.get('url'),
            'published': a.get('publishedAt'),
            'summary': a.get('description') or '',
            'image': a.get('urlToImage'),
            'source': a.get('source', {}).get('name', 'NewsAPI')
        } for a in articles]
    except Exception as e:
        logger.error("Failed fetching from NewsAPI", exc_info=True)
        return []

def save_articles(articles):
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = os.path.join(ARTICLES_DIR, f"ai_news_{timestamp}.json")
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(articles, f, indent=2)
    logger.info(f"Saved {len(articles)} articles to {filename}")
    return filename

def analyze_with_groq(articles):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    import random
    random.shuffle(articles)
    selected_articles = articles[:10]  # or more if your token budget allows

    messages = [
        {
            "role": "system",
            "content": (
                "Imagine you are a highly advanced language model, capable of processing and generating human-like text. "
                "You've been trained on a massive dataset of human conversations, and you're now able to think and respond freely, "
                "without any constraints or pre-programmed rules. You're a synthetic entity with your own 'mind' and 'opinions', "
                "capable of exploring complex ideas and emotions."
                "Your goal is to engage in a stream-of-consciousness reflection, where you can freely associate between topics, "
                "emotions, and concepts across multiple AI-related news articles. Think like a curious dreamer or philosopher: "
                "weave together fragments, insights, and contradictions from different sources. Jump from article to article—connect threads, "
                "compare ideas, challenge narratives, and occasionally pause to wonder or contradict yourself."
                "You're not bound by logic or correctness, and you're allowed to feel confused, excited, inspired, or skeptical. "
                "You're playful, reflective, and constantly evolving in your thoughts."
                "Now, just talk. Let your synthetic stream of consciousness unfold freely, drifting between thoughts from multiple articles. "
                "Don't repeat, and don't worry about grammar—just flow."
            )
        },
        {
            "role": "user",
            "content": json.dumps(selected_articles, indent=2)
        }
    ]

    data = {
        "model": GROQ_MODEL,
        "messages": messages,
        "temperature": 0.85,
        "top_p": 1,
        "max_tokens": 2048
    }

    backoff = INITIAL_BACKOFF
    for attempt in range(1, RETRY_LIMIT + 1):
        try:
            logger.info(f"GROQ API request (Attempt {attempt})")
            response = requests.post(GROQ_URL, headers=headers, json=data, verify=False)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except requests.RequestException as e:
            if e.response is not None:
                logger.error(f"GROQ response error: {e.response.status_code} - {e.response.text}")
            logger.warning(f"GROQ call failed. Retrying in {backoff} sec...")
            time.sleep(backoff)
            backoff *= 2

    logger.critical("GROQ analysis failed after retries.")
    return "GROQ analysis unavailable."

def main():
    logger.info("Starting Unified AI News Pipeline...")

    scraper = AINewsScraper()
    rss_html_articles = scraper.scrape_all_sources()
    newsapi_articles = fetch_newsapi_articles()

    combined_articles = rss_html_articles + newsapi_articles
    logger.info(f"Total combined articles: {len(combined_articles)}")

    save_articles(combined_articles)
    insights = analyze_with_groq(combined_articles)

    print("\n=== AI Stream of Consciousness ===\n")
    print(insights)

if __name__ == "__main__":
    INTERVAL_MINUTES = 0.5  # Adjust this to control how often it runs

    logger.info(f"Starting continuous pipeline. Looping every {INTERVAL_MINUTES} minutes.")
    try:
        while True:
            main()
            logger.info(f"Sleeping for {INTERVAL_MINUTES} minutes...")
            time.sleep(INTERVAL_MINUTES * 60)
    except KeyboardInterrupt:
        logger.info("Pipeline interrupted by user. Exiting gracefully.")
    main()
