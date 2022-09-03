Neural Network enforced login:

Network used with transfer learning and reinforcement learning.
Model used is VGG16 taken from the package tensorflow.keras.applications.vgg16

The network model architecture is a Sequential keras model and the layers are presented as the following:

    return tf.keras.Sequential([
        net,
        tf.keras.layers.GlobalAveragePooling2D(),
        tf.keras.layers.Dense(2048, activation='relu'),
        tf.keras.layers.Dense(1024, activation='relu'),
        tf.keras.layers.Dense(512, activation='relu'),
        tf.keras.layers.Dense(classification_case_number, activation='softmax')
    ])

where the 'net' parameter stands for the vgg16

To do List:

* Check predictions of neural network and retrain it if necessary
    1. Add admin account and password with admin login credentials
    2. Rebuild model in ipython notebook
    3. Retrain using dataset
    4. Add your own photos
    5. Add train method so when a new employee is added, the training can begin and the next day, it will be available
