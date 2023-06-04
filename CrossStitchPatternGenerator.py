from PIL import Image
from PIL import ImageFilter, ImageEnhance
import matplotlib.pyplot as plt
import numpy as np
from colormap import rgb2hex
import pandas as pd


## Settings ##
image_name = "flower.jpg"  # image (.jpg format) of a flower
no_of_colors = 15     # no of colours/threads to use for this project
cloth_length = 220    # length or no. of holes across the fabric


# Open img
img = Image.open(image_name)

# Resize img
width, height = img.width, img.height
resize_value = cloth_length/width
imgSmall = img.resize((round(width*resize_value), round(height*resize_value)), resample=Image.NEAREST)

# Enhance img contrast
enhancer = ImageEnhance.Contrast(imgSmall)
imgSmall = enhancer.enhance(1.8)

# Reduce no. of colors
imgSmall = imgSmall.convert('P', palette=Image.ADAPTIVE, colors= no_of_colors)
imgSmall = imgSmall.convert('RGB')

# Convert to array
image_sequence = imgSmall.getdata()
r = np.reshape(np.array(imgSmall.getdata(band= 0)), (imgSmall.getdata().size[1], imgSmall.getdata().size[0]))
g = np.reshape(np.array(imgSmall.getdata(band= 1)), (imgSmall.getdata().size[1], imgSmall.getdata().size[0]))
b = np.reshape(np.array(imgSmall.getdata(band= 2)), (imgSmall.getdata().size[1], imgSmall.getdata().size[0]))
image_array = np.reshape(np.array(image_sequence), (3, image_sequence.size[1], image_sequence.size[0]))

# Convert RGB to HEX
row, col = r.shape
image_hexarray = np.empty((row, col), dtype='object')
for i in range(0, row):
    for j in range(0, col):
        hex_value = rgb2hex(r[i][j], g[i][j], b[i][j])
        image_hexarray[i][j] = hex_value

# Convert hex to cross stitch symbol
colormap_dict = image_hexarray.reshape(image_hexarray.size)
colormap = set(colormap_dict)
symbol_list = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "+", "=", "[", "]", "{", "}", ";", "'", "<", ">", "?"]
dataframe = pd.DataFrame(image_hexarray)
dataframe = dataframe.replace(colormap, symbol_list[:len(colormap)])
dataframe.to_csv("pattern.csv", header=None, index=None)