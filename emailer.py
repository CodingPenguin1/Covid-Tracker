#!/usr/bin/env python3
import json
import smtplib
from datetime import date
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from os.path import basename

from tabulate import tabulate

from County import County
from generate_plots import *
from update_database import *

gmail_user, gmail_password = '', ''


def _authenticate(file='credentials.json'):
    with open(file, 'r') as f:
        contents = '\n'.join(f.readlines())
        credentials = json.loads(contents)
        return credentials['email'], credentials['password']


if __name__ == '__main__':
    # Update database
    update_database()

    # Login
    gmail_user, gmail_password = _authenticate()
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)

    # Read list of users to email
    with open('recipients.json', 'r') as f:
        contents = '\n'.join(f.readlines())
        recipients = json.loads(contents)

    for recipient in recipients.keys():
        counties = sorted(recipients[recipient]['counties'])
        subject = 'COVID-19 Statistics: ' + ', '.join(_[:_.find(', ')] for _ in counties)

        # Recent stats
        county_names = [date.today().strftime('%B %d %Y')]
        data = [['New cases'],
                ['Total cases']]
        plot_filepaths = []
        for county in counties:
            name, state = county.split(', ')
            county_names.append(name)
            county_tracker = County(name, state)
            data[0].append(county_tracker.new_per_day[-1])
            data[1].append(county_tracker.cases[-1])

            # Plots
            plot_filepaths.append(generate_plot(county_tracker, 'cases, new'))
        table = tabulate(data, county_names, tablefmt='simple')

        # Create and send email
        msg = MIMEMultipart()
        msg['From'] = gmail_user
        msg['To'] = recipient
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = subject
        msg.attach(MIMEText(table))
        for path in plot_filepaths:
            with open(path, 'rb') as f:
                part = MIMEApplication(f.read(), Name=basename(path))
            part['Content-Disposition'] = 'attachment; filename="%s' % basename(path)
            msg.attach(part)
        server.sendmail(gmail_user, recipients[recipient]['email_address'], msg.as_string())
        print(f'Sent mail to {recipient}')

    server.close()
