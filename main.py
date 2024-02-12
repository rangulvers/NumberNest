# this is the main file for the project. It allows the user to input a file and then generate a draw-by-numbers image from the input file
# when calling the script the user will call it with arguments
# arguments:
# 1. input file
# 2. output file
# 3. number of colors



import cv2
import numpy as np
import os
import sys
import time
import random
import math
from PIL import Image








def create_image_from_palette(palette, width, height):
    # Create a new image with the given dimensions
    image = Image.new('RGB', (width, height))

    # Get the image's pixel data
    pixels = image.load()

    # For each pixel in the image...
    for y in range(height):
        for x in range(width):
            # Choose a random color from the palette
            color = random.choice(palette)

            # Set the pixel's color
            pixels[x, y] = color

    # Return the new image
    return image

def reduce_colors(image, num_colors):
    # get the dimensions of the image
    h, w, _ = image.shape
    # get the number of pixels
    num_pixels = h * w
    # get the image in the form of a 2D array
    image_2D = image.reshape(num_pixels, 3)
    # convert the image to a float array
    image_2D = np.float32(image_2D)
    # define the criteria for the k-means algorithm
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
    # run the k-means algorithm
    _, labels, centers = cv2.kmeans(image_2D, num_colors, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    # convert the centers to 8-bit integers
    centers = np.uint8(centers)
    # map the labels to the centers to get the segmented image
    segmented_image = centers[labels.flatten()]
    # reshape the segmented image to the original image shape
    segmented_image = segmented_image.reshape(image.shape)
    # return the segmented image
    return segmented_image

# analyze the image and get the color palette
def get_color_palette(image, num_colors):
    # get the dimensions of the image
    h, w, _ = image.shape
    # get the number of pixels
    num_pixels = h * w
    # get the image in the form of a 2D array
    image_2D = image.reshape(num_pixels, 3)
    # convert the image to a float array
    image_2D = np.float32(image_2D)
    # define the criteria for the k-means algorithm
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
    # run the k-means algorithm
    ret, label, center = cv2.kmeans(image_2D, num_colors, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    # convert the center to a 8-bit integer
    center = np.uint8(center)
    # return the dominant colors
    return [tuple(color) for color in center]

# load the image from the input file
def load_image(input_file):
    # read the image from the input file
    image = cv2.imread(input_file)
    # return the image
    return image


# main function for the project that takes in the input file and the arguments
def main():
    # get the input file from the command line
    input_file = sys.argv[1]
    # get the output file from the command line
    output_file = sys.argv[2]
    # get the number of colors from the command line
    num_colors = int(sys.argv[3])

    # load the image from the input file
    image = cv2.imread(input_file)

    # reduce the image to 10 colors
    reduced_image = reduce_colors(image, 10)

    # save the reduced image
    cv2.imwrite('output.png', reduced_image)




if __name__ == "__main__":
    main()