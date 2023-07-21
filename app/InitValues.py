from app.controller import Controller
from neuralnet.FaceDetection import FaceCropper

faceCropper = FaceCropper()
DEFINED_BASE_PATH = "/Users/georgecamilar/Personal"

URL_PREFIX = "http://localhost:8080/"
HTML_SUFFIX = ".html"


class AppWrapper(object):
    def __init__(self):
        self.controller = Controller(DEFINED_BASE_PATH)
