import glob
image_list = sorted(glob.glob("./Artworks/resized/resized/Albrecht*"))

print(image_list[0], image_list[-1])