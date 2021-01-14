import glob
import os
import pandas as pd
import re

path = os.getcwd()
image_list = sorted(glob.glob(path + "/Artworks/resized/resized/*.jpg"))

name_pattern = re.compile(r'(?<=resized\/resized\/).*?(?=\d)')
index_pattern = re.compile(r'(\d+)')

labels = []

for img in image_list:
        labels.append((img, re.findall(name_pattern, img)[0][:-1], int(re.findall(index_pattern, img)[0])))

labels = pd.DataFrame(labels, columns=['file_path', 'label', 'index'])
labels = labels.sort_values(by=['label', 'index']).reset_index(drop=True).reset_index().rename(columns={"level_0":'order'})
print(labels)
labels.to_csv('./Artworks/labels.csv', index=False)