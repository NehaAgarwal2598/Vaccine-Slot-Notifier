import datetime
import time
import requests
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys
import pytz
import config




def send_curl_request(district_id):
    url = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict?'
    headers = {
        'authority': 'cdn-api.co-vin.in',
        'accept': 'application/json, text/plain, */*',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,fr;q=0.7',
    }

    date_today = datetime.date.today()
    formatted_date = datetime.date.strftime(date_today, "%d-%m-%Y")

    p = (('district_id', district_id), ('date', formatted_date))
    response = requests.get(url, headers=headers, params=p)

    return response




def sendEmail(body):

    url = "https://selfregistration.cowin.gov.in/"
    to, From, subject = sys.argv[2], 'vaccine.no.reply.notifier@gmail.com', 'Vaccine Slot Availability'
    username, password = config.username, config.password

    message = MIMEMultipart()
    message['From'] = From
    message['To'] = to
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain', 'UTF-8'))

    html = "<a href ='" + \
        url + "'>Click here to visit.</a>"
    message.attach(MIMEText(html, "html"))

    smtpSession = SMTP('smtp.gmail.com', 587)
    smtpSession.starttls()
    smtpSession.login(username, password)
    smtpSession.send_message(message, username, to)
    smtpSession.quit()
    print(str(datetime.datetime.now()) + ' Alert sent!!!')




while(1):
    try:
        i = sys.argv[1]
        response = send_curl_request(i)
        data = response.json()
        body = 'Hey there is a vaccine slot available please login and book as soon as possible'
        for j in data["centers"]:
            available_capacity = j["sessions"][0]["available_capacity"]
            age = j["sessions"][0]["min_age_limit"]
            if available_capacity > 0 and age == 18:
                body += "\nName - " + str(j["name"]) + "\n\t Address1 - " + str(j["address"]) + \
                    "\n\tAddress2 - " + str(j["block_name"]) + \
                    "\n\tPincode - " + str(j["pincode"]) + "\tSlots - " + str(
                        available_capacity) + "-\t Date- " + str(j["sessions"][0]["date"]) + "-\t" + str(j["sessions"][0]["vaccine"]) + "\n"
                sendEmail(body)

        print(str(datetime.datetime.now(pytz.timezone('Asia/Calcutta'))) + " (" + str(response.status_code) + " " + str(response.reason) + ")  No Slots available at " +
              i + "!! Waiting for 3secs before sending the request")
        time.sleep(3)
    except:
        print(str(datetime.datetime.now()) + " (" +
              str(response.status_code) + ") " + str(response.reason))

        time.sleep(2)
        continue
