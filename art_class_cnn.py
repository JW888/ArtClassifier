from PIL import Image
import glob
import os

path = os.getcwd()
image_list = sorted(glob.glob(path + "/Artworks/resized/resized/*.jpg"))


image_data = {}


for image in image_list:
    im = Image.open(image)
    w, h = im.size
    image_data[image] = {'width' : w, 'height' : h}

print(image_data[image_list[0]])