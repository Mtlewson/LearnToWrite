import cv2
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

painting = "starry_night"

image = cv2.imread("../data/source/"+painting+".jpg")
#image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
print(image.shape) # shape of image (width x height x RGB channels)

pixel_values = image.reshape((-1, 3))
print(pixel_values.shape) # converted to a flat dimension x color channels
# convert to float
pixel_values = np.float32(pixel_values)

print(pixel_values[0])

# when to stop the algorithm
# cv.TERM_CRITERIA_EPS - stop the algorithm iteration if specified accuracy, epsilon, is reached.
# cv.TERM_CRITERIA_MAX_ITER - stop the algorithm after the specified number of iterations, max_iter.
# cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER - stop the iteration when any of the above condition is met.
# so criteria = (when to stop, number of iterations, accuracy)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 1000, 0.9)
k = 10 # number of clusters to make

# cv2.kmeans(input data, cluster count, None, criteria, algorithm reruns, initial placement)
_, labels, (centers) = cv2.kmeans(pixel_values, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
# convert back to 8 bit values
centers = np.uint8(centers) # these are the mean colors of each cluster of pixels
print(centers)

# write palette of center colors to another file
blank_image = np.zeros((50*k,50*k,3), np.uint8)
blank_image.fill(255)

counter = 0
for i in centers:
    c = list(i)
    c = [int(i) for i in c]
    #c.reverse() # no idea why but it works
    c = tuple(c)
    blank_image = cv2.rectangle(blank_image,(counter,0),(counter+50,50*k),c,-1)
    counter+=50

cv2.imwrite("../data/segmented/"+painting+"/centers.jpeg", blank_image)



# flatten the labels array
labels = labels.flatten() # go from [X,1] to [X]

#segmented_image = centers[labels.flatten()]
#segmented_image = segmented_image.reshape(image.shape)

# color (i.e cluster) to disable
for i in range(k):
    masked_image = np.copy(image)
    masked_image = masked_image.reshape((-1, 3)) # convert to the shape of a vector of pixel values
    # for each cluster, make all other pixels white and then store as separate image
    cluster = i
    masked_image[labels != cluster] = [255, 255, 255]
    # convert back to original shape
    masked_image = masked_image.reshape(image.shape)
    cv2.imwrite("../data/segmented/"+painting+"/img_cluster_"+str(i)+".jpeg",masked_image)
    # show the image
    #plt.imshow(masked_image)
    #plt.show()


print(Counter(labels))
