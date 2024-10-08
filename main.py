import numpy as np
import skimage
from manim import *

np.random.seed(1)

colors = color_gradient([DARKER_GRAY, WHITE], 8)

img = skimage.io.imread("experimental_crop.tif")
max_proj = skimage.io.imread("max_intensity.png")
min_val = 15
max_val = 40
np_img = np.clip(np.array(img), a_min=min_val, a_max=max_val)
scaled = np.asarray((np_img - min_val) / (max_val - min_val) * 255).astype(np.uint8)


class Blink(AnimationGroup):
    def __init__(self, mobject, blink_count=1, min_wait=0, max_wait=2, **kwargs):
        animations = []
        for _ in range(blink_count):
            wait = Wait(np.random.uniform(min_wait, max_wait) / 2)
            # AnimationGroup wants Wait to have mobject not be None
            wait.mobject = mobject
            animations.append(wait)
            animations.append(
                Indicate(
                    mobject,
                    run_time=np.random.uniform(min_wait, max_wait) / 2,
                    color=GRAY,
                )
            )
        super().__init__(*animations, **kwargs)


def get_random_points(
    count, outer_radius, exclusion_radius, starting=None, throw_after_each=10
):
    if starting is None:
        points = []
    else:
        points = starting

    throw_after = throw_after_each * count
    while len(points) < count:
        r = np.random.uniform(0, outer_radius)
        theta = np.random.uniform(0, 2 * np.pi)
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        if all(
            np.linalg.norm(np.array([x, y]) - np.array([px, py])) > exclusion_radius
            for px, py, _ in points
        ):
            points.append((x, y, 0))
        throw_after -= 1
        if throw_after == 0:
            raise ValueError("Could not generate enough points")

    return points


class Galaxy(Group):
    def __init__(self, count):
        positions = [
            (-0.5, 0),
            (0.5, 0),
            (-1.5, 0),
            (1.5, 0),
            (-0.5, 1),
            (0.5, 1),
            (-1.5, 1),
            (1.5, 1),
            (-0.5, -1),
            (0.5, -1),
            (-1.5, -1),
            (1.5, -1),
        ]
        np.random.shuffle(positions)
        positions = positions[:count]
        positions = [
            (
                x * 0.04 + np.random.uniform(0, 0.02),
                y * 0.04 + np.random.uniform(0, 0.02),
                0,
            )
            for x, y in positions
        ]
        self.stars = [Dot(i, radius=0.15 * 0.075, color=DARKER_GRAY) for i in positions]
        super().__init__(*self.stars)


class Main(MovingCameraScene):
    def construct(self):
        main_galaxy = (
            Galaxy(5).move_to((-0.4, 1.3, 0)).rotate(np.random.uniform(0, 2 * np.pi))
        )
        main_star = main_galaxy.stars[0]

        galaxies = Group(
            main_galaxy,
            *(
                Galaxy(np.random.randint(3, 11))
                .move_to(position)
                .rotate(np.random.uniform(0, 2 * np.pi))
                for position in [
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
            ),
        )
        for galaxy in galaxies:
            for star in galaxy.stars:
                self.add(star)
        galaxy_dots = [
            Dot(radius=0.15, color=DARKER_GRAY).move_to(galaxy.get_center())
            for galaxy in galaxies
        ]
        for dot in galaxy_dots:
            dot.z_index = 2

        camera: MovingCamera = self.camera
        camera.frame.set(height=main_star.height * 1.5)
        camera.frame.move_to(main_star.get_center())
        main_star.set(color=DARKER_GRAY)

        self.wait()

        self.next_section()
        for _ in range(3):
            self.play(Blink(main_star, min_wait=0.5, max_wait=1.5))
            self.wait(np.random.uniform(0.3, 0.9))

        self.next_section()
        self.play(
            camera.frame.animate.set(height=main_galaxy.height).move_to(
                main_galaxy.get_center()
            ),
        )

        self.next_section()
        self.play(
            *(
                Succession(*(Blink(i, min_wait=1, max_wait=1.75) for _ in range(12)))
                for i in main_galaxy.stars
            ),
        )

        self.next_section()
        self.play(
            LaggedStart(
                camera.frame.animate.set(height=8).move_to(galaxies.get_center()),
                AnimationGroup(
                    *(FadeIn(dot) for dot in galaxy_dots),
                    *(FadeOut(galaxy) for galaxy in galaxies),
                ),
                lag_ratio=0.8,
            )
        )

        self.next_section()
        for _ in range(15):
            np.random.shuffle(galaxy_dots)
            self.play(
                AnimationGroup(
                    *(
                        dot.animate.set_fill(np.random.choice(colors))
                        for dot in galaxy_dots
                    ),
                    lag_ratio=0.1,
                    run_time=0.5,
                )
            )

        self.play(
            AnimationGroup(
                *(dot.animate.set_fill(DARKER_GRAY) for dot in galaxy_dots),
                lag_ratio=0.1,
                run_time=0.5,
            )
        )

        self.next_section()

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
                frame_rate = 10  # fps
                frame_duration = 1 / frame_rate  # seconds
                frame_index = int(elapsed_time / frame_duration) % scaled.shape[0]

                new_image = ImageMobject(scaled[frame_index, :, :])
                new_image.height = 8
                new_image.z_index = 0
                self.add(new_image)
                old = new_image

            return update_frame

        # self.add_updater(get_frame_updater())
        full_screen_rect = Rectangle(
            width=10,
            height=10,
            fill_color=BLACK,
            fill_opacity=1.0,
            stroke_width=0,
            z_index=1,
        )
        self.add(full_screen_rect)
        self.add_updater(get_frame_updater())
        self.play(
            FadeOut(full_screen_rect),
            *(FadeOut(dot) for dot in galaxy_dots),
            run_time=3,
        )
        self.wait(5)


if __name__ == "__main__":
    Main().render(preview=True)
