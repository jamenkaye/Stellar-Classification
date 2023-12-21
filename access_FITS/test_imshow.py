import cv2
import numpy as np


data = np.random.rand(800, 800)
print(type(data[100][100]))

circleCentre = (400, 400)
circleThickness = 1000
circleRadius = 100

for row in range(data.shape[0]):
    for col in range(data.shape[1]):
        
        data[row][col] = 0 if data[row][col] < 0.2 else 1
        
        if abs((row - circleCentre[0])**2 + 0.25*(col - circleCentre[1])**2 - circleRadius **2) < circleThickness:
            data[row][col] = 0

maximum = -1
minimum = 1
for row in range(data.shape[0]):
    maximum = max(maximum, max(data[row]))
    minimum = min(minimum, min(data[row]))
    
print("Max: {}. Min: {}.".format(maximum, minimum))


cv2.imshow("Image", data)
cv2.waitKey(0)