# AGH UST Medical Informatics 03.2021
# Lab 2 : Segmentation

import cv2 as cv
import numpy as np

im = cv.imread('abdomen.png')
im = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
w = im.shape[1]
h = im.shape[0]

THRESHOLD = 6

mask = np.zeros([h, w], np.uint8)


def mouse_callback(event, x, y, flags, params):
    if event == 1:
        pixel_queue = [(y, x)]
        while len(pixel_queue) > 0:
            parent_y, parent_x = pixel_queue.pop()
            parent_v = im[parent_y, parent_x]
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    if not (dy == dx and dx == 0):
                        nx = parent_x + dx
                        ny = parent_y + dy
                        if 0 <= ny < h and 0 <= nx < w:
                            nv = im[ny, nx]
                            if mask[ny, nx] == 0 and abs(int(parent_v) - int(nv)) < THRESHOLD:
                                pixel_queue.append((ny, nx))

            mask[parent_y, parent_x] = 255

        cv.imshow('mask', mask)

        closed = cv.morphologyEx(mask, cv.MORPH_CLOSE, np.ones((10, 10), np.uint8))
        cv.imshow('closed', closed)

        edges = cv.Canny(closed, 100, 200)
        cv.imshow('edges', edges)

cv.imshow('image', im)
cv.setMouseCallback('image', mouse_callback)
cv.waitKey()
cv.destroyAllWindows()
