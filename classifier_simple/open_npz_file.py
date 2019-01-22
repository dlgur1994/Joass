import numpy as np

data = load('desktop/mfcc_train/0.npz')
lst = data.files
for item in lst:
    print(item)
    print(data[item])
