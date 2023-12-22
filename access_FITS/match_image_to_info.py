import astropy.io.fits as fits
import cv2
import matplotlib.pyplot as plt
import numpy as np

filePath = "access_FITS/sdss_dr_12_data_v1/frame-g-003628-1-0036.fits.bz2"

info = fits.open(filePath) # This seems to only get the 'header info'
data = fits.getdata(filePath)
print(info)
print()
print("Data: {}. Data point: {}".format(type(data), type(data[100][100])))
print(data.shape)

# maximum = -1
# minimum = 1
# for row in range(data.shape[0]):
#     maximum = max(maximum, max(data[row]))
#     minimum = min(minimum, min(data[row]))
    
# print("Max: {}. Min: {}.".format(maximum, minimum))

def brightness_map(input_brightness):
    # Takes a brightness from the image and maps it to a value between 0 and 1 for cv2.imshow()
    # Input is any real number.
    # This is designed for ~exponential data where values are often near zero, but are often around 1,
    # and sometimes up to ~20 or ~200
    return 1 - 1/(1.5*input_brightness + 1)

new_arr = np.zeros(data.shape)
for row in range(data.shape[0]):
    for col in range(data.shape[1]):
        new_arr[data.shape[0] - 1 - row][col] = brightness_map(data[row][col])

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

# circleCentre = (350, 950)
# circleThickness = 1000
# circleRadius = 100

# for row in range(new_arr.shape[0]):
#     for col in range(new_arr.shape[1]):
        
#         if abs((row - circleCentre[0])**2 + (col - circleCentre[1])**2 - circleRadius **2) < circleThickness:
#             new_arr[row][col] = int(255)


# Draw bounding bars
squareCentreSDSS = (1290, 930)
squareCentreToEdge = 20
squareBorder = 10

squareCentre = (data.shape[0] - squareCentreSDSS[0], squareCentreSDSS[1])

new_arr[(squareCentre[0] - squareCentreToEdge):(squareCentre[0] + squareCentreToEdge), 
        (squareCentre[1] - squareCentreToEdge - squareBorder):(squareCentre[1] - squareCentreToEdge)] = 1

new_arr[(squareCentre[0] - squareCentreToEdge):(squareCentre[0] + squareCentreToEdge), 
        (squareCentre[1] + squareCentreToEdge):(squareCentre[1] + squareCentreToEdge + squareBorder)] = 1

new_arr[1000:200, 100:200] = 1

resized_image = cv2.resize(new_arr, (0,0), fx=0.5, fy=0.5)
cv2.imshow("data", resized_image)
cv2.waitKey(0)
