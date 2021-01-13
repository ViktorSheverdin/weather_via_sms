import requests
import credentials
import os
from twilio.rest import Client

MY_LAT = "49.285061"
MY_LNG = "-122.794594"

params = {
    "lon": MY_LNG,
    "lat": MY_LAT,
    "appid": credentials.api_key,
    "exclude": "current,minutely,daily,alerts"
}


def get_data():
    response = requests.get(
        url="https://api.openweathermap.org/data/2.5/onecall", params=params)
    response.raise_for_status()
    # print(response.json()["hourly"][0])
    return response.json()["hourly"][0:12]


def bring_umbrella_check():
    weather = get_data()
    for weather_condition in range(len(weather)):
        if int(weather[weather_condition]["weather"][0]["id"]) < 700:
            # print("Bring umbrella")
            return True
            break


def send_text():
    if bring_umbrella_check():
        client = Client(credentials.twilo_account_sid,
                        credentials.twilo_auth_token)

        message = client.messages.create(
            body="Bring Umbrella",
            from_=credentials.twilo_phone_num,
            to=credentials.my_phone_num
        )

        print(message.sid)
        # print("Bring Umbrella")


def main():
    send_text()


main()
