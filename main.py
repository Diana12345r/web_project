from flask import Flask, url_for, request, render_template
import requests
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)


search_api_server = "https://search-maps.yandex.ru/v1/"
api_key = "3693258b-1cf0-4c9d-8aa5-e6e2d34ff45b"
address_ll = "37.588392,55.734036"


#  Находим координаты для поиска
def coords(city, metro):
    city = city
    metro = metro
    toponym_to_find = f'{city}, метро {metro}'

    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        "format": "json"}
    # Запрос
    response = requests.get(geocoder_api_server, params=geocoder_params)

    if not response:
        print('Попробуйте еще раз')
    # Преобразуем ответ в json-объект
    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    toponym_coodrinates = toponym["Point"]['pos']
    toponym_longitude = ','.join(toponym_coodrinates.split(" "))
    return toponym_longitude


@app.route('/index', methods=['POST', 'GET'])
@app.route("/", methods=['POST', 'GET'])
def index():
    # Главная страница
    if request.method == 'GET':
        return render_template('index.html', list_place=[])
    elif request.method == 'POST':
        about = request.form['about']
        city = request.form['city']
        metro = request.form['metro']
        search_params = {
            "apikey": api_key,
            "text": about,
            "lang": "ru_RU",
            "ll": coords(city, metro),
            "type": "biz"
        }

        response = requests.get(search_api_server, params=search_params)
        if not response:
            return "Попробуйте еще раз"

        json_response = response.json()

        # Получаем первые 10 организаций

        organization = json_response["features"][0:11]
        organizations = []
        # Название организации.
        print(organization)
        for org in organization:
            org_name = org["properties"]["CompanyMetaData"]["name"]
            if "url" in org["properties"]["CompanyMetaData"]:
                org_url = org["properties"]["CompanyMetaData"]["url"]
                organizations.append(f"{org_name}: {org_url}")
            else:
                organizations.append(org_name)
        organizations = list(set(organizations))  # Убираем повторения
        return render_template('rez.html', list_place=organizations)


@app.route('/login', methods=['POST', 'GET'])
# страница для регистрации
def login():
    if request.method == 'GET':
        return render_template('sing_in.html')
    elif request.method == 'POST':
        print(request.form['email'])
        print(request.form['password'])
        return render_template('sing_in.html')


@app.route('/sing-up', methods=['POST', 'GET'])
# страница для входа
def sing_up():
    if request.method == 'GET':
        return render_template('test.html')
    elif request.method == 'POST':
        print(request.form['email'])
        print(request.form['password'])
        print(request.form['file'])
        print(request.form['sex'])
        return render_template('test.html')


if __name__ == '__main__':
    app.run(port=8080, debug=True)
