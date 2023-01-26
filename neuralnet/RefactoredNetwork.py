import sys

import tensorflow as tf
import os

import neuralnet.networkUtils

GIVEN_ERROR_IS_MESSAGE_TEMPLATE = "Cannot load network. If you do not have the trained model, run the training " \
                                  "script. Given error is: {message} "

# TODO can be changed with the [your_dir]/experiments/saved_model/resnet_saved
# SAVED_MODEL_PATH = "/Users/georgecamilar/Personal/licenta/notebooks/saved-models/resnet-saved"
SAVED_MODEL_PATH = "licenta/notebooks/saved-models/resnet-saved"
DATASET_PATH = "ExtendedYaleB"


class FaceRecognitionNet(object):
    def __init__(self, base_path) -> None:
        try:
            self.base_path = base_path
            self.model = tf.keras.models.load_model(
                os.path.join(base_path, SAVED_MODEL_PATH))
            self.class_indices = self.get_dataset_classes()
        except Exception as e:
            error_message = GIVEN_ERROR_IS_MESSAGE_TEMPLATE.format(
                message=str(e))
            sys.exit(error_message)

    def predict(self, image_path):
        image = neuralnet.networkUtils.prepare_image_for_predict(
            image_path=image_path)
        prediction = self.model.predict(image)
        return prediction

    def train(self):
        # load ResNet50 Model
        resnet = self.load_resnet()

        # load data from configured folder
        train_data, validation_data, indices = self.create_dataset_generator(
            os.path.join(self.base_path, DATASET_PATH))
        class_num = len(indices.keys())

        # create new Neural Network Model
        model = tf.keras.Sequential([
            resnet,
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dropout(0.5),
            tf.keras.layers.Dense(512, activation='relu'),
            tf.keras.layers.Dense(256, activation='relu'),
            tf.keras.layers.Dense(128, activation='relu'),
            tf.keras.layers.Dense(class_num, activation='softmax')
        ])

        # Create callbacks
        # early_stopping -- stops the learning process when the network is on high accuracy and improvements are minimal
        early_stopping = tf.keras.callbacks.EarlyStopping(
            monitor='val_loss', patience=3, verbose=1, mode='auto')
        # mcp_save saves -- the model as checkpoints to load faster the desired network variation
        mcp_save = tf.keras.callbacks.ModelCheckpoint(
            '.mdl_wts.hdf5', save_best_only=True, monitor='val_loss', mode='min')
        # reduce_lr_loss -- reduces the learning rate when reaching the learning plateau
        reduce_lr_loss = tf.keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss', factor=0.1, patience=7, verbose=1, min_delta=1e-4, mode='auto')

        # compile and train the model
        model.compile(optimizer='Adam',
                      loss='categorical_crossentropy', metrics=['accuracy'])
        model.fit(train_data,
                  steps_per_epoch=train_data.samples // 32,
                  validation_data=validation_data,
                  validation_steps=validation_data.samples // 32,
                  callbacks=[reduce_lr_loss, early_stopping, mcp_save],
                  shuffle=True,
                  epochs=class_num*3)

        current_working_dir = os.getcwd()
        save_dir = "saved-models/resnet-saved"
        path = os.path.join(current_working_dir, save_dir)
        model.save(path)

    def load_resnet(self):
        resnet = tf.keras.applications.resnet50.ResNet50(
            input_shape=(224, 224, 3),
            include_top=False,
            weights='imagenet',
            pooling=max)

        resnet.summary()

        # freeze layers
        trainable_attr = False
        for layer in resnet.layers:
            layer.trainable = trainable_attr

        return resnet

    def create_dataset_generator(self, dataset_path):
        generator = tf.keras.preprocessing.image.ImageDataGenerator(
            height_shift_range=0.2,
            validation_split=0.2,
            preprocessing_function=tf.keras.applications.resnet50.preprocess_input,
        )
        train_data_gen = generator.flow_from_directory(
            dataset_path,
            target_size=(224, 224),
            batch_size=32,
            shuffle=True,
            class_mode='categorical',
            subset='training',
        )

        validation_data_gen = generator.flow_from_directory(
            dataset_path,
            target_size=(224, 224),
            batch_size=32,
            shuffle=True,
            class_mode='categorical',
            subset='validation'
        )
        return train_data_gen, validation_data_gen, train_data_gen.class_indices

    def get_dataset_classes(self):
        generator = tf.keras.preprocessing.image.ImageDataGenerator()
        data = generator.flow_from_directory(os.path.join(
            self.base_path, DATASET_PATH), target_size=(224, 224))
        return data.class_indices
