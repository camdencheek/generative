#!/usr/bin/python3
import cairo
import scipy.optimize as so
from opensimplex import OpenSimplex
from scipy.spatial.transform import Rotation as R
import skimage.morphology as sm
import random
import numpy as np

surface = cairo.SVGSurface("example.svg", 1000,1000)
ctx = cairo.Context(surface)

seed = 1234
d1 = OpenSimplex(seed)
def noise(point):
  return d1.noise2d(point[0], point[1])



from PIL import Image # Depends on the Pillow lib

from opensimplex import OpenSimplex

WIDTH = 1024
HEIGHT = 1024
FEATURE_SIZE = 100.0



def main():
    simplex = OpenSimplex(random.randint(0,100))
    def noise(point):
      n1 = simplex.noise2d(point[0] / FEATURE_SIZE, point[1] / FEATURE_SIZE)
      n2 = simplex.noise2d(point[0] / FEATURE_SIZE * 2, point[1] / FEATURE_SIZE * 2)
      return (n1 + n2) / 2

    def rot(ang):
      return np.array([[np.cos(ang), np.sin(ang)], [-np.sin(ang), np.cos(ang)]])

    im = Image.new('L', (WIDTH, HEIGHT))
    vals = np.zeros((WIDTH,HEIGHT), dtype=int)
    for y in range(0, HEIGHT):
        for x in range(0, WIDTH):
            value = noise([x,y])
            color = int((value + 1) * 128)
            vals[x][y] = color
            im.putpixel((x, y), color)

    minima = sm.local_minima(vals)
    labelled, n_mins = sm.label(minima, return_num=True)

    for label in range(1, n_mins):
      point = np.transpose(np.where(labelled==label)).mean(axis=0)
      for i in range(10000):
        im.putpixel([int(point[0]), int(point[1])], 0)
        grad = so.approx_fprime(point, noise, 0.1)
        direction = np.matmul(rot(np.pi / 2.0 * 0.95), grad)
        point[0] = point[0] + direction[0] * 50.0
        point[1] = point[1] + direction[1] * 50.0
        if (point[0] > WIDTH or point[1] > WIDTH or point[0] < 0 or point[1] < 0):
          break


    im.save('noise2d.png')



if __name__ == '__main__':
  main()






