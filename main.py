import numpy as np
import skimage
from manim import *

np.random.seed(1)

colors = color_gradient([DARK_GRAY, WHITE], 6)

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
                    color=WHITE,
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
                x * 0.25 + np.random.uniform(0, 0.1),
                y * 0.25 + np.random.uniform(0, 0.1),
                0,
            )
            for x, y in positions
        ]
        self.stars = [Dot(i, radius=0.15 * 0.25, color=DARK_GRAY) for i in positions]
        super().__init__(*self.stars)


class Main(MovingCameraScene):
    def construct(self):
        galaxies = Group(
            *(
                Galaxy(np.random.randint(3, 11))
                .move_to(position)
                .rotate(np.random.uniform(0, 2 * np.pi))
                for position in [
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
            )
        )
        for galaxy in galaxies:
            for star in galaxy.stars:
                self.add(star)
        galaxy_dots = [
            Dot(radius=0.15, color=DARK_GRAY).move_to(galaxy.get_center())
            for galaxy in galaxies
        ]
        for dot in galaxy_dots:
            dot.z_index = 1
        main_galaxy = galaxies[0]
        main_star = main_galaxy.stars[0]

        camera: MovingCamera = self.camera
        camera.frame.set(height=main_star.height * 1.5)
        camera.frame.move_to(main_star.get_center())

        self.wait()
        self.next_section()

        for _ in range(3):
            self.play(Blink(main_star, min_wait=0.5, max_wait=1.5))
            self.wait(np.random.uniform(0.3, 0.9))
        self.wait()
        self.next_section()

        self.play(
            camera.frame.animate.set(height=main_galaxy.height).move_to(
                main_galaxy.get_center()
            )
        )
        self.wait()
        self.next_section()

        self.play(
            *(
                Succession(
                    Blink(i, min_wait=1, max_wait=3),
                    Blink(i, min_wait=1, max_wait=3),
                    Blink(i, min_wait=1, max_wait=3),
                )
                for i in main_galaxy.stars
            ),
            run_time=4
        )
        self.wait()
        self.next_section()

        self.play(
            camera.frame.animate.set(height=galaxies.height).move_to(
                galaxies.get_center()
            ),
        )
        self.wait()
        self.next_section()

        self.play(
            *(Transform(galaxy, dot) for galaxy, dot in zip(galaxies, galaxy_dots))
        )
        self.wait()
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
                    run_time=0.5
                )
            )
        self.play(
            AnimationGroup(
                *(dot.animate.set_fill(DARK_GRAY) for dot in galaxy_dots),
                lag_ratio=0.1,
                run_time=0.5
            )
        )
        self.wait()
        self.next_section()
        
        frame = ImageMobject(scaled[0, :, :])
        frame.height = 8
        self.play(FadeIn(frame), *(FadeOut(dot) for dot in galaxy_dots), duration=2)
        for dot in galaxy_dots:
            self.remove(dot)
        self.wait()
        self.next_section()
        
        self.remove(frame)
        for i in range(80):
            frame = ImageMobject(scaled[i, :, :])
            frame.height = 8
            self.add(frame)
            self.wait(0.15)
            self.remove(frame)


if __name__ == "__main__":
    Main().render(preview=True)
