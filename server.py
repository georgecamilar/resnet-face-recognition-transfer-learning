import os

import flask
from flask import Flask
from flask import request, jsonify, redirect
from requests import Response

import neuralnet.networkUtils as utils
from app.Controller import Controller

app = Flask(__name__, static_folder='./static', template_folder='./templates')
controller = Controller()


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
            print('POST is executed')
            # check username and password
            username = request.form['username']
            password = request.form['password']
            canvas_image = request.form['canvas']
            file_name = username if username != '' else 'current'
            file_path = os.path.join(os.getcwd(), "utilityspace/" + file_name + ".jpeg")
            # create dir if it doesn't exist
            utils.create_dir_if_doesnt_exist(file_path)
            utils.save_image_from_image_data(image_data_string=canvas_image, directory=file_path)
            predicted_class = controller.get_prediction(image_path=file_path)
            print("This is the predicted class")
            print(predicted_class)
            # TODO if predicted class is admin, then redirect to admin html, otherwise, normal login page html
        except Exception as exception:
            print('Exception in image submit - get prediction. Message {message}'.format(message=str(exception)))
            return jsonify({
                'status': 'not ok',
                'code': '500'
            })
        utils.remove_image(image_path=file_path)
        return jsonify({
            'status': 'ok',
            'dataurl': canvas_image,
            'username': username,
            'password': password
        })

    return jsonify({'status': 'not ok'})


app.run(host="localhost", port=8080)
