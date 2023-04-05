from flask import Flask, render_template, request, redirect, url_for
import requests
from bs4 import BeautifulSoup
import datetime

app = Flask(__name__)


@app.route("/")
def home():
    url = 'https://fr.finance.yahoo.com/devisas/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    inner_html_list = []

    quote_links = soup.find_all(attrs={"data-test": "quoteLink"})
    for link in quote_links:
        inner_html = link.decode_contents()
        inner_html_list.append(inner_html)

    return render_template('hello.html', cours=inner_html_list)


@app.route("/add/<cours>", methods=['GET'])
def add(cours):
    print(cours)
    now = datetime.datetime.now()
    timestamp = datetime.datetime.timestamp(now)
    timestamp = int(timestamp)

    # timestamp 30 days ago
    timestamp_30_days_ago = timestamp - 2592000
    print(timestamp_30_days_ago)

    link = "https://query1.finance.yahoo.com/v7/finance/download/" + cours + \
        "?period1=" + str(timestamp_30_days_ago) + "&period2=" + str(timestamp) + \
        "&interval=1d&events=history&includeAdjustedClose=true"
    filepath = 'temp/'+ cours + '.csv'
    user_agent = {
        'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/111.0'}
    with requests.get(link, headers=user_agent) as r:
        with open(filepath, 'wb') as f:
            f.write(r.content)
            # Add csv in mongodb

    return redirect(url_for('home'))
