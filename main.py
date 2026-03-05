import requests
from twilio.rest import Client
import os

OWM_ENDPOINT_URL = "http://api.openweathermap.org/data/2.5/forecast"

WEATHER_PARAMS = {
    "lat": 19.0308262,
    "lon": 73.0198537,
    "cnt": 4,
    "appid": os.environ.get("OWM_API_KEY")
}

# ------------------ Twilio Config ------------------ #
ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
AUTH_TOKEN  = os.environ.get("TWILIO_AUTH_TOKEN")
FROM_NUMBER = os.environ.get("TWILIO_FROM_NUMBER")   # +14342165557
TO_NUMBER   = os.environ.get("TWILIO_TO_NUMBER")     # +918290884698

# ------------------ Weather Fetch ------------------ #
response = requests.get(OWM_ENDPOINT_URL, params=WEATHER_PARAMS)
response.raise_for_status()
data = response.json()

current_temp = round(data["list"][0]["main"]["temp"] - 273.15, 2)
humidity     = data["list"][0]["main"]["humidity"]
cond_code    = data["list"][0]["weather"][0]["id"]
description  = data["list"][0]["weather"][0]["description"]

print(f"Current temp : {current_temp}°C")
print(f"Humidity     : {humidity}%")
print(f"Condition id : {cond_code}")
print(f"Description  : {description}")

# ------------------ Rain Check ------------------ #
will_rainfall = any(int(h["weather"][0]["id"]) < 700 for h in data["list"])

if will_rainfall:
    print("Bring an umbrella!")
    client = Client(ACCOUNT_SID, AUTH_TOKEN)

    # SMS
    sms = client.messages.create(
        body="🌧️ It's going to rain in Navi Mumbai! Bring an umbrella!",
        from_=FROM_NUMBER,
        to=TO_NUMBER,
    )
    print(f"SMS sent     : {sms.sid}")

    # WhatsApp
    wa = client.messages.create(
        from_=f"whatsapp:{FROM_NUMBER}",
        body="🌧️ It's going to rain in Navi Mumbai! Bring an umbrella!",
        to=f"whatsapp:{TO_NUMBER}",
    )
    print(f"WhatsApp sent: {wa.sid}")

else:
    print(f"No rain expected — {description}!")
