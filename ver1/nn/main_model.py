#기존의 모델을 이어받아서 학습 + gaussian noise
#_*_coding: utf-8_*_

import tensorflow as tf
import numpy as np

def Gaussian_noise(input_data, std = 0.1):
  noise = np.random.normal(loc = 0.0, scale = std, size = input_data.shape)
  #noise = tf.random_normal(shape = input_data.shape(), mean = 0.0, stddev = std, dtype = tf.float32)
  
  return input_data + noise

dirname = '/gdrive/My Drive/18-winter/정리판/main/'
data = np.load(dirname + 'data/data.npz')
x_data = data['X']
y_data = data['Y']

x_data = Gaussian_noise(x_data)

tf.reset_default_graph()

with tf.Session() as sess:
  saver = tf.train.import_meta_graph(dirname + '/model_gaussian/main_model.meta')
  saver.restore(sess, tf.train.latest_checkpoint(dirname + '/model_gaussian/'))

  graph = tf.get_default_graph()
  
  learning_rate = 0.1
  training_epochs = 10000000
  #batch_size = 100
  
  n_dim = 39
  n_classes = 9

  n_hid1 = 300
  n_hid2 = 200
  n_hid3 = 100

  X = tf.placeholder(tf.float32, [None, 39], name = 'X')
  Y = tf.placeholder(tf.float32, [None, 9], name = 'Y')
  
  stddev = 0.1 #standard deviation

  #WEIGHTS
  W1 = graph.get_tensor_by_name("w1:0")
  W2 = graph.get_tensor_by_name("w2:0")
  W3 = graph.get_tensor_by_name("w3:0")
  W = graph.get_tensor_by_name("w:0")

  #BIASES
  b1 = graph.get_tensor_by_name("b1:0")
  b2 = graph.get_tensor_by_name("b2:0")
  b3 = graph.get_tensor_by_name("b3:0")
  b = graph.get_tensor_by_name("b:0")

  #laters
  layer1 = tf.nn.sigmoid(tf.matmul(X, W1) + b1)
  layer2 = tf.nn.relu(tf.matmul(layer1, W2) + b2)
  layer3 = tf.nn.relu(tf.matmul(layer2, W3) + b3)

  #dropout
  keep_prob = tf.placeholder(tf.float32, name = 'keep_prob')
  dropout = tf.nn.dropout(layer3, keep_prob)

  k = tf.matmul(dropout, W) + b

  y = tf.nn.softmax(tf.matmul(dropout, W) + b)#추측값

  cross_entropy = tf.reduce_mean(-Y*tf.log(tf.clip_by_value(y, 1e-10, 1.0)))#tf.clip_by_value(t, min, max, name = None): t를 min과 max 사이의 값으로 지정
  train_step = tf.train.GradientDescentOptimizer(learning_rate).minimize(cross_entropy)

  correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(Y, 1))
  accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

  epoch = 0
  train_accuracy = 0
  
  for epoch in range(training_epochs):
    sess.run(train_step, feed_dict = {X: x_data, Y: y_data, keep_prob: 0.5})

    if epoch%1000 == 0:
        train_accuracy, hypo = sess.run([accuracy, y], feed_dict = {X: x_data, Y: y_data, keep_prob: 1.0})
                 
        print("step: %d, "%(epoch))
        print("training accuracy: %f, "%(train_accuracy))
        
        m = 0       
        h = [0,0,0,0,0,0,0,0,0]   
        for k in range(0, 16128):
          h = h + hypo[k]
          m = m+1

        h /= m
        print(h)
        max_ = np.argmax(h)
        print(max_)
       
        m = 0
        h = [0,0,0,0,0,0,0,0,0]       
        for k in range(16129, 35093):
          h = h + hypo[k]
          m = m+1
        
        h /= m
        print(h)
        max_ = np.argmax(h)
        print(max_)
        
        m = 0
        h = [0,0,0,0,0,0,0,0,0]
        for k in range(35094, 52909):
          h = h + hypo[k]
          m = m+1
        
        h /= m        
        print(h)
        max_ = np.argmax(h)
        print(max_)
        
        m = 0
        h = [0,0,0,0,0,0,0,0,0]
        for k in range(52910, 69924):
          h = h + hypo[k]
          m = m+1
        
        h /= m        
        print(h)
        max_ = np.argmax(h)
        print(max_)
         
        m = 0  
        h = [0,0,0,0,0,0,0,0,0]
        for k in range(69925, 85754):
          h = h + hypo[k]
          m = m+1
        
        h /= m        
        print(h)
        max_ = np.argmax(h)
        print(max_)
          
        m = 0  
        h = [0,0,0,0,0,0,0,0,0]
        for k in range(85755, 105390):
          h = h + hypo[k]
          m = m+1
        
        h /= m        
        print(h)
        max_ = np.argmax(h)
        print(max_)

        m = 0
        h = [0,0,0,0,0,0,0,0,0]
        for k in range(105391, 123585):
          h = h + hypo[k]
          m = m+1
        
        h /= m        
        print(h)
        max_ = np.argmax(h)
        print(max_)  
          
        m = 0  
        h = [0,0,0,0,0,0,0,0,0]
        for k in range(123586, 142774):
          h = h + hypo[k]
          m = m+1
        
        h /= m        
        print(h)
        max_ = np.argmax(h)
        print(max_)
        
        m = 0
        h = [0,0,0,0,0,0,0,0,0]
        for k in range(142775, 157066):
          h = h + hypo[k]
          m = m+1
        
        h /= m        
        print(h)
        max_ = np.argmax(h)
        print(max_)          

    if epoch%1000 == 0:
        saver.save(sess, dirname + 'model_gaussian/main_model')
        print("save %d"%epoch)

    if 0.9 < train_accuracy:
      break
    if hypo[0][0] == 'nan':
      break

print(sess.run([accuracy, y], feed_dict = {X: x_data, Y: y_data, keep_prob: 1.0}))
saver.save(sess, dirname + 'model_gaussian/main_model')

data.close()
print("save the model")
