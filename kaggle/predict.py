import numpy as np
import os
import random
from ipywidgets import interact

# from tensorflow.keras import layers
from tensorflow.keras import models
# from tensorflow.keras import optimizers

# from tensorflow.keras.utils import plot_model
# from tensorflow.keras import backend

from matplotlib import pyplot as plt
from PIL import Image

# For confusion matrix
import seaborn as sn
import pandas as pd
from sklearn.metrics import confusion_matrix

def files_in_folder(folder_path):
    return os.listdir(folder_path)


# Load the model
conv_model = models.load_model("kaggle_astro_model.h5") # .keras is new format (but not noticibly faster)
# conv_model = models.load_model("kaggle_astro_model.h5") # .h5 is old file format

'''~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Load the test images
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'''

dataPath = "data"
galaxyPath = dataPath + "/test_galaxy"
starPath = dataPath + "/test_star"

galaxyImageFileNames = files_in_folder(galaxyPath)
starImageFileNames = files_in_folder(starPath)

testImages = []
numTotalImages = len(galaxyImageFileNames) + len(starImageFileNames)
imagesLoaded = 0

for file in galaxyImageFileNames:
    testImages.append([np.array(Image.open(f'{galaxyPath}/{file}'))[:, :, 0], np.array([0, 1])])
    # Note ^ only need 0'th color channel since all channels are the same
    imagesLoaded += 1
    if imagesLoaded % 50 == 0:
        print("Loaded {} of {} images; {}% complete.".format(imagesLoaded,
                                                             numTotalImages, round(100*imagesLoaded/numTotalImages, 1)))

print("Done loading test galaxies.")
for file in starImageFileNames:
    testImages.append([np.array(Image.open(f'{starPath}/{file}'))[:, :, 0], np.array([1, 0])])
    imagesLoaded += 1
    if (imagesLoaded % 50 == 0):
        print("Loaded {} of {} images; {}% complete.".format(imagesLoaded,
                                                             numTotalImages, round(100*imagesLoaded/numTotalImages, 1)))
print("Done loading test stars.")

# Shuffle and separate into data and answers
random.shuffle(testImages)
onlyTestImages = np.stack([entry[0] for entry in testImages])
testAnswers = np.stack([entry[1] for entry in testImages])

print(testAnswers.shape)
print(onlyTestImages.shape)

'''~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Make predictions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'''

predictions_raw = conv_model.predict(onlyTestImages, use_multiprocessing=True)
predictions_old = np.argmax(predictions_raw, axis=1)
Y_dataset_1D = np.argmax(testAnswers, axis=1)

# If high confidence of star, pick star, otherwise pick galaxy
predictions = []
THRESH = 0.7

for index in range(len(predictions_old)):
    if predictions_raw[index][0] > THRESH:
        predictions.append(0)
    else:
        predictions.append(1)

predictions = np.array(predictions)

galaxyNumber = 0
starNumber = 0
totalGalaxyConfidence = 0
totalStarConfidence = 0

for index in range(len(predictions_old)):
    if Y_dataset_1D[index] == 1: # Since index 1 is where you find the value of 1 in the answer vector representing galaxy
        star_or_galaxy = "galaxy."
        galaxyNumber += 1
        totalGalaxyConfidence += predictions_raw[index][1]
    else:
        star_or_galaxy = "star.  "
        starNumber += 1
        totalStarConfidence += predictions_raw[index][0]

print("What is the average confidence in the correct answer, based on the ground truth of the image?")
print("Star:   {}%".format(round(100*totalStarConfidence/starNumber, 1)))
print("Galaxy: {}%".format(round(100*totalGalaxyConfidence/galaxyNumber, 1)))

# Plot Confusion matrix
conf_mat = confusion_matrix(Y_dataset_1D, predictions)

df_cm = pd.DataFrame(conf_mat, index = [i for i in ["star", "galaxy"]],
                  columns = [i for i in ["star", "galaxy"]])
plt.figure(figsize = (4, 4))
plt.title("actual on y axis\n predicted on x-axis")
plt.xlabel("predicted")
plt.ylabel("actual")
sn.heatmap(df_cm, annot=True)

print(conf_mat)