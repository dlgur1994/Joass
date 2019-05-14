#새로운 model을 만드는 NN, test accuracy는 생략 - 전체 feature에 대한 training accuracy만 측정
#_*_coding: utf-8_*_

import tensorflow as tf
import numpy as np

#data location
dirname = '/gdrive/My Drive/18-winter/정리판/main/'
data = np.load(dirname + 'data/data.npz')
x_data = data['X']
y_data = data['Y']

learning_rate = 0.1
training_epochs = 10000000

n_dim = 39
n_classes = 9

n_hid1 = 300
n_hid2 = 200
n_hid3 = 100

X = tf.placeholder(tf.float32, [None, n_dim], name = 'X')
Y = tf.placeholder(tf.float32, [None, n_classes], name = 'Y')

stddev = 0.1 #standard deviation??

#WEIGHTS
W1 = tf.Variable(tf.random_normal([n_dim, n_hid1], stddev = stddev), name = "w1")
W2 = tf.Variable(tf.random_normal([n_hid1, n_hid2], stddev = stddev), name = "w2")
W3 = tf.Variable(tf.random_normal([n_hid2, n_hid3], stddev = stddev), name = "w3")
W = tf.Variable(tf.random_normal([n_hid3, n_classes], stddev = stddev), name = "w")

#BIASES
b1 = tf.Variable(tf.random_normal([n_hid1]), name = "b1")
b2 = tf.Variable(tf.random_normal([n_hid2]), name = "b2")
b3 = tf.Variable(tf.random_normal([n_hid3]), name = "b3")
b = tf.Variable(tf.random_normal([n_classes]), name = "b")

#layers
layer1 = tf.nn.sigmoid(tf.matmul(X, W1) + b1, name = "layer1")
layer2 = tf.nn.relu(tf.matmul(layer1, W2) + b2, name = "layer2")
layer3 = tf.nn.relu(tf.matmul(layer2, W3) + b3, name = "layer3")

#dropout
keep_prob = tf.placeholder(tf.float32, name = "keep_prob")
dropout = tf.nn.dropout(layer3, keep_prob, name = "dropout")

k = tf.matmul(dropout, W) + b

y = tf.nn.softmax(tf.matmul(dropout, W) + b)#추측값

cross_entropy = tf.reduce_mean(-Y*tf.log(tf.clip_by_value(y, 1e-10, 1.0)), name = "cost")#tf.clip_by_value(t, min, max, name = None): t를 min과 max 사이의 값으로 지정

train_step = tf.train.GradientDescentOptimizer(learning_rate).minimize(cross_entropy)

correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(Y, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32), name = "accuracy")

init = tf.global_variables_initializer()

saver = tf.train.Saver()#saver

epoch = 0
train_accuracy = 0

with tf.Session() as sess:
    sess.run(init)

    for epoch in range(training_epochs):
        sess.run(train_step, feed_dict = {X: x_data, Y: y_data, keep_prob: 0.5})

        if epoch%1000 == 0:
            train_accuracy, hypo = sess.run([accuracy, y], feed_dict = {X: x_data, Y: y_data, keep_prob: 1.0})
            print('step: ',epoch,', training accuracy: ',train_accuracy)

            saver.save(sess, dirname + 'model/main_model.ckpt')
            print("save %d"%epoch)

        if 0.9 < train_accuracy:
          break
        if hypo[0][0] == 'nan':
          break

    print(sess.run([accuracy, y], feed_dict = {X: x_data, Y: y_data, keep_prob: 1.0}))

    #save trained model
    saver.save(sess, dirname + 'model/main_model.ckpt')

    data.close()
    print("save the model")
