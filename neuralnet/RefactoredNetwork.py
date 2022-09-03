import sys

import tensorflow as tf

import neuralnet.networkUtils

GIVEN_ERROR_IS_MESSAGE_TEMPLATE = "Cannot load network. If you do not have the trained model, run the training " \
                                  "script. Given error is: {message} "

# TODO can be changed with the [your_dir]/experiments/saved_model/resnet_saved
SAVED_MODEL_PATH = "/Users/georgecamilar/Documents/licenta/notebooks/saved-models/resnet-saved"


class FaceRecognitionNet(object):
    def __init__(self) -> None:
        try:
            self.model = tf.keras.models.load_model(SAVED_MODEL_PATH)
            self.model.summary()
        except Exception as e:
            error_message = GIVEN_ERROR_IS_MESSAGE_TEMPLATE.format(message=str(e))
            sys.exit(error_message)

    def predict(self, image_path):
        image = neuralnet.networkUtils.prepare_image_for_predict(image_path=image_path)
        prediction = self.model.predict(image)
        return prediction
