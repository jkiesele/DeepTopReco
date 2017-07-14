
#define your model

from training_base import training_base

import keras
from keras.layers import Dense, Dropout, Flatten,Concatenate, Convolution2D, LSTM,merge, Convolution1D, Conv2D
from keras.models import Model
def mymodel(Inputs,nclasses,nregclasses,dropoutRate):

    allinputs=Inputs[0]

    x=  Dense(128, activation='relu',kernel_initializer='lecun_uniform', name='dense_1')(allinputs)
    x=  Dense(128, activation='relu',kernel_initializer='lecun_uniform', name='dense_2')(x)
    x=  Dense(128, activation='relu',kernel_initializer='lecun_uniform', name='dense_3')(x)


    prediction =   Dense(nregclasses, activation='linear',kernel_initializer='ones',name='mttbar_pred')(x)
    model = Model(inputs=Inputs, outputs=prediction)
    return model




#also does all the parsing
train=training_base(testrun=False)


train.setModel(mymodel,dropoutRate=0.125)

train.compileModel(learningrate=0.002,
                   loss=['mean_squared_error'],
                   metrics=['accuracy'])


model,history = train.trainModel(nepochs=50, 
                                 batchsize=2000, 
                                 stop_patience=300, 
                                 lr_factor=0.5, 
                                 lr_patience=10, 
                                 lr_epsilon=0.0001, 
                                 lr_cooldown=2, 
                                 lr_minimum=0.0001, 
                                 maxqsize=100)