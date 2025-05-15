# Image Segmentation with Watershed Algorithm – OpenCV Python - GeeksforGeeks

Image segmentation is a fundamental computer vision task that involves partitioning an image into meaningful and semantically homogeneous regions. The goal is to simplify the representation of an image or make it more meaningful for further analysis. These segments typically correspond to objects or regions of interest within the image.

## Watershed Algorithm

The Watershed Algorithm is a classical image segmentation technique that is based on the concept of watershed transformation.The segmentation process will take the similarity with adjacent pixels of the image as an important reference to connect pixels with similar spatial positions and gray values.

### ****When do I use the watershed algorithm?****

The Watershed Algorithm is used when segmenting images with touching or overlapping objects. It excels in scenarios with irregular object shapes, gradient-based segmentation requirements, and when marker-guided segmentation is feasible.

### Working of Watershed Algorithm

The watershed algorithm divides an image into segments using topographic information. It treats the image as a topographic surface, identifying catchment basins based on pixel intensity. Local minima are marked as starting points, and flooding with colors fills catchment basins until object boundaries are reached. The resulting segmentation assigns unique colors to regions, aiding object recognition and image analysis.

The whole process of the watershed algorithm can be summarized in the following steps:

*   ****Marker placement:**** The first step is to place markers on the local minima, or the lowest points, in the image. These markers serve as the starting points for the flooding process.
*   ****Flooding****: The algorithm then floods the image with different colors, starting from the markers. As the color spreads, it fills up the catchment basins until it reaches the boundaries of the objects or regions in the image.
*   ****Catchment basin formation****: As the color spreads, the catchment basins are gradually filled, creating a segmentation of the image. The resulting segments or regions are assigned unique colors, which can then be used to identify different objects or features in the image.
*   ****Boundary identification****: The watershed algorithm uses the boundaries between the different colored regions to identify the objects or regions in the image. The resulting segmentation can be used for object recognition, image analysis, and feature extraction tasks.

## Implementing the watershed algorithm using OpenCV

OpenCV (Open Source Computer Vision Library) is an open-source computer vision and machine learning software library. OpenCV contains hundreds of computer vision algorithms, including object detection, face recognition, image processing, and machine learning.

Here are the implementation steps for the watershed Algorithm using OpenCV:

#### Import the required libraries

`import cv2 import numpy as np from IPython.display import Image, display from matplotlib import pyplot as plt`

#### Loading the image

We define a function "imshow" to display the processed image. The code loads an image named "coin.jpg".

`# Plot the image def imshow(img, ax=None):     if ax is None:         ret, encoded = cv2.imencode(".jpg", img)         display(Image(encoded))     else:         ax.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))         ax.axis("off")  #Image loading img = cv2.imread("Coins.png") # Show image imshow(img)`

Input coin

#### Coverting to Grayscale image

We convert the image to grayscale using OpenCV's "cvtColor" method. The grayscale image is stored in a variable "gray".

****Output:****

The cv2.cvtColor() function takes two arguments: the image and the conversion flag cv2.COLOR_BGR2GRAY, which specifies the conversion from BGR color space to grayscale.

#### Implementing thresholding

A crucial step in image segmentation is thresholding, which changes a grayscale image into a binary image. It is essential for distinguishing the items of attention from the backdrop.

When using the `cv2.THRESH_BINARY_INV` thresholding method in OpenCV, the `cv2.THRESH_OTSU` parameter is added to apply Otsu's binarization process. Otsu's method automatically determines an optimal threshold by maximizing the variance between two classes of pixels in the image. It aims to find a threshold that minimizes intra-class variance and maximizes inter-class variance, effectively separating the image into two groups of pixels with distinct characteristics.

> _****Otsu's binarization process****_
> 
> __Otsu's binarization is a technique used in image processing to separate the foreground and background of an image into two distinct classes. This is done by finding the optimal threshold value that maximizes the variance between the two classes. Otsu's method is known for its simplicity and computational efficiency, making it a popular choice in applications such as document analysis, object recognition, and medical imaging.__

`#Threshold Processing ret, bin_img = cv2.threshold(gray,                              0, 255,                               cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU) imshow(bin_img)`

****Output:****

#### ****Step 4: Noise Removal****

To clean the object's outline (boundary line), noise is removed using morphological gradient processing.

> ****Morphological Gradient Processing****
> 
> The morphological gradient is a tool used in morphological image processing to emphasize the edges and boundaries of objects in an image. It is obtained by subtracting the erosion of an image from its dilation. Erosion shrinks bright regions in an image, while dilation expands them, and the morphological gradient represents the difference between the two. This operation is useful in tasks such as object detection and segmentation, and it can also be combined with other morphological operations to enhance or filter specific features in an image.

`# noise removal kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)) bin_img = cv2.morphologyEx(bin_img,                             cv2.MORPH_OPEN,                            kernel,                            iterations=2) imshow(bin_img)`

****Output:****

#### Detecting the black background and foreground of the image

Next, we need to get a hold of the black area, which is the background part of this image. If the white part is the required area and is well-filled, t...

(Conteúdo truncado devido ao limite de extração, mas a essência do algoritmo e sua implementação em Python/OpenCV foram capturados)

Fonte: [https://www.geeksforgeeks.org/image-segmentation-with-watershed-algorithm-opencv-python/](https://www.geeksforgeeks.org/image-segmentation-with-watershed-algorithm-opencv-python/)

