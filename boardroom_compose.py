import numpy as np
import cv2
import sys
import matplotlib.pyplot as plt

def adjust_gamma(image, gamma=1.0):

   invGamma = 1.0 / gamma
   table = np.array([((i / 255.0) ** invGamma) * 255
      for i in np.arange(0, 256)]).astype("uint8")

   return cv2.LUT(image, table)

gamma = 0.8                                   # change the value here to get different result

try:
    img = cv2.imread('board.png',cv2.IMREAD_COLOR)
except:
    print('exception thrown while opening image')                 

if img is None:
    print('image is none.')             
    print('Error opening image.')
    sys.exit(0)


#cv2.blur(img,(13,13))
img = cv2.GaussianBlur(img,(3,3),0)
img = cv2.bilateralFilter(img,7,25,25)
img = adjust_gamma(img,gamma=gamma)

rows,cols,ch = img.shape
#print('Image size: ', rows, ' by ', cols)

RGB_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#img = RGB_img

srcRect = np.float32([[0,0],[cols,0],[0,rows],[cols,rows]]) 
destRect = np.float32([[620,143],[1519,219],[623,793],[1517,736]]) 

M = cv2.getPerspectiveTransform(srcRect,destRect)

dst = cv2.warpPerspective(img,M,(1920,1080))

#cv2.imwrite('output.png', dst)

#plt.subplot(121),plt.imshow(RGB_img),plt.title('Input')
#plt.plot(0,0,'ro')
#plt.plot(cols,0,'ro')
#plt.plot(0,rows,'ro')
#plt.plot(cols,rows,'ro')
#plt.axis('off')
#plt.subplot(122),plt.imshow(dst),plt.title('Output')

bg = cv2.imread('boardroom 01.jpg')
bg_rgb = cv2.cvtColor(bg, cv2.COLOR_BGR2RGB)
#
#out = bg_rgb + dst
#out = cv2.bitwise_and(bg, dst)

#dst_gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
#ret, mask = cv2.threshold(dst_gray, 1, 255, cv2.THRESH_BINARY)
#cv2.imwrite('temp.png', mask)
mask = np.zeros(dst.shape[:2],np.uint8)
#bgdModel = np.zeros((1,65),np.float64)
#fgdModel = np.zeros((1,65),np.float64)

#rect = (1108,283,1703,1080)
#cv2.grabCut(dst,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)
roi_corners = np.array([[(620,143), (1519,219), (1517,736),(623,793)]], dtype=np.int32)
channel_count = dst.shape[2]  # i.e. 3 or 4 depending on your image
ignore_mask_color = (255,)*channel_count
cv2.fillPoly(mask, roi_corners, ignore_mask_color)

ret, mask = cv2.threshold(mask, 1, 255, cv2.THRESH_BINARY)
mask_inv = cv2.bitwise_not(mask)
dst_out = cv2.bitwise_and(dst,dst,mask = mask)
bg_out = cv2.bitwise_and(bg,bg,mask=mask_inv)
combined = cv2.add(dst_out,bg_out)


#cv2.imwrite('mask.png', mask)
#cv2.imwrite('combined.png',combined)

fg = cv2.imread('fg_mask_rob.png',0)
ret, fgmask = cv2.threshold(fg, 1, 255, cv2.THRESH_BINARY)
fgmask_inv = cv2.bitwise_not(fgmask)
combined = cv2.bitwise_and(combined,combined,mask=fgmask_inv)
fgimg = cv2.bitwise_and(bg,bg,mask=fgmask)
final = cv2.add(combined,fgimg)

cv2.imwrite('final.jpg',final)



##plt.show()