#main_model + model_소작크 -> test
import tensorflow as tf
import numpy as np
import librosa

def extract_feature(filename):
    X, sr = librosa.load(filename)
    mfccs = librosa.feature.mfcc(y = X, sr = sr, n_mfcc = 39, hop_length = int(sr*0.01), n_fft = int(sr*0.02)).T

    return mfccs

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
            
            self.X = self.graph.get_tensor_by_name("X:0")
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
            
#             # There are TWO options how to get activation operation:
#               # FROM SAVED COLLECTION:            
#             self.activation = tf.get_collection('activation')[0]
#               # BY NAME:
#             self.activation = self.graph.get_operation_by_name('activation_opt').outputs[0]

    def run(self, data, s):
        if s == 2:
            x = 2
        if s == 3:
            x = 2
        if s == 9:
            x = 9

        """ Running the activation operation previously imported """
        # The 'x' corresponds to name of input placeholder
        y_hat = self.sess.run(self.y, feed_dict={"X:0": data, self.keep_prob: 1.0})
        
        length = len(y_hat)
        ans_list = np.zeros(shape = [x], dtype = np.float32)
        
        for num in range(length):
          ans_list = ans_list + y_hat[num]
          
        ans_list /= num
        ans = np.argmax(ans_list, 0)
        max_value = ans_list[ans]
        
        #f = open("/home/ubuntu/code/out.txt", "a")
        
        #for i in range(x):
            #f.write(str(ans_list[i]) + "\t")
        #f.write("\n" + str(ans_list[ans]) + "\n")
        #f.close()

        if s == 9:
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
          if ans == 5:
            output = '오늘날씨'
          if ans == 6:
            output = '오늘일정'
          if ans == 7:
            output = '지니야'
          if ans == 8:
            output = '클로바'
        if s == 2:
          if ans == 0:
            output = '소리작게'
          if ans == 1:
            output = '소리크게'
        if s == 3:
          if ans == 0:
            output = '오늘날씨'
          if ans == 1:
            output = '오늘일정'
            
        return output, ans_list, ans, max_value

### Using the class ###
dirname = '/home/ubuntu/'
n = 39

main_model_path = dirname + 'model/model.ckpt'
sound_model_path = dirname + 'model/소리_작게크게/model_two'
day_model_path = dirname + 'model/오늘_날씨일정/model_today'
input_path = '/home/ubuntu/sound_data/record/test_data/'

#input_path = '/var/www/html/input.wav'

#data = np.ndarray(shape = [0, n], dtype = np.float32)
#feature = extract_feature(input_path)
#data = np.append(feature, data, axis = 0)

m = 0

for i in range(9):

    l = i

    if i == 0:
        dirname = '뉴스'
    if i == 1:
        dirname = '리모컨'
    if i == 2:
        dirname = '소리작게'
        l = 0
    if i == 3:
        dirname = '소리크게'
        l = 1
    if i == 4:
        dirname = '시간'
    if i == 5:
        dirname = '오늘날씨'
        l = 0
    if i == 6:
        dirname = '오늘일정'
        l = 1
    if i == 7:
        dirname = '지니야'
    if i == 8:
        dirname = '클로바'

    n = 0

    for j in range(30):
        #data = np.load(input_path + dirname + '/%d.npz'%j)
        data = extract_feature(input_path + dirname + '/%d.wav'%j)

        model = ImportGraph(main_model_path)
        result, ans_list_, ans_, max_value = model.run(data, 9)
        c = 0

        if result == '소리작게' or result == '소리크게':
            model_ = ImportGraph(sound_model_path)
            result, ans_list, ans, max_value = model_.run(data, 2)
            c = 1
        if result == '오늘날씨' or result == '오늘일정':
            model_ = ImportGraph(day_model_path)
            result, ans_list, ans, max_value = model_.run(data, 3)
            c = 1

        if max_value < 0.3:
            result = '잘 모르겠어요!'
                
        print(dirname + ' ' + result)

        f_name = "/home/ubuntu/static/ans_hypo_max.txt"
        
        f = open(f_name, "a")
        write = dirname + ' ' + result + " %f" %max_value
        f.write(write + "\n")
        f.close()

        if dirname == result:
        #    f = open(f_name, "a")
        #    if c == 0:
        #        f.write(str(ans_list_[ans_]) + "\t" + str(ans_list_[l])  + "\r")
        #    if c == 1:
        #        f.write(str(ans_list_[ans_]) + "\t" + str(ans_list_[l]) + "\r")
        #    f.close()

            m = m + 1
            n = n + 1
    print('일치: %d'%n)
print('전체: %d'%m)

#out_file = open('/var/www/html/new.php', 'w')
#out_file.write(result)
