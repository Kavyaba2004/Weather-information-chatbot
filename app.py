from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Replace with your OpenWeatherMap API key
API_KEY = "2cc7aa96de2504384f84fdaa275b014f"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get_weather", methods=["POST"])
def get_weather():
    city = request.json.get("city", "")
    if not city:
        return jsonify({"message": "Please provide a city name."})

    try:
        # Construct the API URL
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={API_KEY}"
        
        # Make the API request
        response = requests.get(url)
        response.raise_for_status()
        
        # Get JSON data from the API response
        data = response.json()

        # Check if city is valid
        if response.status_code == 404:
            return jsonify({"message": f"City '{city}' not found. Please try again."})

        # Extract weather info and format the message
        message = (
            f"The current weather in {data['name']} is {data['main']['temp']}°C "
            f"with {data['weather'][0]['description']}."
        )
        return jsonify({"message": message})

    except requests.exceptions.RequestException as e:
        # Handle errors during the request
        return jsonify({"message": "Could not fetch weather information. Check the city name or try again later."})


if __name__ == "__main__":
    app.run(debug=True)
