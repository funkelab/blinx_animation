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

class ImageUpdaterScene(Scene):
    def construct(self):
        # Initialize the ImageMobject with the first image
        # image_mobject = ImageMobject(scaled[0, :, :])
        # image_mobject.scale(2)  # Adjust the scale as needed

        # Add the image to the scene
        # self.add(image_mobject)

        # Define the updater function
        def get_frame_updater():
            elapsed_time = 0
            old = None
            def update_frame(dt):
                # capture the variables in the closure
                nonlocal elapsed_time, old
                if old is not None:
                    self.remove(old)
                # Calculate the current frame based on time elapsed
                elapsed_time += dt
                frame_rate = 10  # 10 frames per second
                frame_duration = 1 / frame_rate  # Duration of each frame in seconds
                frame_index = int(elapsed_time / frame_duration) % scaled.shape[0]
                
                new_image = ImageMobject(scaled[frame_index, :, :])
                new_image.height = 8
                new_image.fade(1 - elapsed_time / 10.0)
                self.add(new_image)
                old = new_image
            return update_frame

        self.add_updater(get_frame_updater())

        # Play some animation to observe the image changing
        self.wait(10)  # Wait for 10 seconds to see the image changes
