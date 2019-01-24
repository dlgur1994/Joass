import glob
import librosa
import numpy as np


def extract_feature(file_name):
    X, sample_rate = librosa.load(file_name)
    mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T,axis=0)
    return mfccs

def parse_audio_files(filenames):
    rows = len(filenames)
    features = np.zeros((rows,193))
    i = 0
    for fn in filenames:
        try:
            mfccs = extract_feature(fn)
            ext_features = np.hstack([mfccs])
        except:
            print(fn)
        else:
            features[i] = ext_features
            i += 1
    return features

audio_files = []
for i in range(0,50):
    audio_files.extend(glob.glob('train/%d.wav' % i))

print(len(audio_files))
for i in range(50):
    files = audio_files[i*1000: (i+1)*1000]
    X = parse_audio_files(files)
    np.savez('desktop/mfcc_train/%d' % i, X=X)
