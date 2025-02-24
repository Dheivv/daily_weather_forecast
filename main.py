import requests
from twilio.rest import Client
import smtplib
from email.message import EmailMessage
import os
# import dotenv

# load files with ENV variables
# dotenv.load_dotenv(dotenv_path='C:/Users/mcato/100 Days Of Code/Day 35/rain_alert_project/config.env')

# twilio credentials to send sms with weather forecast
TWILIO_SID = os.getenv('TWILIO_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')

# smtplib credentials to send email in case twilio doesn't work
EMAIL = 'davidecatozzi0@gmail.com'
APP_PASSWORD = os.getenv('PYTHON_APP_PASSWORD')

# openweather api endpoint to retrieve weather data and credentials
API_ENDPOINT = 'https://api.openweathermap.org/data/2.5/forecast'
API_KEY = os.getenv('OPEN_WEATHER_API_KEY')

# lat and long coordinates for Senigallia, Italy, AN
LAT = 43.715014
LONG = 13.218024

weather_params = {
    'lat': LAT,
    'lon': LONG,
    'appid': API_KEY,
    'cnt': '5',
}

res = requests.get(API_ENDPOINT, params=weather_params)
res.raise_for_status()
weather_data = res.json()

msg_list = []
for hour_data in weather_data['list']:
    condition_code = hour_data['weather'][0]['id']
    dt_txt_hour = str(hour_data['dt_txt'].split(' ')[1].split(':')[0]) + ':' + str(hour_data['dt_txt'].split(' ')[1].split(':')[1])
    # print(f'Per le ore {dt_txt_hour} il codice è: {condition_code}')

    if 200 <= int(condition_code) < 240:
        forecast = f'Tempesta ⛈️  prevista dalle {dt_txt_hour}UTC (codice {condition_code})'
        msg_list.append(forecast)

    if 300 <= int(condition_code) < 330:
        forecast = f'Pioggerella 🌦️  prevista dalle {dt_txt_hour}UTC (codice {condition_code})'
        msg_list.append(forecast)

    if 500 <= int(condition_code) < 540:
        forecast = f'Pioggia 🌧️  prevista dalle {dt_txt_hour}UTC (codice {condition_code})'
        msg_list.append(forecast)

    if 600 <= int(condition_code) < 630:
        forecast = f'Neve ❄️  prevista dalle {dt_txt_hour}UTC (codice {condition_code})'
        msg_list.append(forecast)

    if int(condition_code) == 701 or int(condition_code) == 741:
        forecast = f'Nebbia 🌫️  prevista per le {dt_txt_hour}UTC (codice {condition_code})'
        msg_list.append(forecast)

    if int(condition_code) == 800:
        forecast = f'Tempo sereno ☀️  previsto per le {dt_txt_hour}UTC (codice {condition_code})'
        msg_list.append(forecast)

    if 801 <= int(condition_code) <= 804:
        forecast = f'Nuvole sparse 🌤️  previste per le {dt_txt_hour}UTC (codice {condition_code})'
        msg_list.append(forecast)

header = 'Ecco le previsioni di oggi:\n'
body_msg = ''
for msg, i in zip(msg_list, range(0, len(msg_list))):
    if i < len(msg_list) - 1: 
        body_msg += msg + ';\n'
    else:
        body_msg += msg + '.'
full_msg = header + body_msg

if full_msg:
    try:
        client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            from_='whatsapp:+14155238886',
            body=full_msg,
            to='whatsapp:+393271465724',
        )

    except:
        email = EmailMessage()
        email.set_content(full_msg + "\n\n(Hai ricevuto questa email perché ci sono stati dei problemi nell'invio con Twilio)")
        email['Subject'] = 'Le previsioni di oggi'
        email['From'] = EMAIL 
        email['To'] = EMAIL

        connection = smtplib.SMTP('smtp.gmail.com')
        connection.starttls()
        connection.login(EMAIL, APP_PASSWORD)
        connection.send_message(email)
