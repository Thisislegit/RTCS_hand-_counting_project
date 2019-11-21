# importing stuff
import tensorflow as tf
import numpy as np
import cv2
import math
import os
import time
from scipy import misc

# loading data params
PATH = 'data2/'





# conv net hyper parameters

img_size = 64

img_size_flat = img_size * img_size

img_shape = (img_size, img_size)

num_channels = 1
num_classes = 6

# conv layer 1
filter_size1 = 3
num_filters1 =  8

# conv layer 2 
filter_size2 = 3
num_filters2 = 16

# conv layer 3 
filter_size3 = 3
num_filters3 = 32


fc_layer = 512 

lr = 0.001
def create_conv_layer(input, num_input_channels, filter_size, num_filters, use_pooling=True):
    
    filter_shape = [filter_size, filter_size, num_input_channels, num_filters]
    
    print(filter_shape)
    
    weights = tf.Variable(tf.truncated_normal(shape=filter_shape))
    
    biases = tf.Variable(tf.constant(0.05, shape=[num_filters]))
    
    layer = tf.nn.conv2d(input=input,
                        filter=weights,
                        strides=[1, 1, 1, 1],
                         padding='SAME')
    
    layer += biases
    
    if use_pooling:
        
        layer = tf.nn.max_pool(value=layer,
                              ksize=[1, 2, 2, 1],
                               strides=[1, 2, 2, 1],
                               padding='SAME')
        
    layer = tf.nn.relu(layer)
    
    return layer, weights


def create_fully_connected(input,
                          num_inputs,
                          num_outputs,
                          use_relu=True):
    
    weights = tf.Variable(tf.truncated_normal(shape=[num_inputs, num_outputs]))
    
    biases = tf.Variable(tf.constant(0.05, shape=[num_outputs]))
    
    layer = tf.matmul(input, weights) + biases
    
    if use_relu:
        layer = tf.nn.relu(layer)
        
    return layer

def flatten_layer(layer):
    
    layer_shape = layer.get_shape()
    
    num_features = layer_shape[1:4].num_elements()
    
    layer_flat = tf.reshape(layer, [-1, num_features])
    
    return layer_flat, num_features


x = tf.placeholder(tf.float32, shape=[None, img_size, img_size, num_channels], name='x')
y = tf.placeholder(tf.float32, shape=[None, num_classes], name='y')



layer_conv1, weights_conv1 = create_conv_layer(input=x,
                                              num_input_channels=num_channels,
                                              filter_size=filter_size1,
                                              num_filters=num_filters1,
                                              use_pooling=True)

layer_conv2, weights_conv2 = create_conv_layer(input=layer_conv1,
                                              num_input_channels=num_filters1,
                                              filter_size=filter_size2,
                                              num_filters=num_filters2,
                                              use_pooling=True)

layer_conv3, weights_conv3 = create_conv_layer(input=layer_conv2,
                                              num_input_channels=num_filters2,
                                              filter_size=filter_size3,
                                              num_filters=num_filters3,
                                              use_pooling=True)


layer_flat, num_features = flatten_layer(layer_conv3)
print("Num features: " + str(num_features))


fc_layer1 = create_fully_connected(input=layer_flat,
                                  num_inputs=num_features,
                                  num_outputs=fc_layer,
                                  use_relu=True)

dropout = tf.layers.dropout(inputs=fc_layer1, rate=0.4, training=False)

fc_layer2 = create_fully_connected(input=dropout,
                                  num_inputs=fc_layer,
                                  num_outputs=num_classes,
                                  use_relu=False)




y_pred = tf.nn.softmax(fc_layer2)
y_pred_class = tf.argmax(y_pred, axis=1)

cross_entropy = tf.nn.softmax_cross_entropy_with_logits(logits=fc_layer2, labels=y)

cost = tf.reduce_mean(cross_entropy)

optimizer = tf.train.AdamOptimizer(learning_rate=lr).minimize(cost)

saver = tf.train.Saver()

save_dir = 'checkpoints/fingerstwo/'

session = tf.Session()

session.run(tf.global_variables_initializer())

saver.restore(sess=session, save_path=save_dir)


def resize_img(img, img_size):
    y = math.floor((img_size/img.shape[0])*img.shape[1])
    resized = cv2.resize(img, (y, img_size))
    return resized

 
def crop_img_hor(img, final_width):
    left_border = math.floor((img.shape[1] - final_width) / 2)
    right_border = final_width + left_border
    img_cropped = img[:, left_border:right_border]
    return img_cropped

def crop_img_ver(img, final_width):
    top_border = math.floor((img.shape[0] - final_width) / 2)
    bottom_border = final_width + top_border
    img_cropped = img[top_border: bottom_border, :]
    return img_cropped



def crop_img(img, final_width):
    left_border = math.floor((img.shape[1] - final_width) / 2)
    right_border = final_width + left_border
#     print(left_border)
#     print(right_border)
    img_cropped = img[:, left_border:right_border]
    return img_cropped

def preprocess_imgs(X):
    X = (X / 255 * 0.99) + 0.01
    return X




from picamera.array import PiRGBArray
from picamera import PiCamera


image_size = 64
cropped_size = 380
recognition_ratio = 10
res = (640, 480)
fps = 30


# initialize the cam
camera = PiCamera()
camera.resolution = res
camera.framerate = fps
rawCapture = PiRGBArray(camera, size=res)

# allow the camera to warmup
time.sleep(0.1)

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):

    # current frame as numpy array
    img = frame.array

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
#    img_resized = resize_img(img_gray, img_size)

    img_cropped = crop_img_hor(img_gray, cropped_size)
    img_cropped = crop_img_ver(img_cropped, cropped_size) 
    img_resized = resize_img(img_cropped, img_size)
    print("RESIZED: " + str(img_resized.shape))
    img_shapened = img_resized.reshape(1, img_size, img_size, 1) 

    img_scaled = preprocess_imgs(img_shapened)

    pred_cls = session.run(y_pred_class, feed_dict={x: img_scaled})
    pred = session.run(y_pred, feed_dict={x: img_scaled})
    font = cv2.FONT_HERSHEY_SIMPLEX
    msg = ""
    if pred_cls[0] == 0:
        msg = "Two"
    elif pred_cls[0] == 1:
        msg = "Five"
    elif pred_cls[0] == 2:
        msg = "Zero"
    elif pred_cls[0] == 3:
        msg = "Four"
    elif pred_cls[0] == 4:
        msg = "Three"
    elif pred_cls[0] == 5:
        msg = "One"

   # cv2.putText(img, msg, (50, 50), font, 2, (255, 255, 255), 2, cv2.LINE_AA)

    cv2.putText(img_cropped, msg, (30,60), font, 2, (0, 255, 0), 2, cv2.LINE_AA)
    
    print(pred)
    #cv2.imshow('RAW', img)
    cv2.imshow('RAW', img_cropped)
    key = cv2.waitKey(1) & 0xFF 
    rawCapture.truncate(0)

    if key == ord('q'):
        print("FJDASLFJASLFJDASLF")
        break







