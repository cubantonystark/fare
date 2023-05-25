import cv2
import os, glob
source_dir = 'C:\\Users\\escam\\Pictures\\imagery\\underwater_tests\\coral_formation\\images\\'

if not os.path.exists('C:\\Users\\escam\\Pictures\\imagery\\underwater_tests\\coral_formation\\cropped'):
    
    os.mkdir('C:\\Users\\escam\\Pictures\\imagery\\underwater_tests\\coral_formation\\cropped')

arr = glob.glob(source_dir+'*.png')

print(arr)

for itr in arr:
    
    try:
        
        img = cv2.imread(itr)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        _,thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
        x,y,w,h = cv2.boundingRect(thresh)

        crop = img[y:y+h,x:x+w]    
        cv2.imwrite(itr.replace('images', 'cropped'),crop) 
        print('Processed: '+str(itr))
        
    except:
        
        continue