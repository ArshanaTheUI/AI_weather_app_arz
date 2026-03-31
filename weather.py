from flask import Blueprint, jsonify, request
import requests
from tensorflow.keras.models import load_model
import numpy as np

weather = Blueprint("weather", __name__)

API_KEY = "057b843e471725429410a7b2e0fc567f"

# ✅ Load LSTM model
lstm_model = load_model("lstm_model.h5", compile=False)

# 🔍 City-based weather
@weather.route("/weather", methods=["POST"])
def get_weather():
    data = request.json
    city = data["city"]

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    res = requests.get(url)
    weather_data = res.json()

    if "main" not in weather_data:
        return jsonify({"error": weather_data})

    temp = weather_data["main"]["temp"]
    condition = weather_data["weather"][0]["main"]
    city_name = weather_data["name"]

    if temp > 35:
        suggestion = "Too hot! Stay hydrated 🥵"
    elif temp < 20:
        suggestion = "Cold! Wear jacket 🧥"
    else:
        suggestion = "Nice weather 🌤️"

    return jsonify({
        "temperature": temp,
        "condition": condition,
        "city": city_name,
        "suggestion": suggestion
    })


# 📍 Location-based weather
@weather.route("/weather-by-coords", methods=["POST"])
def weather_by_coords():
    data = request.json
    lat = data["lat"]
    lon = data["lon"]

    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"

    res = requests.get(url)
    weather_data = res.json()

    if "main" not in weather_data:
        return jsonify({"error": weather_data})

    temp = weather_data["main"]["temp"]
    condition = weather_data["weather"][0]["main"]
    city_name = weather_data["name"]

    if temp > 35:
        suggestion = "Too hot! Stay hydrated 🥵"
    elif temp < 20:
        suggestion = "Cold! Wear jacket 🧥"
    else:
        suggestion = "Nice weather 🌤️"

    return jsonify({
        "temperature": temp,
        "condition": condition,
        "city": city_name,
        "suggestion": suggestion
    })


# 🤖 LSTM Prediction API (FIXED POSITION)
@weather.route("/predict-lstm", methods=["POST"])
def predict_lstm():
    data = request.json
    temps = data["temps"]

    if len(temps) < 3:
        return jsonify({"predicted_temp": temps[-1]})

    last = temps[-3:]

    X = np.array(last).reshape((1, 3, 1))

    prediction = lstm_model.predict(X)

    return jsonify({
        "predicted_temp": round(float(prediction[0][0]), 2)
    })