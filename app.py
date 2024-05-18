import configparser
import os
import random
import time

from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

app = Flask(__name__)

config = configparser.ConfigParser()
config.read('config.ini')

sites_string = config['SITES']['LIST_OF_SITES']
websites = sites_string.split(',') if sites_string else []

ddgs = DDGS(proxy="socks5://localhost:1050", timeout=20)

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
]


def duckduckgo_search(website, search_terms):
    print(f'trying {website}...')
    results = ddgs.text(f'site:{website} \'{search_terms}\'', max_results=10, safesearch='off')
    return results


def google_search(website, search_terms):
    print(f'Trying Google for {website}...')
    query = f'site:{website} {search_terms}'
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument(f"user-agent={random.choice(user_agents)}")
    chromedriver_path = os.getenv('CHROME_DRIVER', '/usr/bin/chromedriver')
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"https://www.google.com/search?q={query}")
    time.sleep(random.uniform(2, 5))  # wait for the page to load
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()
    search_results = []
    for g in soup.find_all('div', class_='g'):
        anchors = g.find_all('a')
        if anchors:
            link = anchors[0]['href']
            title = g.find('h3').text if g.find('h3') else link
            search_results.append({'href': link, 'title': title})
    return search_results


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_terms = request.form['search_terms']
        search_results = {}
        for website in websites:
            results = duckduckgo_search(website, search_terms)
            if not results:
                # Add a random delay between 1 and 5 seconds before fallback
                time.sleep(random.uniform(1, 5))
                results = google_search(website, search_terms)
            search_results[website] = results
        return render_template('index.html', search_results=search_results)
    return render_template('index.html', search_results=None)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
