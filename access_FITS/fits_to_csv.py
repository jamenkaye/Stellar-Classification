import astropy.io.fits as fits
from datetime import datetime


# filePath = "access_FITS\hlsp_appp_hst_wfpc2_sfd-pu4k2ho01_f606w_v2_sci_drz.fits"
# filePath = "access_FITS/sdss_dr_12_data_v1/frame-g-007778-5-0267.fits.bz2"
# filePath = "access_FITS/sdss_dr_12_data_v1/frame-g-000756-2-0471.fits.bz2"
filePath = "access_FITS/sdss_dr_12_data_v1/frame-g-003628-1-0036.fits.bz2"

info = fits.open(filePath) # This seems to only get the 'header info'
print(info)
print()

data = fits.getdata(filePath)
print(type(data))
print()
print(data.shape)

# File name for data file - these will be unique so I don't need to manually rename :)
dataFileName = datetime.now().strftime('%Y-%m-%d_%H_%M_%S') + "_data.csv"

# create and open the data file
file = open("access_FITS/sdss_dr_12_data_v1/csv_data/" + dataFileName, "w+")
file.write(filePath + "\n")

maximum = -1
minimum = 1

for row in range(data.shape[0] - 1, -1, -1):
    maximum = max(maximum, max(data[row]))
    minimum = min(minimum, min(data[row]))
    rowStr = ""
    
    for col in range(data.shape[0]):
        value = data[row][col]
        
        if value < 0.05:
            value = 0
        
        rowStr += str(value) + ","
        
    file.write(rowStr + "\n")
    
print("Max: {}. Min: {}.".format(maximum, minimum))
