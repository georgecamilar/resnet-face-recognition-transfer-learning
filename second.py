from dropoutTraining.NeuralNetworkFactory import *
from neuralnet.networkUtils import *

if __name__ == "__main__":
    save_directory = os.path.join(HOME_DIRECTORY, 'saved')
    name = latest_saved_model(save_directory)
    path = os.path.join(save_directory, name)
    print(path)