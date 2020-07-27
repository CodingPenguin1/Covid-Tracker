import csv
import json
from os import path, mkdir

import requests
from bs4 import BeautifulSoup


class County:
    def __init__(self, name):
        self.name = name

        self.dates = []
        self.active = []
        self.confirmed = []
        self.deaths = []
        self.recovered = []
        self.new_per_day = []

        self.update_data()

    def update_data(self):
        # Get webpage content
        website = requests.get(f'https://www.covidtrackers.com/usa/ohio/{self.name.lower()}-county/')
        website_html = website.text

        # Initialize parser
        soup = BeautifulSoup(website_html, 'html.parser')

        # Parse out data
        data_json = soup.find('canvas', {'class': 'covid-case-line-chart'}).attrs['data-json']
        data_json = json.loads(data_json)

        days = data_json['day']
        active = data_json['open']
        confirmed = data_json['confirmed']
        deaths = data_json['deaths']
        recovered = data_json['recovered']

        # Load data in to list for easy parsing
        data = []
        for i in range(len(days)):
            data.append((days[i], active[i], confirmed[i], deaths[i], recovered[i]))
        data.reverse()

        # Load data from CSV
        csv_data = self.load_csv()

        # Write new data to CSV
        known_dates = []
        for day in csv_data:
            known_dates.append(day[0])

        for day in data:
            if day[0] not in known_dates:
                csv_data.append(day)
        self.write_csv(csv_data)

        # Copy data to object properties
        for date in data:
            self.dates.append(date[0])
            self.active.append(date[1])
            self.confirmed.append(date[2])
            self.deaths.append(date[3])
            self.recovered.append(date[4])

        # Create new cases per day list
        self.new_per_day = [0]
        for i in range(1, len(self.active)):
            self.new_per_day.append(self.active[i] - self.active[i - 1])

    def load_csv(self):
        filename = f'data/{self.name.lower()}.csv'
        if path.exists(filename):
            with open(filename, 'r') as f:
                csv_data = csv.reader(f)
                csv_data = [_ for _ in csv_data]
                # csv_data.reverse()
                return csv_data
        return []

    def write_csv(self, data):
        filename = f'data/{self.name.lower()}.csv'
        if not path.exists('data'):
            mkdir('data')
        with open(filename, 'w') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerows(data)
