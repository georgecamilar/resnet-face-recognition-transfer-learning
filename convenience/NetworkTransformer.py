from neuralnet.RefactoredNetwork import FaceRecognitionNet



network_model = FaceRecognitionNet()

json_model = network_model.model.to_json()

