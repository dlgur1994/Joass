import librosa
import numpy as np

def extract_feature(file_name):
    X, sr = librosa.load(file_name)
    mfccs = librosa.feature.mfcc(y=X, sr=sr, n_mfcc=39, hop_length=int(sr*0.01), n_fft=int(sr*0.02)).T
    return mfccs

n = 39#n을 39로 해야하는가???
#dirname = '/gdrive/My Drive/조아쓰/자료조사/2018-08-13 녹음/이은상/'
dirname = '/gdrive/My Drive/18-winter/내목소리/data/20/'

for i in range(5):
  if i == 0:
    filename = "뉴스20"
  if i == 1:
    filename = "리모컨20"
  if i == 2:
    filename = "소리작게20"
  if i == 3:
    filename = "소리크게20"
  if i == 4:
    filename = "시간20"

  f = dirname + filename + '.wav'#load file  
  all_mfccs = np.ndarray(shape = [0,n], dtype = np.float32)
  feature = extract_feature(f)

  all_mfccs = np.append(all_mfccs, feature, axis = 0)
  np.savez(dirname + filename + '.npz', X = all_mfccs)

  print(i)
