from app.Repository import AppRepository
from neuralnet.RefactoredNetwork import FaceRecognitionNet
import neuralnet.networkUtils as utils


class Controller(object):
    def __init__(self):
        self.repository = AppRepository()
        self.network = FaceRecognitionNet()

    def get_prediction(self, image_path):
        # For now, it prints the prediction, but it should return it and
        # work with the simple login algorithm to authenticate or not
        prediction_tensor = self.network.predict(image_path)
        identity_predictions = utils.get_top_k_results(prediction_tensor)
        for identity in identity_predictions:
            prediction_id = utils.get_prediction_id(identity)
            if prediction_id != -1:
                return prediction_id

        raise Exception("Cannot find user")