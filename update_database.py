#!/usr/bin/env python3
import requests


def update_database():
    r = requests.get('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv')

    with open('data.csv', 'w') as f:
        f.write(r.text)
