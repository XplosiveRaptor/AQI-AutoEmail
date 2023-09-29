#   AQI-AutoEmail is a Python script to automatically send an email alert that the AQI flag should be changed.
#   Copyright (C) 2023  Donovan James
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.

import smtplib
import requests
import math
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime

# Replace with your own AirNow API key (sign up at https://www.airnowapi.org/)
api_key = ""

# Replace with your Gmail email and password
sender_email = ""
sender_password = ""

# Recipient email address
recipient_email = ""

# Email tail
email_signature = "\n\nThis email was sent automatically by a script hosted by \{Your Name\}.\nFor questions please contact \{Your Email\}"

# Replace with location for your city
# This is the White House
latitude = 38.8979
longitude = -77.0366

# Categorize an AQI into categories - 0 is Green, 1 is Yellow, etc
def categorize_quality(air_quality):
    air_quality - (air_quality % 50)
    return math.floor(air_quality / 50)

# Turn a category into a flag color
def colorize_category(category):
    if category == 0: return "Green"
    if category == 1: return "Yellow"
    if category == 2: return "Orange"
    if category == 3: return "Red"
    if category == 4: return "Purple"
    if category >= 5: return "Maroon"
    

# Specify the AirNow API endpoint
api_url = f"https://www.airnowapi.org/aq/observation/latLong/current/?format=application/json&latitude={latitude}&longitude={longitude}&distance=25&API_KEY={api_key}"

# Function to send an email
def send_email(subject, body):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, recipient_email, msg.as_string())
    server.quit()

# Initialize the previous AQI category
prev_aqi_category = 3

# Initialize last email send date
prev_email = datetime.date.today()- datetime.timedelta(1)

# If it is a different day than last send date
if(datetime.date.today() > prev_email):
    try:
        # Send a GET request to the AirNow API
        response = requests.get(api_url)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()

            # Ensure there is at least one data point
            if len(data) > 0:
                # Extract the AQI value
                aqi = data[0]["AQI"]
                aqi_category = categorize_quality(aqi)

                # Check if there is a change in AQI category
                if prev_aqi_category is not None and (aqi_category != prev_aqi_category):
                    subject = "Air Quality Alert"
                    body = f"Today's date: {datetime.date.today()}\n\nThe Air Quality Index (AQI) in Mission Viejo has changed.\nCurrent AQI: {aqi}\nA {colorize_category(aqi_category)} flag should be flown.{email_signature}"
                    send_email(subject, body)
                    print("Email sent: Air quality change alert!")

                prev_aqi_category = aqi_category
                prev_email = datetime.date.today()

                print(f"Current AQI: {aqi}")

        else:
            print("Error: Unable to retrieve air quality data.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

print("All done!")
