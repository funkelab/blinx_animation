import numpy as np
from manim import *


count = 0


class Blink(Succession):
    def __init__(self, mobject, blink_count=1, min_wait=0, max_wait=2, **kwargs):
        super().__init__(
            *(
                Succession(
                    Wait(run_time=np.random.uniform(min_wait / 3.0, max_wait / 3.0)),
                    Indicate(
                        mobject,
                        run_time=np.random.uniform(min_wait / 3.0, max_wait / 3.0),
                    ),
                    Wait(run_time=np.random.uniform(min_wait / 3.0, max_wait / 3.0)),
                )
                for _ in range(blink_count)
            ),
            **kwargs,
        )


class Main(MovingCameraScene):
    def construct(self):
        positions = [
            (1, 1),
            (-1, 1),
            (-1, -1),
            (1, -1),
            (2, 0),
            (-2, 0),
            (0, 2),
            (0, -2),
        ]
        main_center_dot = Dot((0, 0, 0), radius=1)
        main_group = Group(
            main_center_dot,
            *(Dot(3 * UP * x + 3 * RIGHT * y, radius=1) for x, y in positions),
        )

        camera: MovingCamera = self.camera
        camera.frame.set(height=3)
        self.add(main_group)

        self.wait()
        self.play(Indicate(main_center_dot))
        self.wait()
        self.play(camera.frame.animate.set(height=main_group.height))
        self.wait()
        self.play(*(Indicate(i) for i in main_group))
        self.wait()
        self.play(
            camera.frame.animate.set(height=main_group.height * 3),
            *(
                i.animate.shift((i.get_center() - main_group.get_center()) * -0.5)
                for i in main_group
            ),
        )
        self.wait()


if __name__ == "__main__":
    Main().render(preview=True)
