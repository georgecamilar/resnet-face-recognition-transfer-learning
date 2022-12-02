#!/usr/bin/env python3

import flask
from flask import Flask
from flask import request, jsonify, redirect
from requests import Response

import neuralnet.networkUtils as utils
from app.Controller import Controller

app = Flask(__name__, static_folder='./static', template_folder='./templates')
controller = Controller()
URL_PREFIX = 'http://localhost:8080/'
HTML_SUFFIX = '.html'


@app.route("/")
def redirect_to_index():
    return redirect("/index.html", code=302)


@app.route('/<path:name>')
def serve_static_files(name) -> Response:
    return flask.send_from_directory('./templates/', name)


@app.route('/submit', methods=['POST'])
def image_submit() -> Response:
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            canvas_image = request.form['canvas']
            file_path = utils.create_photo_file(
                username=username, canvas_image=canvas_image)
            login_status = controller.login(username, password, file_path)
        except Exception as exception:
            print(
                'Exception in image submit - get prediction. Message {message}'.format(message=str(exception)))
            return jsonify({
                'status': 'not ok',
                'code': '403'
            })
        utils.remove_image(image_path=file_path)
        # Make it redirect to the page
        # return redirect(getIndexPageUrl(login_status))
        location_addr = getIndexPageUrl(login_status)
        return jsonify({
            'status': login_status,
            'dataurl': canvas_image,
            'username': username,
            'htmlcode': redirect(location_addr),
            'location': location_addr,
            'password': password
        })

    return jsonify({'status': 'not ok'})


def getIndexPageUrl(status):
    if(status == 'admin'):
        return URL_PREFIX + 'admin' + HTML_SUFFIX
    else:
        return URL_PREFIX + 'user' + HTML_SUFFIX


@app.route('/test/facerequest', methods=['POST'])
def evaluate_image() -> Response:
    if request.method == 'POST':
        try:
            canvas_image = request.form['canvas']
            file_path = utils.create_photo_file(
                username='test_photo', canvas_image=canvas_image)
            prediction_name = controller.get_prediction(file_path)
            utils.remove_image(image_path=file_path)
            return jsonify({"responseValue": prediction_name})
        except Exception as ex:
            print(ex)
    return jsonify({'responseValue': 'Internal Error'})


app.run(host="localhost", port=8080)
