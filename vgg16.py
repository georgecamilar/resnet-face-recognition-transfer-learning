# import tensorflow as tf
# from tensorflow import keras
# from tensorflow.keras.applications.vgg16 import VGG16
#
# taken_net = VGG16(include_top=False, weights='imagenet', input_shape=(224, 224, 3))
# taken_net.summary()
#
#
# # this needs to be refactored
#
# def freeze_layers(net):
#     for layer in net.layers:
#         layer.trainable = False
#     return net
#
#
# def create_override(net, classification_case_number):
#     return tf.keras.Sequential([
#         net,
#         tf.keras.layers.GlobalAveragePooling2D(),
#         tf.keras.layers.Dense(2048, activation='relu'),
#         tf.keras.layers.Dense(1024, activation='relu'),
#         tf.keras.layers.Dense(512, activation='relu'),
#         tf.keras.layers.Dense(classification_case_number, activation='softmax')
#     ])
#
#
# def create_image_data_generator():
#     train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
#         rescale=1. / 255,
#         rotation_range=20,
#         width_shift_range=0.2,
#         height_shift_range=0.2,
#         horizontal_flip=False,
#         fill_mode='nearest',
#         preprocessing_function=tf.keras.applications.vgg16.preprocess_input,
#         validation_split=0.2
#     )
#     train_data = train_datagen.flow_from_directory(
#         "/Users/georgecamilar/Documents/transferLearning/gt_db",
#         target_size=(224, 224),
#         batch_size=32,
#         shuffle=True,
#         class_mode='categorical',
#         subset='training')
#
#     validation_data = train_datagen.flow_from_directory(
#         "/Users/georgecamilar/Documents/transferLearning/gt_db",
#         target_size=(224, 224),
#         batch_size=32,
#         shuffle=True,
#         class_mode='categorical',
#         subset='validation')
#
#     return train_data, validation_data
#
#     # prepare dataset
#
# def get_classes(data):
#     return data.class_indices
#
#
# train, validation = create_image_data_generator()
# class_number = len(train.class_indices)
# taken_net = freeze_layers(taken_net)
#
# model = create_override(taken_net, class_number)
# model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['accuracy'])
# model.fit_generator(train,
#                     steps_per_epoch=train.samples // 32,
#                     validation_data=validation,
#                     validation_steps=validation.samples // 32,
#                     epochs=25)
#
# # model.save_weights('./checkpoints/my_checkpoint')
# model.save_weights('./checkpoints2/3-dense-layers')
# model.save('./checkpoint')
