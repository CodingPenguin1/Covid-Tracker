import csv
import json
from os import mkdir, path

from bs4 import BeautifulSoup

from update_database import *


class County:
    def __init__(self, name, state):
        self.name = name
        self.state = state

        self.dates = []
        self.cases = []
        self.deaths = []
        self.new_per_day = []

        self.update_data()

    def update_data(self):
        # Load data from CSV
        csv_data = self.load_csv()

        for date in csv_data:
            self.dates.append(date[0])
            self.cases.append(int(date[4]))
            self.deaths.append(int(date[5]))

        # Create new cases per day list
        self.new_per_day = [0]
        for i in range(1, len(self.cases)):
            self.new_per_day.append(self.cases[i] - self.cases[i - 1])

    def load_csv(self):
        filename = 'data.csv'
        if not path.exists(filename):
            update_database()

        with open(filename, 'r') as f:
            csv_data = csv.reader(f)

            county_data = []
            for line in csv_data:
                if self.name.lower() == line[1].lower() and self.state.lower() == line[2].lower():
                    county_data.append(line)
            return county_data


if __name__ == '__main__':
    c = County('greene', 'ohio')
    for i in range(len(c.dates)):
        print(c.dates[i], c.cases[i], c.new_per_day[i], c.deaths[i])
