import astropy.io.fits as fits
import cv2
import matplotlib.pyplot as plt
import numpy as np
import math

# filePath = "access_FITS\hlsp_appp_hst_wfpc2_sfd-pu4k2ho01_f606w_v2_sci_drz.fits"
# filePath = "access_FITS/sdss_dr_12_data_v1/frame-g-007778-5-0267.fits.bz2"
# filePath = "access_FITS/sdss_dr_12_data_v1/frame-g-000756-2-0471.fits.bz2"
filePath = "access_FITS/sdss_dr_12_data_v1/frame-g-003628-1-0036.fits.bz2"

info = fits.open(filePath) # This seems to only get the 'header info'
print(info)
print()

data = fits.getdata(filePath)
print(type(data))
print(type(data[100][100]))
print()
print(data.shape)

maximum = -1
minimum = 1
for row in range(data.shape[0]):
    maximum = max(maximum, max(data[row]))
    minimum = min(minimum, min(data[row]))
    
print("Max: {}. Min: {}.".format(maximum, minimum))

new_arr = np.zeros(data.shape)
for row in range(data.shape[0]):
    for col in range(data.shape[1]):
        new_arr[data.shape[0] - 1 - row][col] = ((data[row][col] - minimum)/(maximum - minimum))**(0.2)


# Linear scaling:
# for row in range(data.shape[0]):
#     for col in range(data.shape[1]):
#         data[row][col] = int(255*(data[row][col] - minimum)/(maximum - minimum))

# Logarithmic scaling?

# Manual binary mask (Doesn't work)
# for row in range(data.shape[0]):
#     for col in range(data.shape[1]):
#         val = data[row][col]
#         # data[row][col] = np.fabs(0.9) if (val > 0.07) else np.fabs(0.1)
#         # data[row][col] = 1-val
#         data[row][col] = np.int32(0.99) if val > 0.07 else np.int32(0.01)
        
# print(type(data[100][100])) # Still np.float32 even when I try to change it

# Draw circle for test

# circleCentre = (400, 400)
# circleThickness = 1000
# circleRadius = 100

# for row in range(data.shape[0]):
#     for col in range(data.shape[1]):
        
#         if abs((row - circleCentre[0])**2 + 0.5*(col - circleCentre[1])**2 - circleRadius **2) < circleThickness:
#             data[row][col] = int(255)


# Binary masking
# data = cv2.inRange(src=data, lowerb=0.07, upperb=30)


print(type(new_arr[100][100]))

resized_image = cv2.resize(new_arr, (0,0), fx=0.5, fy=0.5)
cv2.imshow("data", resized_image)
cv2.waitKey(0)
