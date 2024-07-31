#%%
import numpy as np
import skimage
from manim import *
import matplotlib.pyplot as plt

img = skimage.io.imread('experimental_crop.tif')
max_proj = skimage.io.imread('max_intensity.png')
min_val = 15
max_val = 40
np_img = np.clip(np.array(img), a_min=min_val, a_max=max_val)
scaled = np.asarray((np_img - min_val) / (max_val - min_val) * 255).astype(np.uint8)

#%%

class Image(MovingCameraScene):
    def construct(self):
        max_proj_obj = ImageMobject(max_proj)
        max_proj_obj.height = 8
        self.add(max_proj_obj)
        self.wait(1)
        self.remove(max_proj_obj)
        for i in range(20):
            frame = ImageMobject(scaled[i,:,:])
            frame.height=8
            self.add(frame)
            self.wait(0.1)
            self.remove(frame)


if __name__ == "__main__":
    Image().render(preview=True)



    # minval = np.percentile(np_img, 10)
    # maxval = np.percentile(np_img, 100)
    # clipped_img = np.clip(np_img, minval, maxval)
    # adjusted_img = ((clipped_img - minval) / (maxval - minval)) * 255