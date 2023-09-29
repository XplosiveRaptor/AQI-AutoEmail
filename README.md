# AQI-AutoEmail
This is a Pyhon Script that automatically sends an email to indicate that an Air Quality Index (AQI) flag should be changed.
To run this, the following are required: 
* a gmail address
* an app password for this script from the gmail account
* an AirNow API key (sign up at https://www.airnowapi.org/) 
* the longitude and latitude of the desired location
Input these where the comments indicate in the code.

The default email looks like this:
-------------------------------------------------
Subject: Air Quality Alert

Today's date: 0000-00-00

The Air Quality Index (AQI) in CITY has changed.
Current AQI: 0
A COLOR flag should be flown.

This email was sent automatically by a script hosted by YOUR NAME.
For questions please contact YOUR EMAIL
-------------------------------------------------
