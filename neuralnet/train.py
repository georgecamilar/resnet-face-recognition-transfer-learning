# Used for training

# Used to train the resnet model on the new dataset
# Taken from the Extended Yale Dataset
# Added sGeorge as the class for George Camilar as a subject for the neural network

import tensorflow as tf
import os

dataset_path = "/Users/georgecamilar/Documents/ExtendedYaleB"

resnet = tf.keras.applications.resnet50.ResNet50(
    input_shape=(224, 224, 3),
    include_top=False,
    weights='imagenet',
    pooling=max)

resnet.summary()

trainable_attr = False

for layer in resnet.layers:
    layer.trainable = trainable_attr


def create_new_model(num_classes):
    return tf.keras.Sequential([
        resnet,
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(512, activation='relu'),
        tf.keras.layers.Dense(256, activation='relu'),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(num_classes, activation='softmax')
    ])


def dataset_generator(dataset_path):
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


train_data, validation_data, indices = dataset_generator(dataset_path)

# TODO look into early stopping from documentation
early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=3, verbose=1, mode='auto')
mcp_save = tf.keras.callbacks.ModelCheckpoint('.mdl_wts.hdf5', save_best_only=True, monitor='val_loss', mode='min')
reduce_lr_loss = tf.keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.1, patience=7, verbose=1,
                                                      min_delta=1e-4, mode='auto')

class_num = len(indices.keys())
print("Epochs: {}".format(class_num * 3), "Batch Size: 32", "Starting Learning Rate: {}".format(0.10))
model = create_new_model(class_num)
model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(train_data,
          steps_per_epoch=train_data.samples // 32,
          validation_data=validation_data,
          validation_steps=validation_data.samples // 32,
          callbacks=[reduce_lr_loss, early_stopping, mcp_save],
          shuffle=True,
          epochs=class_num * 3)

current_working_dir = os.getcwd()
save_dir = "saved-models/resnet-saved"
path = os.path.join(current_working_dir, save_dir)
model.save(path)
