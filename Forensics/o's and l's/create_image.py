from PIL import Image
import numpy as np
import cv2
f = open('chall.txt', 'r')

x = []
while True:
    a = f.readline()
    if not a:
        break
    a = a[:len(a)-1]
    a = a.split(' ')
    tmp = []
    for i in a:
        if i == 'o':
            tmp.append(0)
        else:
            tmp.append(1)

    x.append(tmp)

x = np.array(x)
img = Image.new('1', (300, 300))
pix = img.load()

for i in range(x.shape[0]):
    for j in range(x.shape[1]):
        pix[i, j] = int(x[i][j])

img.show()
