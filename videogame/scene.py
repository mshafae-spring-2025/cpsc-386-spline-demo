"""Scene objects for making games with PyGame."""

from math import isclose
from random import randint, uniform
import pygame
# from videogame import assets
from videogame import rgbcolors
# from .circle import CircleSprite

# If you're interested in using abstract base classes, feel free to rewrite
# these classes.
# For more information about Python Abstract Base classes, see
# https://docs.python.org/3.8/library/abc.html


def random_position(max_width, max_height):
    return pygame.math.Vector2(
        randint(0, max_width - 1), randint(0, max_height - 1)
    )


class Scene:
    """Base class for making PyGame Scenes."""

    def __init__(
        self, screen, background_color, screen_flags=None, soundtrack=None
    ):
        """Scene initializer"""
        self._screen = screen
        if not screen_flags:
            screen_flags = pygame.SCALED
        self._background = pygame.Surface(
            self._screen.get_size(), flags=screen_flags
        )
        self._background.fill(background_color)
        self._frame_rate = 60
        self._is_valid = True
        self._soundtrack = soundtrack
        self._render_updates = None

    def draw(self):
        """Draw the scene."""
        self._screen.blit(self._background, (0, 0))

    def process_event(self, event):
        """Process a game event by the scene."""
        # This should be commented out or removed since it generates a lot of noise.
        # print(str(event))
        if event.type == pygame.QUIT:
            print("Good Bye!")
            self._is_valid = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            print("Bye bye!")
            self._is_valid = False

    @property
    def delta_time(self):
        return self._delta_time

    @delta_time.setter
    def delta_time(self, val):
        self._delta_time = val

    def is_valid(self):
        """Is the scene valid? A valid scene can be used to play a scene."""
        return self._is_valid

    def render_updates(self):
        """Render all sprite updates."""

    def update_scene(self):
        """Update the scene state."""

    def start_scene(self):
        """Start the scene."""
        if self._soundtrack:
            try:
                pygame.mixer.music.load(self._soundtrack)
                pygame.mixer.music.set_volume(0.05)
            except pygame.error as pygame_error:
                print("\n".join(pygame_error.args))
                raise SystemExit("broken!!") from pygame_error
            pygame.mixer.music.play(loops=-1, fade_ms=500)

    def end_scene(self):
        """End the scene."""
        if self._soundtrack and pygame.mixer.music.get_busy():
            pygame.mixer.music.fadeout(500)
            pygame.mixer.music.stop()

    def frame_rate(self):
        """Return the frame rate the scene desires."""
        return self._frame_rate


class PressAnyKeyToExitScene(Scene):
    """Empty scene where it will invalidate when a key is pressed."""

    def process_event(self, event):
        """Process game events."""
        super().process_event(event)
        if event.type == pygame.KEYDOWN:
            self._is_valid = False

class SplineScene(PressAnyKeyToExitScene):
    def __init__(self, screen):
        super().__init__(screen, rgbcolors.black)
        # self._center = pygame.Vector2(400, 400)
        self._t = 0
        p0 = pygame.Vector2(0, 0)
        p1 = pygame.Vector2(100, 175)
        p2 = pygame.Vector2(200, 50)
        p3 = pygame.Vector2(500, 700)
        p4 = pygame.Vector2(700, 400)
        p5 = pygame.Vector2(800, 50)
        self._points = (p0, p1, p2, p3, p4, p5)
        self._colors = (rgbcolors.green, rgbcolors.blue, rgbcolors.orange, rgbcolors.yellow, rgbcolors.purple, rgbcolors.red)
        self._control_points = ((p0, p1, p2, p3), (p1, p2, p3, p4), (p2, p3, p4, p5),)
        self._segment = 0
        self._coefficients(*self._control_points[0])
        
    def _coefficients(self, p0, p1, p2, p3):
        alpha = 0.5
        tension = 0.5
        
        t01 = ((p1 - p0).length())**alpha
        t12 = ((p2 - p1).length())**alpha
        t23 = ((p3 - p2).length())**alpha
        
        m1 = (1.0 - tension) * (p2 - p1 + t12 * ((p1 - p0) / t01 - (p2 - p0) / (t01 + t12)))
        m2 = (1.0 - tension) * (p2 - p1 + t12 * ((p3 - p2) / t23 - (p3 - p1) / (t12 + t23)))
        
        self._a =  2.0 * (p1 - p2) + m1 + m2
        self._b = -3.0 * (p1 - p2) - m1 - m1 - m2
        self._c = m1
        self._d = p1

    def _eval(self, t):
        return (self._a * (t**3)) + (self._b * (t**2)) + (self._c * t) + self._d
        
        
    def draw(self):
        super().draw()
        center = self._eval(self._t)
        radius = 32
        pygame.draw.circle(self._screen, rgbcolors.white, center, radius)
        for p, c in zip(self._points, self._colors):
            pygame.draw.circle(self._screen, c, p, radius//2)
            

    def update_scene(self):
        """Update the scene state."""
        self._t += (self.delta_time / 1000)
        if self._t > 1.0:
            self._segment = (self._segment + 1) % len(self._control_points)
            self._coefficients(*self._control_points[self._segment])
            self._t = 0.0
        # print(self._t, self.delta_time, (self.delta_time / 10000))
    

