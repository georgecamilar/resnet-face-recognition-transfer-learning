#!/usr/bin/env python3
import os

import flask
from flask import Flask
from flask import request, jsonify, redirect, flash
from requests import Response

import neuralnet.networkUtils as utils
from app.Controller import Controller
from neuralnet.FaceDetection import FaceCropper
from dropoutTraining.NeuralNetworkFactory import NeuralNetworkFactory

app = Flask(__name__, static_folder="./static", template_folder="./templates")
faceCropper = FaceCropper()
DEFINED_BASE_PATH = "/Users/georgecamilar/Personal"
controller = Controller(DEFINED_BASE_PATH)

URL_PREFIX = "http://localhost:8080/"
HTML_SUFFIX = ".html"


@app.route("/")
def redirect_to_index():
    return redirect("/index.html", code=302)


@app.route("/<path:name>")
def serve_static_files(name) -> Response:
    return flask.send_from_directory("./templates/", name)


@app.route("/submit", methods=["POST"])
def image_submit() -> Response:
    if request.method == "POST":
        file_path = ""
        try:
            username = request.form["username"]
            password = request.form["password"]
            canvas_image = request.form["canvas"]
            file_path = utils.create_photo_file(
                username=username, canvas_image=canvas_image
            )
            login_status = controller.login(username, password, file_path)
        except Exception as exception:
            print(
                "Exception in image submit - get prediction. Message {message}".format(
                    message=str(exception)
                )
            )
            return jsonify({"status": "not ok", "code": "403"})
        finally:
            if file_path != "":
                utils.remove_image(image_path=file_path)
        # Make it redirect to the page
        # return redirect(getIndexPageUrl(login_status))
        location_addr = get_index_page_url(login_status)
        return jsonify(
            {
                "status": login_status,
                "dataurl": canvas_image,
                "username": username,
                "htmlcode": redirect(location_addr),
                "location": location_addr,
                "password": password,
            }
        )

    return jsonify({"status": "not ok"})


def get_index_page_url(status):
    if status == "admin":
        return URL_PREFIX + "admin" + HTML_SUFFIX
    else:
        return URL_PREFIX + "user" + HTML_SUFFIX


@app.route("/test/facerequest", methods=["POST"])
def evaluate_image() -> Response:
    if request.method == "POST":
        try:
            canvas_image = request.form["canvas"]
            file_path = utils.create_photo_file(
                username="test_photo", canvas_image=canvas_image
            )
            # indices are probabilities
            # values are the classes of the respective probabilities
            p_indices, p_values = controller.get_all_predictions_and_percentages(
                image_path=file_path
            )
            utils.remove_image(image_path=file_path)
            values = utils.filter_probabilities(
                p_indices.numpy().tolist()[0],
                p_values.numpy().tolist()[0],
                controller.network.class_indices,
            )
            return jsonify(create_response_body(status_string="ok", classes=values))
        except Exception as ex:
            return jsonify(create_response_body("Exception occured", []))


def create_response_body(status_string, classes):
    return {"status": status_string, "classes": classes}


@app.route("/app/newsubject", methods=["POST"])
def upload_photos() -> Response:
    if request.method == "POST":
        if "file" not in request.files:
            flash("No files added")
            return jsonify({"status": "not ok"})

    return jsonify({"status": "ok"})


@app.route("/app/uploadVideo", methods=["POST"])
def add_photos_to_dataset() -> Response:
    """
        Steps:
        * video found
        * save video to local storage temporary folder
        * get dataset path
        * get faces from video
        * save to dataset
    """
    try:
        if request.method == "POST":
            # read request values
            subject_name = (
                request.form.get("name")
                if request.form.get("name") is not None
                else "new"
            )
            print(subject_name)
            if request.files.get("video") is not None:
                video_file_path = utils.create_video_file(
                    name=subject_name, video_blob=request.files.get("video")
                )
                # create new dataset directory for the new subject
                dataset_path = utils.DATASET_DIRECTORY
                save_target_directory = os.path.join(dataset_path, subject_name)
                print("Writing to directory" + save_target_directory)
                utils.create_dir_if_doesnt_exist(save_target_directory)

                faceCropper.crop_faces_from_video(
                    video_path=video_file_path,
                    output_directory=save_target_directory,
                )

                neural_net_factory = NeuralNetworkFactory(utils.DATASET_DIRECTORY)
                utils.remove_image(video_file_path)
            return jsonify(
                create_response_body(status_string="post executed", classes=[])
            )
    except Exception as ex:
        print(str(ex))
        return jsonify(create_response_body(status_string="not post", classes=[]))


app.run(host="localhost", port=8080)
