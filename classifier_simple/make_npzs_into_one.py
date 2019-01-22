#_*_coding: utf-8_*_
import numpy as np
n = 50
tc = []

'''
서로 다른 mfcc폴더에 저장되어 있는 npz를 하나의 npz로 모으는 것.
'''

N = 39
for i in range(n):
    filename = (r'desktop/mfcc_train/%d.npz'%i)
    f = np.load(filename, 'r')
    print('%d file'%i)
    num = f['X'].shape[0]

    for m in range(num):
        line = f['X'][m]
        narr = []
        for j in range(N):
            s_n = str(line[j]).split()
            s_n[0] = s_n[len(s_n)-1][:-1]
            for numb in s_n:
                if numb == '':
                    continue
                narr.append(float(numb))
            tc.append(narr)
        f.close

tc = np.array(tc)
tc = tc.astype(np.float32)
f.close()

np.savez('desktop/mfcc_train_final/train_data', X = tc)
#전체 set을 합친 npz 파일 저장
