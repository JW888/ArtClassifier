import glob
import os
import re
from shutil import copy2


path = os.getcwd()
image_list = sorted(glob.glob(path + "/Artworks/resized/resized/Albrecht*"))

path_ar = path + '/Artworks/resized/resized/archive'


# try:
#     os.mkdir(path_ar)
# except OSError:
#     print ("Creation of the directory %s failed" % path_ar)
# else:
#     print ("Successfully created the directory %s " % path_ar)

# for ad_image in image_list:
#     path_copy = path_ar + ad_image[71:]
#     copy2(ad_image, path_copy)


ad_pattern = re.compile(r'(?=Albrecht_Du).*?(?=\d)')

for ad_image in image_list:

    path_mod = re.sub(ad_pattern, "Albrecht_Durer_", ad_image)
    os.rename(ad_image, path_mod)
