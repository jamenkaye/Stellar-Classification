import astropy.io.fits as fits
import cv2

filePath = "access_FITS\hlsp_appp_hst_wfpc2_sfd-pu4k2ho01_f606w_v2_sci_drz.fits"

info = fits.open(filePath) # This seems to only get the 'header info'
print(info)
print()

data = fits.getdata(filePath)
print(type(data))
print()
print(data.shape)

maximum = -1
minimum = 1
for row in range(data.shape[0]):
    maximum = max(maximum, max(data[row]))
    minimum = min(minimum, min(data[row]))
    
print("Max: {}. Min: {}.".format(maximum, minimum))


resized_image = cv2.resize(data, (0,0), fx=0.5, fy=0.5)
cv2.imshow("data", resized_image)
cv2.waitKey(0)
