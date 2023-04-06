# Projet-bourse
Ce site est conçu pour suivre les fluctuations de devises. Il permet aux utilisateurs de visualiser les données statistiques sur une journée, une semaine, un mois et une année. Le site affiche également un graphique représentant les données sur une année. Les données sont récupérées de Yahoo Finance via une bibliothèque et stockées dans MongoDB avec une collection pour chaque devise. Il y a également une collection "stats" qui permet d'effectuer des analyses sur toutes les devises. On peut actualiser les donnees avec le bouton 'actualiser'.

Sur le frontend, nous affichons le delta du jour. Ces données sont récupérées en effectuant un scraping du site Yahoo Finance en temps réel.

## Technologies utilisées
Le projet utilise les technologies suivantes :

pymongo\
Flask (Jinja 2)\
Pandas\
Plotly\
Beautifulsoup\
yfinance (bibliothèque Yahoo Finance)

Bootstrap
