import cv2
import numpy as np
from matplotlib import pyplot as plt

# TODO: make function accept a list of templates, return multiply match_count/exp_match_count * treshold to give assurance
# make run with variable treshold


def findTemplate(templ_path, addit_templ_path, surf_path, with_rotation = False, treshold = 0.80):
    tresh = treshold
    
    img_rgb = cv2.imread(surf_path)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(templ_path,0)
    template2 = cv2.imread(addit_templ_path, 0)
    w, h = template.shape[::-1]
    w2, h2 = template.shape[::-1]
    
    resFlip = None    
    if with_rotation:
        template_flip = cv2.flip(template, 0)
        resFlip = cv2.matchTemplate(img_gray, template_flip, cv2.TM_CCOEFF_NORMED)

    res = cv2.matchTemplate(img_gray, template, cv2.TM_SQDIFF_NORMED) #TM_CCOEFF_NORMED
    
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    print("min_val: " + str(min_val) + "; max_val" + str(max_val) + "; min loc:" + str(min_loc) + "; max loc:" + str(max_loc))
    
    # Calculate the similarity percentage of the matched template image
    # 
    # if max_val >= threshold:
    
    similarity = round(max_val * 100, 2)  
    print("best similarity: " + str(similarity))  
    
    loc = np.where( res >= tresh)
    count = 0
    for pt in zip(*loc[::-1]):
        (x,y) = pt[::-1]
        print("$$$ " + str(res[0][0]) + "/ " + str(res[1][0]))
        print("## " + str(x) + "_" + str(y) + " -- for " + str(pt))
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,111,255), 1)
        count += 1
    
    if resFlip is not None:
        loc = np.where(resFlip >= tresh)
    for pt in zip(*loc[::-1]):
        (x,y) = pt[::-1]
        print("## " + str(x) + "_" + str(y) + " -- for " + str(pt))
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (111,0,255), 1)
        count += 1

    return img_rgb, count

input_image_path = 'C:/Users/plus3/OneDrive/Desktop/cards/default/1440/images/rank_a.png'
input_image_path2 = 'C:/Users/plus3/OneDrive/Desktop/cards/default/1440/images/suit_spade.png'
input_image_surf = 'C:/Users/plus3/OneDrive/Desktop/cards/default/1440/cache/As.png'

img_rgb, count = findTemplate(input_image_path, input_image_path2, input_image_surf, True)   


cv2.imwrite('res.png',img_rgb)
cv2.imshow('contoh.jpg', img_rgb)
cv2.waitKey(0) &0xFF
print("Match count: " + str(count))
 
cv2.destroyAllWindows()
