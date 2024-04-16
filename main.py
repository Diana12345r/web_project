from flask import Flask, url_for, request
import requests

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    with open('design.html', 'r', encoding='utf-8') as html_stream:
        html = html_stream.read()
    if request.method == "GET":
        return html
    elif request.method == 'POST':
        f = request.files['file']
        print(f.read())
        return "Форма отправлена"


if __name__ == '__main__':
    app.run(port=8000, debug=True)


print('hi')