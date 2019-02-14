#_*_coding: utf-8_*_

'''
181107 이은상 소리 data
뉴스, 리모컨, 소리작게, 소리크게, 시간, 오늘날씨, 오늘일정, 지니야, 클로바
각각 70번
'''

import numpy as np

tc = []
td = []

N = 39#dimension size - 각 행의
classes = 5#number of commands
ans = [0,0,0,0,0]
#ans = [0,0,0,0,0,0,0,0,0]

dirname = '/gdrive/My Drive/18-winter/내목소리/data/20/'

for i in range(classes):
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

  f = np.load(dirname + filename + ".npz")#load file
  
  #label
  ans = [0,0,0,0,0]
  ans[i] = 1
  
  #length of X
  num = len(f['X'])
  print(num)
    
  #td = label
  for m in range(num):
    if i == 0:
      if m == 0:
        td = np.array(ans)
      else:
        td = np.vstack([td, ans])
    else:
      td = np.vstack([td, ans])
      
  if i == 0:
    tc = f['X']
  else:
    tc = np.vstack([tc, f['X']])

  tc = tc.astype(np.float32)
  td = td.astype(np.float32)
  
  print("tc %d"%len(tc))
  print("td %d"%len(td))
  
np.savez(dirname + "data", X = tc, Y = td)#npz 파일 이름 저장
  
print("finish")
