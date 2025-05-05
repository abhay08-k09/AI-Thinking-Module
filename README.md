# Unified AI News Scraper and Analyzer

This project scrapes AI-related news articles from multiple sources, analyzes them using the GROQ API, and generates a stream of consciousness-like response based on the collected articles. The system continuously fetches, processes, and analyzes the latest AI news.

## Features

- Scrapes news from various sources, including:
  - TechCrunch AI
  - AI Trends
  - MIT Tech Review
  - VentureBeat AI
  - Wired AI
- Fetches additional news articles from NewsAPI.
- Uses BeautifulSoup for parsing HTML content.
- Supports RSS feed parsing using Feedparser.
- Processes and analyzes collected articles using the GROQ API (an AI language model).
- Periodic execution (set to run every 30 minutes by default).
- Logs all actions and errors for debugging and monitoring.

## Installation

1. **Clone this repository:**

    ```bash
    git clone https://github.com/yourusername/ai-news-scraper.git
    cd ai-news-scraper
    ```

2. **Create a virtual environment (optional but recommended):**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up your API keys:**

    **NewsAPI:**
    - Sign up at [NewsAPI](https://newsapi.org/) to get your API key.
    - Replace the placeholder `INSERT_NEWS_API_KEY_HERE` in the script with your API key.

    **GROQ API:**
    - Sign up at [GROQ](https://www.groq.com/) to get your API key.
    - Replace the placeholder `INSERT_GROQ_API_KEY_HERE` in the script with your API key.

5. **Optionally, change the interval at which the scraper runs** by adjusting the `INTERVAL_MINUTES` variable in the `main()` function (default is set to 0.5, meaning it runs every 30 minutes).

    ```python
    INTERVAL_MINUTES = 0.5  # Adjust this value to control how often it runs
    ```

## Usage

### Running the Scraper

To start the scraper, run the following command in your terminal:

```bash
python AI_THINKING_MODULE.py
```

This will execute the scraper, which will:

- Periodically fetch AI-related news articles.
- Analyze the collected articles using the GROQ API.
- Output an AI-generated "stream of consciousness" based on the content.

## Output

### AI Stream of Consciousness:
The scraper generates and outputs a narrative-style stream of consciousness based on the articles fetched from multiple sources.

### Saved Articles:
Articles will be saved as JSON files in the `ai_news/` folder. Each file contains the following metadata for each article:

- `title`: Title of the article.
- `link`: URL to the full article.
- `published`: Date and time the article was published.
- `summary`: A brief summary of the article.
- `source`: The source of the article (e.g., TechCrunch, NewsAPI).

### Example of a saved JSON file:

```json
[
    {
        "title": "AI Revolutionizing Healthcare: Opportunities and Challenges",
        "link": "https://www.example.com/article1",
        "published": "2025-05-01T12:30:00Z",
        "summary": "AI is revolutionizing healthcare by offering solutions for diagnostics and treatments.",
        "image": "https://www.example.com/image.jpg",
        "source": "TechCrunch AI"
    }
]
```
## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Notes:
- Replace all the placeholders (`INSERT_NEWS_API_KEY_HERE` and `INSERT_GROQ_API_KEY_HERE`) in the script with your actual API keys.
- Ensure that the dependencies are installed correctly and that the virtual environment is activated if you're using one.
- The script logs all activities, so you can monitor the progress in the console or terminal.
