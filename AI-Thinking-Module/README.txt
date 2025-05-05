Unified AI News Scraper and Analyzer
This project scrapes AI-related news articles from multiple sources, analyzes them using the GROQ API, and generates a stream of consciousness-like response based on the collected articles. The system continuously fetches, processes, and analyzes the latest AI news.

Features
Scrapes news from various sources, including:

TechCrunch AI

AI Trends

MIT Tech Review

VentureBeat AI

Wired AI

Fetches additional news articles from NewsAPI.

Uses BeautifulSoup for parsing HTML content.

Supports RSS feed parsing using Feedparser.

Processes and analyzes collected articles using the GROQ API (an AI language model).

Periodic execution (set to run every 30 minutes by default).

Logs all actions and errors for debugging and monitoring.

Installation
Clone this repository:

bash
Copy
Edit
git clone https://github.com/yourusername/ai-news-scraper.git
cd ai-news-scraper
Create a virtual environment (optional but recommended):

bash
Copy
Edit
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Set up your API keys:

NewsAPI:

Sign up at NewsAPI to get your API key.

Replace the placeholder INSERT_NEWS_API_KEY_HERE in the script with your API key.

GROQ API:

Sign up at GROQ to get your API key.

Replace the placeholder INSERT_GROQ_API_KEY_HERE in the script with your API key.

Optionally, change the interval at which the scraper runs by adjusting the INTERVAL_MINUTES variable in the main() function (default is set to 0.5, meaning it runs every 30 minutes).

python
Copy
Edit
INTERVAL_MINUTES = 0.5  # Adjust this value to control how often it runs
Usage
Running the Scraper
To start the scraper, simply run the AI_THINKING_MODULE.py script:

bash
Copy
Edit
python AI_THINKING_MODULE.py
This will start the scraper, which will fetch and analyze articles periodically based on the specified interval.

Output
The script will output the "AI Stream of Consciousness" after analyzing the articles. This output is an AI-generated, narrative-style synthesis of the articles fetched from multiple sources.

The articles are saved as JSON files with timestamps in the ai_news/ folder. Each file contains metadata for every article, including title, link, published date, summary, and source.

Example of saved JSON file:

json
Copy
Edit
[
    {
        "title": "AI Revolutionizing Healthcare: Opportunities and Challenges",
        "link": "https://www.example.com/article1",
        "published": "2025-05-01T12:30:00Z",
        "summary": "AI is increasingly being used in healthcare, providing solutions for diagnostic tools, personalized treatments, and much more. This article explores the opportunities and challenges of this revolution.",
        "image": "https://www.example.com/image.jpg",
        "source": "TechCrunch AI"
    },
    ...
]
Configuration
API Keys
You will need to set up two API keys:

NEWS_API_KEY:

Get your NewsAPI key from NewsAPI.

Replace the placeholder INSERT_NEWS_API_KEY_HERE with your key in the script.

GROQ_API_KEY:

Get your GROQ API key from GROQ.

Replace the placeholder INSERT_GROQ_API_KEY_HERE with your key in the script.

Adjusting the Run Interval
By default, the scraper runs every 30 minutes. You can adjust this by changing the INTERVAL_MINUTES variable in the script:

python
Copy
Edit
INTERVAL_MINUTES = 0.5  # This means the script runs every 30 minutes.
Change the value of INTERVAL_MINUTES to any number (in minutes) to control how often the scraper runs. For example, to make it run every hour, set it to 60:

python
Copy
Edit
INTERVAL_MINUTES = 60  # Runs every hour
License
This project is licensed under the MIT License - see the LICENSE file for details.

Notes:
Replace all the placeholders (INSERT_NEWS_API_KEY_HERE and INSERT_GROQ_API_KEY_HERE) in the script with your actual API keys.

Ensure that the dependencies are installed correctly and that the virtual environment is activated if you're using one.

You can modify the interval at which the scraper runs by adjusting the INTERVAL_MINUTES variable.

The script logs all activities, so you can monitor the progress in the console or terminal.