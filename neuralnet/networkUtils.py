import tensorflow as tf
from tensorflow import keras
import numpy as np
import json

from binascii import a2b_base64
import os

DATASET_DIRECTORY = '/Users/georgecamilar/Personal/ExtendedYaleB'
HOME_DIRECTORY = '/Users/georgecamilar/Personal/licenta/experiments'


# Network Utils

def prepare_image_for_predict(image_path):
    img = tf.keras.utils.load_img(image_path, target_size=(224, 224))
    img_tensor = tf.keras.preprocessing.image.img_to_array(img)
    img_array_expanded_dims = np.expand_dims(img_tensor, axis=0)
    preprocessed = tf.keras.applications.resnet50.preprocess_input(
        img_array_expanded_dims)
    return preprocessed


def get_classes_dict():
    # create generator to load images and get mappings for images and classes to dictionary
    generator = tf.keras.preprocessing.image.ImageDataGenerator()
    data = generator.flow_from_directory(
        DATASET_DIRECTORY, target_size=(224, 224))
    return data.class_indices


def read_train_classes():
    with open("train_classes.json") as classes_handle:
        data = json.load(classes_handle)
        return data


def get_prediction_id(predicted_class_number, dataset_classes=None):
    if dataset_classes is None:
        dataset_classes = read_train_classes()
    for key, value in dataset_classes.items():
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


def save_video_from_blob(blob, path):
    pass


def remove_image(image_path):
    if os.path.exists(image_path):
        os.remove(image_path)


def get_top_k_results(prediction):
    return np.argmax(prediction, axis=1)


def get_top_k_result_classes(prediction_tensor):
    return tf.math.top_k(prediction_tensor, k=10, sorted=True)


def create_dir_if_doesnt_exist(dir_path):
    if not os.path.isdir(dir_path):
        print('dir does not exist, so we create it.')
        print('dir path ' + dir_path)
        os.makedirs(dir_path)


def create_photo_file(username, canvas_image):
    file_name = username if username != '' else 'current'
    file_path = os.path.join(
        os.getcwd(), "utilityspace/" + file_name + ".jpeg")
    create_dir_if_doesnt_exist(file_path)
    save_image_from_image_data(
        image_data_string=canvas_image, directory=file_path)
    return file_path


def create_video_file(name, video_blob):
    file_name = name if name != '' else 'current_video'
    file_path = os.path.join(
        os.getcwd(), "newEntry/")
    create_dir_if_doesnt_exist(file_path)
    # save_image_from_image_data(
    #     image_data_string=video_blob, directory=file_path)
    video_blob.save(file_path + file_name + ".webm")
    return file_path + file_name + ".webm"


def filter_probabilities(network_estimations, class_list, dataset_classlist):
    result = {}
    index = 0
    print("Network estimations are: ", network_estimations)
    print("Class list is: ", class_list)
    for probability in network_estimations:
        print("Probability is: ", probability)
        if probability is not None and probability > 0.01:
            result[get_prediction_id(
                class_list[index], dataset_classes=dataset_classlist)] = probability
        index += 1
    return result


def latest_saved_model(parent):
    current_version = 0.0
    for directory in os.listdir(path=parent):
        splitted = str(directory).split('-')
        if len(splitted) <= 1 or splitted[0] != 'version':
            continue
        print('Found a good version number: ', directory)
        version = turn_to_float(splitted[1])
        if version > current_version:
            current_version = version
    # Gradually increase version
    return current_version


def next_model_version(parent):
    return latest_saved_model(parent) + 0.1


def turn_to_float(number):
    try:
        return float(number)
    except ValueError:
        return 0.0


def load_dataset(path):
    from keras.preprocessing.image import ImageDataGenerator
    try:
        generator = tf.keras.preprocessing.image.ImageDataGenerator(
            height_shift_range=0.2,
            width_shift_range=0.3,
            zoom_range=0.2,
            rotation_range=20,
            validation_split=0.2,
            fill_mode='nearest',
            preprocessing_function=tf.keras.applications.resnet50.preprocess_input,
        )

        train_generator = generator.flow_from_directory(
            path,
            target_size=(224, 224),
            batch_size=32,
            shuffle=True,
            class_mode='categorical',
            subset='training',
        )

        validation_generator = generator.flow_from_directory(
            path,
            target_size=(224, 224),
            batch_size=32,
            shuffle=True,
            class_mode='categorical',
            subset='validation'
        )
        return train_generator, validation_generator, train_generator.class_indices
    except Exception as exception:
        raise Exception(exception)
