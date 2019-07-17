#main_model + model_소작크 -> test
import tensorflow as tf
import numpy as np
import librosa

class ImportGraph():
    """  Importing and running isolated TF graph """
    def __init__(self, loc):
        # Create local graph and use it in the session
        self.graph = tf.Graph()
        self.sess = tf.Session(graph=self.graph)
        with self.graph.as_default():
            # Import saved model from location 'loc' into local graph
            saver = tf.train.import_meta_graph(loc + '.meta', clear_devices=True)
            saver.restore(self.sess, loc)
            
            #self.X = self.graph.get_tensor_by_name("X:0")
            self.X = tf.placeholder(tf.float32, [None, 39], name = 'X')
            self.Y = self.graph.get_tensor_by_name("Y:0")

            #WEIGHTS
            self.W1 = self.graph.get_tensor_by_name("w1:0")
            self.W2 = self.graph.get_tensor_by_name("w2:0")
            self.W3 = self.graph.get_tensor_by_name("w3:0")
            self.W = self.graph.get_tensor_by_name("w:0")

            #BIASES
            self.b1 = self.graph.get_tensor_by_name("b1:0")
            self.b2 = self.graph.get_tensor_by_name("b2:0")
            self.b3 = self.graph.get_tensor_by_name("b3:0")
            self.b = self.graph.get_tensor_by_name("b:0")

            #layers
            self.layer1 = tf.nn.sigmoid(tf.matmul(self.X, self.W1) + self.b1)
            self.layer2 = tf.nn.relu(tf.matmul(self.layer1, self.W2) + self.b2)
            self.layer3 = tf.nn.relu(tf.matmul(self.layer2, self.W3) + self.b3)

            #dropout
            self.keep_prob = tf.placeholder(tf.float32, name = "keep_prob")
            self.dropout = tf.nn.dropout(self.layer3, self.keep_prob)

            self.y = tf.nn.softmax(tf.matmul(self.dropout, self.W) + self.b)#추측값

    def run(self, data, s):
        """ Running the activation operation previously imported """
        # The 'x' corresponds to name of input placeholder
        y_hat = self.sess.run(self.y, feed_dict={self.X: data, self.keep_prob: 1.0})
        
        length = len(y_hat)
        ans_list = np.zeros(shape = [s], dtype = np.float32)
        
        for num in range(length):
          ans_list = ans_list + y_hat[num]
          
        ans_list /= num
        ans = np.argmax(ans_list, 0)
        
        if s == 5:
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
        if s == 2:
          if ans == 0:
            output = '소리작게'
          if ans == 1:
            output = '소리크게'
        
        return output, ans_list

def extract_feature(filename):
    X, sr = librosa.load(filename)
    mfccs = librosa.feature.mfcc(y = X, sr = sr, n_mfcc = 39, hop_length = int(sr*0.01), n_fft = int(sr*0.02)).T

    return mfccs

### Using the class ###
dirname = '/home/ubuntu/'

main_model_path = dirname + 'model/temp/main_model.ckpt'
input_path = dirname + 'sound_data/record/my_voice/'

e = [0,0,0,0,0]#각 class 마다 일치한 test sample 개수
T = 0#ans와 일치한 test sample 개수
m = 0#전체 test sample 개수
hypo = [0,0,0,0,0]

for d in range(5):
    if d == 0:
      filename = '뉴스'
    if d == 1:
      filename = '리모컨'
    if d == 2:
      filename = '소리작게'
    if d == 3:
      filename = '소리크게'
    if d == 4:
      filename = '시간'
    
    for count in range(1):
      #data = np.load(input_path + filename + '/%d.npz'%count)# random data
      n = 39
      input_file = input_path + filename + ".wav"

      data = np.ndarray(shape = [0,n], dtype = np.float32)
      feature = extract_feature(input_file)
      data = np.append(data, feature, axis = 0)

      model = ImportGraph(main_model_path)
      result, hypo = model.run(data, 5)

      m = m+1
      if filename == result:
        T = T+1
        e[d] = e[d]+1
        
      print(filename, result)
      print(hypo)

for l in range(5):
  print(e[l])
  
test_accuracy = T/m
print("test_accuracy: %f"%test_accuracy)
