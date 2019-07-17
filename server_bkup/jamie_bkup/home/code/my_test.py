import tensorflow as tf
import numpy as np
import librosa

def extract_feature(filename):
  X, sr = librosa.load(filename)
  mfccs = librosa.feature.mfcc(y = X, sr = sr, n_mfcc = 39, hop_length = int(sr * 0.01), n_fft = int(sr * 0.02)).T
    
  return mfccs

n = 39
dirname = '/home/ubuntu/'
input_file = dirname + 'input/시간.wav'
trained_model = 'model/temp/main_model.ckpt'

all_mfccs = np.ndarray(shape = [0,n], dtype = np.float32)
feature = extract_feature(input_file)
all_mfccs = np.append(all_mfccs, feature, axis = 0)

tf.reset_default_graph()

with tf.Session() as sess:
  saver = tf.train.import_meta_graph(dirname + trained_model + '.meta')
  saver.restore(sess, dirname + trained_model)
  
  graph = tf.get_default_graph()
  
  learning_rate = 0.1
  training_epochs = 1000000
  
  n_dim = 39
  
  #classes number
  n_classes = 5
  
  n_hid1 = 300
  n_hid2 = 200
  n_hid3 = 100
  
  #placeholder for input
  X = graph.get_tensor_by_name('X:0')
  Y = graph.get_tensor_by_name('Y:0')
  
  stddev = 0.1
  
  #weight
  W1 = graph.get_tensor_by_name('w1:0')
  W2 = graph.get_tensor_by_name('w2:0')
  W3 = graph.get_tensor_by_name('w3:0')
  W = graph.get_tensor_by_name('w:0')
  
  #bias
  b1 = graph.get_tensor_by_name('b1:0')
  b2 = graph.get_tensor_by_name('b2:0')
  b3 = graph.get_tensor_by_name('b3:0')
  b = graph.get_tensor_by_name('b:0')
  
  #layer
  layer1 = tf.nn.sigmoid(tf.matmul(X, W1) + b1)
  layer2 = tf.nn.sigmoid(tf.matmul(layer1, W2) + b2)
  layer3 = tf.nn.sigmoid(tf.matmul(layer2, W3) + b3)
  
  keep_prob = graph.get_tensor_by_name('keep_prob:0')
  dropout = tf.nn.dropout(layer3, keep_prob)
  
  k = tf.matmul(dropout, W) + b
  
  #y_hat
  y = tf.nn.softmax(tf.matmul(dropout, W) + b)
  
  cross_entropy = tf.reduce_mean(-Y * tf.log(tf.clip_by_value(y, 1e-10, 1.0)))
  train_step = tf.train.GradientDescentOptimizer(learning_rate).minimize(cross_entropy)
  
  #y_hat의 max value와 Y의 value 비교
  correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(Y, 1))
  accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
  
  data = all_mfccs
  
  y_hat = sess.run(y, feed_dict = {X: data, keep_prob: 1.0})
  
  #answer list
  length = len(y_hat)
  ans_list = np.zeros(shape = [2], dtype = np.float32)
  
  for num in range(length):
    if num == 0:
      ans_list = y_hat[num]
    else:
      ans_list = ans_list + y_hat[num]
      
  ans_list /= num
  ans = np.argmax(ans_list, 0)
    
  if ans == 0:
    output = '뉴스'
  if ans == 1:
    output = '리모컨'
  if ans == 2:
    output = '소리작게'
  if ans == 3:
    output = '소리크게'
  if ans == 4:
    output = '시간'

  print(output)
  print(ans_list)

  out_file = open('/var/www/html/new.php', 'w')
  out_file.write(output)
