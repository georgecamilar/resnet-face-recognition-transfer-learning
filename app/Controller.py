from app.Repository import AppRepository
from neuralnet.RefactoredNetwork import FaceRecognitionNet
import neuralnet.networkUtils as utils
from app.CustomException import AppException
import os

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

    def get_username_from_prediction(self, prediction):
        default_answer = 'unknown'
        try:
            candidates = self.repository.search_by_prediction_name(prediction=prediction)
            for result in candidates:
                return result[1] if result[1] is not None and result[1] != '' else default_answer
        except Exception as ex:
            print('Error happened in:')
            print(os.path.abspath(__file__), ex)
            return default_answer

    def login(self, username, password, image_file_path):
        predicted_class = self.get_prediction(image_path=image_file_path)
        response_list = self.repository.search_by_username(username)
        for candidate in response_list:
            print('Candidate is:')
            print(candidate)
            if username == candidate[1] and password == candidate[2] and predicted_class == candidate[3]:
                login_status = candidate[4] if candidate[4] is not None else 'user'
                return login_status
        raise Exception("Login credentials are wrong")
