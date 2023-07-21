
import cv2
import numpy as np
def nothing(x):
    pass

cv2.namedWindow("tracking")
cv2.createTrackbar("image_size",'tracking',2,4,nothing,)
cv2.createTrackbar("median_blur",'tracking',1,10,nothing)
cv2.createTrackbar("edge_preserve",'tracking',0,50,nothing)
cv2.createTrackbar("bilaterdal_sigma",'tracking',0,10,nothing)
cv2.createTrackbar("addweights_alpha",'tracking',1,10,nothing)
cv2.createTrackbar("addweights_gamma",'tracking',1,10,nothing)

while True:
#-----------------Phase 1
#Readin the image
    image = cv2.imread('WhatsApp Image 2023-07-14 at 12.22.02 AM.jpeg')
    image_size= cv2.getTrackbarPos('image_size','tracking')
    median_blur = cv2.getTrackbarPos('median_blur', 'tracking')
    edge_preserve = cv2.getTrackbarPos('edge_preserve', 'tracking')

    bilaterdal_sigma = cv2.getTrackbarPos('bilaterdal_sigma', 'tracking')
    addweights_alpha = cv2.getTrackbarPos('addweights_alpha','tracking')
    addweights_gamma = cv2.getTrackbarPos('addweights_gamma','tracking')
#resizing the image
#Interpolation is cubic for best results
    image_resized = cv2.resize(image, None, fx=.25*image_size, fy=.25*image_size)



#-----------------Phase 2
#removing impurities from image
    if median_blur%2==0:
        median_blur=median_blur+1
        image_cleared = cv2.medianBlur(image_resized, median_blur)
        image_cleared = cv2.medianBlur(image_cleared, median_blur)
        image_cleared = cv2.medianBlur(image_cleared, median_blur)
    else:
        image_cleared = cv2.medianBlur(image_resized, median_blur)
        image_cleared = cv2.medianBlur(image_cleared, median_blur)
        image_cleared = cv2.medianBlur(image_cleared, median_blur)


    image_cleared = cv2.edgePreservingFilter(image_cleared, sigma_s=0.5*edge_preserve)




#-----------------Phase 3
#Bilateral Image filtering
    image_filtered = cv2.bilateralFilter(image_cleared, 3, 0.5*bilaterdal_sigma, 2,)

    for i in range(2):
	    image_filtered = cv2.bilateralFilter(image_filtered, 3, 0.5*bilaterdal_sigma, 12)

    for i in range(3):
        image_filtered = cv2.bilateralFilter(image_filtered, 5, 0.5*bilaterdal_sigma, 12)

# for i in range(3):
# 	image_filtered = cv2.bilateralFilter(image_filtered, 5, 40, 10)

# for i in range(2):
# 	image_filtered = cv2.bilateralFilter(image_filtered, 3, 40, 5)




#--------------------------Phase 4
#Sharpening the image using addWeighted()
    gaussian_mask= cv2.GaussianBlur(image_filtered, (7,7), 12,19)
    image_sharp = cv2.addWeighted(image_filtered, 0.1*addweights_alpha, gaussian_mask, 0.1*addweights_gamma, 0)
    image_sharp = cv2.addWeighted(image_sharp, 0.1*addweights_alpha, gaussian_mask, 0.1*addweights_gamma, 10)





#displayng images
    cv2.imshow('Final Image', image_sharp)
    #cv2.imshow('Clear impurities', image_cleared)
    cv2.imshow('original', image_resized)
#cv2.imwrite('art_test1.jpg', image_sharp)
    c = cv2.waitKey(1) & 0xFF
    if c == 27:
        break

cv2.destroyAllWindows()