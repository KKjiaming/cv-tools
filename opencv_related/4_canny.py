import cv2 as cv
from matplotlib import pyplot as plot
from cv2 import equalizeHist
# helper function to easily display our images
def img_show(title, image):
    plot.title(title)
    plot.xticks([])
    plot.yticks([])
    plot.imshow(image, cmap="gray")
    plot.show()

# read in our original image as grayscale
img = cv.imread(r"threshold_problem\2165.012906_2022-12-07_15-39-05-765.jpg")
img = cv.cvtColor(img,cv.COLOR_BGR2GRAY)

img = equalizeHist(img)



# show grayscale image using our helper function
img_show("Grayscale Image", img)


# blurring the image with a 5x5, sigma = 1 Guassian kernel
img_blur = cv.GaussianBlur(img, (5, 5), 1)

# obtaining a horizontal and vertical Sobel filtering of the image
img_sobelx = cv.Sobel(img_blur, cv.CV_64F, 1, 0, ksize=3)
img_sobely = cv.Sobel(img_blur, cv.CV_64F, 0, 1, ksize=3)

# image with both horizontal and vertical Sobel kernels applied
img_sobelxy = cv.addWeighted(cv.convertScaleAbs(img_sobelx), 0.5, cv.convertScaleAbs(img_sobely), 0.5, 0)

# finally, generate canny edges
# extreme examples: high threshold [900, 1000]; low threshold [1, 10]
img_edges = cv.Canny(img, 50, 100)

img_show("img_edges", img_edges)
