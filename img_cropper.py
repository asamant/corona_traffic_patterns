#!/usr/bin/env python3

import os
from PIL import Image

# store images in a new directory
cwd = os.getcwd()
img_path = os.path.join(cwd, 'Images')
if not os.path.exists(img_path):
    os.mkdir(img_path)

# could be different based on how you've configured
screenshot_dir = os.path.join(cwd, 'Screenshots')

# iterate through screenshot dir crop imgs
for filename in os.listdir(screenshot_dir):
    if filename.endswith(".png") or filename.endswith(".jpg"):
        img_full_path = os.path.join(screenshot_dir, filename)
        im = Image.open(img_full_path)
        width, height = im.size
        new_im = im.crop((width/3, 5, width, height-5))
        new_im.save(img_path + "/" + filename)
    else:
        continue
