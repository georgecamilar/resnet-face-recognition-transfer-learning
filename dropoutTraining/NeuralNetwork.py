import tensorflow as tf
from neuralnet.networkUtils import *


class FaceRecognitionNet:
    def __init__(self, path):
        self.net = tf.keras.models.load_model(path)

    def make_prediction(self, image_path):
        image = prepare_image_for_predict(image_path=image_path)
        prediction = self.net.predict(image)
        return prediction
