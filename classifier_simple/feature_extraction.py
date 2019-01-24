import librosa #음성 추출을 위한 library librosa
import numpy as np #python에서 행렬을 다루는 library numpy를 np로 import
def extract_feature(file_name):
    X, sr = librosa.load(file_name)
    mfccs = librosa.feature.mfcc(y=X, sr=sr, n_mfcc=39, hop_length=int(sr*0.01), n_fft=int(sr*0.02)).T
    return mfccs

'''
function extract_feature: file 이름을 받아서 특징을 추출하는 함수
audio file을 floating time seriese로 load
(sr = sampling rate, default = 22050)
load한 file을 mfcc를 통해 특징 추출. return할 mfcc의 개수 39개
return mfccs: [N][39] size의 numpy(행렬)
'''

n_files = 50 #load할 audio file 개수
n = 39 #column 개수

#총 50개의 file을 feature 추출한다.
for i in range(n_files):
    all_mfccs = []
    files = ('desktop/train/%d.wav'%i) #feature 추출할 .wav 파일의 위치
    
    all_mfccs = np.ndarray(shape=[0, n], dtype = np.float32)
    feature = extract_feature(files) #file에서 특징 추출한 feature
    
    all_mfccs = np.append(all_mfccs, feature, axis=0)
    np.savez('desktop/mfcc_train/%d'%i, X = all_mfccs) #추출한 feature, numpy 행렬으로 저장
    
    print(i,"file")
