# %%
import numpy as np
import skimage
from manim import *
import matplotlib.pyplot as plt

img = skimage.io.imread("experimental_crop.tif")
max_proj = skimage.io.imread("max_intensity.png")
min_val = 15
max_val = 40
np_img = np.clip(np.array(img), a_min=min_val, a_max=max_val)
scaled = np.asarray((np_img - min_val) / (max_val - min_val) * 255).astype(np.uint8)

# %%


class Image(MovingCameraScene):
    def construct(self):
        max_proj_obj = ImageMobject(max_proj)
        max_proj_obj.height = 8
        self.add(max_proj_obj)
        poss = [
            (-0.4, 1.3, 0),
            (0.6, 2.6, 0),
            (2.0, 0.8, 0),
            (3.2, -0.7, 0),
            (0.9, -1, 0),
            (-0.65, -1.75, 0),
            (-2.15, -1.4, 0),
            (-1, 2.9, 0),
            (-2.5, -0.3, 0),
            (-3.7, 2.75, 0),
            (-3.5, -3.3, 0),
        ]

        for pos in poss:
            self.add(Dot(pos, radius=0.15, color=RED))
        # self.wait(1)
        # self.remove(max_proj_obj)
        # for i in range(20):
        #     frame = ImageMobject(scaled[i,:,:])
        #     frame.height=8
        #     self.add(frame)
        #     self.wait(0.1)
        #     self.remove(frame)


5
if __name__ == "__main__":
    Image().render(preview=True)

    # minval = np.percentile(np_img, 10)
    # maxval = np.percentile(np_img, 100)
    # clipped_img = np.clip(np_img, minval, maxval)
    # adjusted_img = ((clipped_img - minval) / (maxval - minval)) * 255
