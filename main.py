from flask import Flask, render_template, request, redirect, url_for
import requests
from bs4 import BeautifulSoup
import datetime
import functions
import plotly.graph_objs as go
import pandas as pd
import os

app = Flask(__name__)


@app.route("/")
def home():
    url = 'https://fr.finance.yahoo.com/devisas/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    cours_list = []

    quote_links = soup.find_all(attrs={"data-test": "quoteLink"})
    for link in quote_links:
        inner_html = link.decode_contents()
        title = link.get('title')
        cours_list.append({'key': inner_html, 'title': title})

    # Get all cours followed by user
    # followed_cours content of temp folder
    followed_cours = os.listdir('temp')
    graphs = []

    for cours in followed_cours:
        # Charger les données à partir d'un fichier CSV
        try:
            data = pd.read_csv('temp/' + cours)
        except:
            continue

        # Créer une trace pour le graphique
        trace = go.Scatter(
            x=pd.to_datetime(data['Date']),
            y=data['Close'],
            mode='lines'
        )

        # Créer la figure pour le graphique
        fig = go.Figure(data=[trace])

        # Ajouter un titre et des étiquettes d'axe
        fig.update_layout(
            title='Valeurs de clôture',
            xaxis_title='Date',
            yaxis_title='Close',
        )

        # Convertir la figure en HTML pour l'afficher dans la vue Flask
        graph_html = fig.to_html(full_html=False)
        # remove .csv from cours name
        cours = cours[:-4]
        graphs.append({'cours': cours, 'graph_html': graph_html})

    return render_template('home.html', cours=cours_list, graphs=graphs)


@app.route("/add/<cours>", methods=['GET'])
def add(cours):
    print(cours)
    now = datetime.datetime.now()
    timestamp = datetime.datetime.timestamp(now)
    timestamp = int(timestamp)

    # timestamp 1 minute ago
    timestamp_one_minute_ago = timestamp - 60

    # timestamp one year ago
    timestamp_one_year_ago = timestamp - 31536000

    # timestamp 30 days ago
    timestamp_30_days_ago = timestamp - 2592000

    link = "https://query1.finance.yahoo.com/v7/finance/download/" + cours + \
        "?period1=" + str(timestamp_one_year_ago) + "&period2=" + str(timestamp_one_minute_ago) + \
        "&interval=1d&events=history&includeAdjustedClose=true"
    print(link)
    #link = link.replace('=', '%3D')
    filepath = 'temp/' + cours + '.csv'
    user_agent = {
        'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/111.0'}

    with requests.get(link, headers=user_agent, stream=True) as r:
        if r.status_code != 200:
            print(r.status_code)
        with open(filepath, 'wb') as f:
            f.write(r.content)
            # Add csv in mongodb
        if r.status_code == 200:
            functions.add_csv_to_mongodb(functions.db[cours], filepath)
    return redirect(url_for('home'))


@app.route("/delete/<cours>", methods=['GET'])
def delete(cours):
    functions.delete_cours(cours)
    return redirect(url_for('home'))


@app.route("/get/prices/<cours>", methods=['GET'])
def get_prices(cours):
    # Get price from yahoo
    url = 'https://fr.finance.yahoo.com/quote/' + cours
    print(url)
    user_agent = {
        'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/111.0'}
    response = requests.get(url, headers=user_agent)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the div with class "D(ib) Mend(20px)" and get its html content
    if (soup.find('div', class_='D(ib) Mend(20px)') == None):
        return "Cours introuvable"

    div_content = soup.find('div', class_='D(ib) Mend(20px)').decode_contents()

    # Create a new BeautifulSoup object for the div content
    div_soup = BeautifulSoup(div_content, 'html.parser')

    # Format the HTML using Bootstrap classes h4 for first span only

    div_soup.find('fin-streamer').attrs['class'] = ['h4', 'mr-1']

    # if span contain '-' then color is red else green
    div_soup.find('span').attrs['class'] = 'h4'
    if div_soup.find('span').text[0] == '-':
        div_soup.find('span').attrs['class'] = 'h4 text-danger'
    else:
        div_soup.find('span').attrs['class'] = 'h4 text-success'

    # Get the HTML content as a string
    formatted_html = str(div_soup)

    # Return the content
    return formatted_html
