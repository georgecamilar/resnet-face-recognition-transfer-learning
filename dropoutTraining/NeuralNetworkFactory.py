import tensorflow as tf
from neuralnet.networkUtils import *


class NeuralNetworkFactory:
    def __init__(self, dataset_path=None):
        try:
            train_datagen, validation_generator, class_indices = load_dataset(dataset_path)
            print(len(class_indices))
            base_model = self.__create_frozen_model()

            save_directory = os.path.join(HOME_DIRECTORY, 'saved')
            name = next_model_version(save_directory)
            final_directory = os.path.join(save_directory, "version-" + str(name))
            path = os.path.join(final_directory, "network_save.h5")

            carry = tf.keras.layers.GlobalAveragePooling2D()(base_model.output)
            carry = tf.keras.layers.Dense(1024, activation="relu")(carry)
            carry = tf.keras.layers.Dropout(0.5)(carry)
            carry = tf.keras.layers.Dense(512, activation="relu")(carry)
            carry = tf.keras.layers.Dropout(0.5)(carry)
            carry = tf.keras.layers.Dense(len(class_indices), activation="softmax")(carry)
            self.model = tf.keras.models.Model(inputs=base_model.input, outputs=carry)
            self.model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['accuracy'])

            # Create callbacks
            early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=1, verbose=1, mode='auto')
            reduce_lr_loss = tf.keras.callbacks.ReduceLROnPlateau(
                monitor='val_loss', factor=0.1, patience=1, verbose=1, min_delta=1e-4, mode='auto')

            self.model.fit(train_datagen,
                           steps_per_epoch=train_datagen.samples // 32,
                           validation_data=validation_generator,
                           validation_steps=validation_generator.samples // 32,
                           callbacks=[reduce_lr_loss, early_stopping],
                           shuffle=True,
                           epochs=10)
            create_dir_if_doesnt_exist(final_directory)
            self.next_model_save_path = final_directory + "/network_save.h5"
            print("Model saved at path: ", self.next_model_save_path)
            self.model.save(self.next_model_save_path)

        except Exception as exception:
            print("Dataset path loading failed: " + str(exception))

    @staticmethod
    def __create_frozen_model():
        # Load ResNet50 with the imagenet weights
        # using 224/224 width/height ratio with all 3 RGB channels
        resnet = tf.keras.applications.resnet50.ResNet50(weights='imagenet', input_shape=(224, 224, 3),
                                                         include_top=False)
        # Freeze the layers
        for layer in resnet.layers:
            layer.trainable = False

        return resnet