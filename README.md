Neural Network enforced login:

Network used with transfer learning and reinforcement learning.
Model used is VGG16 taken from the package tensorflow.keras.applications.resnet50

The network model architecture is a Sequential keras model and the layers are presented as the following:
Model: "sequential"
_________________________________________________________________
 Layer (type)                Output Shape              Param #   
=================================================================
 resnet50 (Functional)       (None, 7, 7, 2048)        23587712  
                                                                 
 flatten (Flatten)           (None, 100352)            0         
                                                                 
 dropout (Dropout)           (None, 100352)            0         
                                                                 
 dense (Dense)               (None, 512)               51380736  
                                                                 
 dense_1 (Dense)             (None, 256)               131328    
                                                                 
 dense_2 (Dense)             (None, 128)               32896     
                                                                 
 dense_3 (Dense)             (None, 29)                3741      
                                                                 
=================================================================
Total params: 75,136,413
Trainable params: 51,548,701
Non-trainable params: 23,587,712
_________________________________________________________________

where the 'net' parameter stands for the resnet

To do List:

* Check predictions of neural network and retrain it if necessary
    1. Add admin account and password with admin login credentials
    2. Rebuild model in ipython notebook
    3. Retrain using dataset
    4. Add your own photos
    5. Add train method so when a new employee is added, the training can begin and the next day, it will be available
