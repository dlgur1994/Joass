import numpy as np

tc = []
for i in range(5):
    tc.append(0)
    
for j in range(5):
    tc.append(1)

np.savez('desktop/mfcc_y_test/test_y_data', tc)
