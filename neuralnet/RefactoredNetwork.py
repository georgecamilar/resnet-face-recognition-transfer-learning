import sys

import tensorflow as tf
import os

import neuralnet.networkUtils

GIVEN_ERROR_IS_MESSAGE_TEMPLATE = "Cannot load network. If you do not have the trained model, run the training " \
                                  "script. Given error is: {message} "

# TODO can be changed with the [your_dir]/experiments/saved_model/resnet_saved
# SAVED_MODEL_PATH = "/Users/georgecamilar/Personal/licenta/notebooks/saved-models/resnet-saved"
SAVED_MODEL_PATH = "licenta/backup/resnet-saved"
DATASET_PATH = "ExtendedYaleB"
SAVE_NAME = "network_save.h5"


class FaceRecognitionNet(object):
    def __init__(self, base_path=None) -> None:
        if base_path is not None:
            try:
                self.base_path = base_path
                save_directory = os.path.join(neuralnet.networkUtils.HOME_DIRECTORY, 'saved')
                latest = neuralnet.networkUtils.latest_saved_model(save_directory)
                self.currentVersion = "version-" + str(latest)
                save_file = os.path.join(save_directory, self.currentVersion + "/" + SAVE_NAME)
                print(f"--- Save file used is: {save_file} ---")
                self.model = tf.keras.models.load_model(save_file)
                self.class_indices = self.get_dataset_classes()
            except Exception as e:
                error_message = GIVEN_ERROR_IS_MESSAGE_TEMPLATE.format(message=str(e))
                sys.exit(error_message)

    def predict(self, image_path):
        image = neuralnet.networkUtils.prepare_image_for_predict(image_path=image_path)
        prediction = self.model.predict(image)
        return prediction

    def create_dataset_generator(self, dataset_path):
        generator = tf.keras.preprocessing.image.ImageDataGenerator(height_shift_range=0.2, validation_split=0.2,
                                                                    preprocessing_function=tf.keras.applications.resnet50.preprocess_input, )
        train_data_gen = generator.flow_from_directory(dataset_path, target_size=(224, 224), batch_size=32,
                                                       shuffle=True, class_mode='categorical', subset='training', )

        validation_data_gen = generator.flow_from_directory(dataset_path, target_size=(224, 224), batch_size=32,
                                                            shuffle=True, class_mode='categorical', subset='validation')
        return train_data_gen, validation_data_gen, train_data_gen.class_indices

    def get_dataset_classes(self):
        generator = tf.keras.preprocessing.image.ImageDataGenerator()
        data = generator.flow_from_directory(os.path.join(self.base_path, DATASET_PATH), target_size=(224, 224))
        return data.class_indices
