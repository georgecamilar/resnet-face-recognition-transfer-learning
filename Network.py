import os
import json
from typing import Any

import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.vgg16 import VGG16


def freeze_layers(net):
    for layer in net.layers:
        layer.trainable = False
    return net


def create_override(net, classification_case_number):
    return tf.keras.Sequential([
        net,
        tf.keras.layers.GlobalAveragePooling2D(),
        tf.keras.layers.Dense(2048, activation='relu'),
        tf.keras.layers.Dense(1024, activation='relu'),
        tf.keras.layers.Dense(512, activation='relu'),
        tf.keras.layers.Dense(classification_case_number, activation='softmax')
    ])

def create_image_data_generator(preprocess_function):
    train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
        rescale=1. / 255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        horizontal_flip=False,
        fill_mode='nearest',
        preprocessing_function=preprocess_function,
        validation_split=0.2
    )
    train_data = train_datagen.flow_from_directory(
        "/Users/georgecamilar/Documents/transferLearning/gt_db_copy",
        target_size=(224, 224),
        batch_size=32,
        shuffle=True,
        class_mode='categorical',
        subset='training')

    validation_data = train_datagen.flow_from_directory(
        "/Users/georgecamilar/Documents/transferLearning/gt_db_copy",
        target_size=(224, 224),
        batch_size=32,
        shuffle=True,
        class_mode='categorical',
        subset='validation')

    return train_data, validation_data


def write_to_classes_file(data):
    path = os.path.join(os.getcwd(), "train_classes.json")
    with open(path, 'w') as file_handle:
        file_handle.write(json.dumps(data))


class Network(object):
    def __init__(self, model_path) -> None:
        if model_path == "":
            self.model = self.train()
        else:
            self.model = tf.keras.models.load_model(model_path)
            self.classes = self.initialize_class_indices(tf.keras.applications.vgg16.preprocess_input)

    def initialize_class_indices(self, preprocess_f):
        train_data, validation_data = create_image_data_generator(preprocess_f)
        return train_data.class_indices

    def predict(self, image_path) -> Any:
        img = tf.keras.utils.load_img(image_path)
        img_tensor = tf.keras.preprocessing.image.img_to_array(img)
        img_array_expanded_dims = np.expand_dims(img_tensor, axis=0)
        preprocessed = tf.keras.applications.vgg16.preprocess_input(img_array_expanded_dims)
        return self.model.predict(preprocessed)

    def train(self):
        taken_net = VGG16(include_top=False, weights='imagenet', input_shape=(224, 224, 3))
        taken_net.summary()
        train_data, validation_data = create_image_data_generator()
        taken_net = freeze_layers(taken_net)
        # should write the classes to a json file
        class_number = len(train_data.class_indices)
        model = create_override(taken_net, class_number)

        model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['accuracy'])
        model.fit_generator(train_data,
                            steps_per_epoch=train_data.samples // 32,
                            validation_data=validation_data,
                            validation_steps=validation_data.samples // 32,
                            epochs=25)

        model.save('./checkpoint_partial')
        return model

    def get_class_indices(self):
        return self.classes
