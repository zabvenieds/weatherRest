from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Ваш API ключ от OpenWeatherMap
API_KEY = "bae48b44c59647b067d3965f54ac777d"
BASE_URL = "http://api.openweathermap.org/data/2.5/air_pollution"

# JSON схема для валидации ответа
JSON_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "list": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "aqi": { "type": "integer" },
                    "co": { "type": "number" },
                    "no": { "type": "number" },
                    "no2": { "type": "number" },
                    "o3": { "type": "number" },
                    "so2": { "type": "number" },
                    "pm2_5": { "type": "number" },
                    "pm10": { "type": "number" },
                    "nh3": { "type": "number" }
                },
                "additionalProperties": False,
                "required": ["aqi", "co", "no", "no2", "o3", "so2", "pm2_5", "pm10", "nh3"]
            }
        }
    },
    "minProperties": 1,
    "additionalProperties": False,
    "definitions": {}
}

def fetch_air_pollution_data(lat, lon):
    """Функция для получения данных о загрязнении воздуха."""
    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Ошибка при запросе к API: {response.status_code}")

def transform_data(data):
    """Функция для преобразования данных в нужный формат."""
    transformed = {
        "list": []
    }
    for item in data.get("list", []):
        transformed_item = {
            "aqi": item["main"]["aqi"],
            "co": item["components"]["co"],
            "no": item["components"]["no"],
            "no2": item["components"]["no2"],
            "o3": item["components"]["o3"],
            "so2": item["components"]["so2"],
            "pm2_5": item["components"]["pm2_5"],
            "pm10": item["components"]["pm10"],
            "nh3": item["components"]["nh3"]
        }
        transformed["list"].append(transformed_item)
    return transformed

@app.route('/air-pollution', methods=['GET'])
def get_air_pollution():
    """Эндпоинт для получения данных о загрязнении воздуха."""
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)

    if not lat or not lon:
        return jsonify({"error": "Необходимо указать параметры lat и lon"}), 400

    try:
        # Получаем данные от OpenWeatherMap
        data = fetch_air_pollution_data(lat, lon)
        # Преобразуем данные в нужный формат
        transformed_data = transform_data(data)
        # Возвращаем данные в формате JSON
        return jsonify(transformed_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)