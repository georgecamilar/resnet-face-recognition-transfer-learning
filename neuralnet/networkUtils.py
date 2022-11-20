import tensorflow as tf
import numpy as np
from binascii import a2b_base64
import os

DATASET_DIRECTORY = '/Users/georgecamilar/Documents/ExtendedYaleB'


# Network Utils

def prepare_image_for_predict(image_path):
    img = tf.keras.utils.load_img(image_path, target_size=(224, 224))
    img_tensor = tf.keras.preprocessing.image.img_to_array(img)
    img_array_expanded_dims = np.expand_dims(img_tensor, axis=0)
    preprocessed = tf.keras.applications.resnet50.preprocess_input(img_array_expanded_dims)
    return preprocessed


def get_classes_dict():
    # create generator to load images and get mappings for images and classes to dictionary
    generator = tf.keras.preprocessing.image.ImageDataGenerator()
    data = generator.flow_from_directory(DATASET_DIRECTORY, target_size=(224, 224))
    return data.class_indices


def get_prediction_id(predicted_class_number):
    for key, value in get_classes_dict().items():
        if value == predicted_class_number:
            return key
    print("Network predicted a number that doesn't exist")
    return -1


# File work utils

def save_image_from_image_data(image_data_string, directory):
    image_data_array = image_data_string.split('base64,')
    if len(image_data_array) <= 1:
        return
    binary_data = a2b_base64(image_data_array[1])
    print('Current path of writing the image is {}\n'.format(directory))
    fh = open(directory, 'wb')
    fh.write(binary_data)
    fh.close()


def remove_image(image_path):
    if os.path.exists(image_path):
        os.remove(image_path)


def get_top_k_results(prediction):
    return np.argmax(prediction, axis=1)


def create_dir_if_doesnt_exist(dir_path):
    if os.path.isdir(dir_path):
        os.makedirs(dir_path)


def create_photo_file(username, canvas_image):
    file_name = username if username != '' else 'current'
    file_path = os.path.join(os.getcwd(), "utilityspace/" + file_name + ".jpeg")
    create_dir_if_doesnt_exist(file_path)
    save_image_from_image_data(image_data_string=canvas_image, directory=file_path)
    return file_path
