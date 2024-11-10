import random

import pygame

from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, 2)

    def update(self, dt):
        self.position += self.velocity * dt
        self.wrap_around()

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        random_angle = random.uniform(20, 50)
        v_splinter_1 = self.velocity.rotate(random_angle)
        v_splinter_2 = self.velocity.rotate(-random_angle)
        splinter_radius = self.radius - ASTEROID_MIN_RADIUS
        splinter_1 = Asteroid(self.position.x, self.position.y, splinter_radius)
        splinter_1.velocity = v_splinter_1 * 1.2
        splinter_2 = Asteroid(self.position.x, self.position.y, splinter_radius)
        splinter_2.velocity = v_splinter_2 * 1.2
