import pygame
from pygame.math import lerp, Vector2

from common_classes import GameObject, PhysicsMixin
from config import get_boundaries, logger


class Boid(PhysicsMixin, GameObject):
    def __init__(self, position, speed, forward):
        super().__init__(position)
        self.speed = speed
        self.forward = forward
        self.parent = None
        self.turn_speed = 90
        self.heading = (self.forward.angle_to(Vector2(0, -1)) + 360) % 360


    def set_parent(self, parent):
        self.parent = parent

    def update(self, dt, time):
        self.position += self.forward * (self.speed * dt)
        #self.forward = self.forward.normalize() * 0.3 + self.get_boundary_avoidance_vector() * 0.7
        avoidance_angle = self.get_avoidance_direction()
        angle_direction = 0
        if avoidance_angle > 0:
            angle_direction = 1
        elif avoidance_angle < 0:
            angle_direction = -1
        angle = angle_direction * self.turn_speed * dt
        self.heading += angle
        self.heading %= 360
        self.forward = Vector2(0, -1).rotate(self.heading).normalize()

        #forward_alignment = self.get_forward_alignment()
        #self.forward = lerp(self.forward, forward_alignment, 0.9)
        #center_alignment = self.get_center_alignment()
        #self.forward = lerp(self.forward, center_alignment, 0.9)
        #self.velocity = self.forward * self.speed
        #logger.debug(f"[{self.id}] Position: {self.position}, Heading: {self.heading}")

    def get_avoidance_direction(self):
        avoidance_vector = self.get_boundary_avoidance_vector()
        print(self.id, avoidance_vector)
        if avoidance_vector is not None:
            avoidance_angle = avoidance_vector.angle_to(self.forward)
            avoidance_angle = (avoidance_angle + 360) % 360
            if avoidance_angle < 0.5 or avoidance_angle > 359.5:
                return 0
            angle = -1 if avoidance_angle < 180 else 1
            return angle
        return 0

    def get_boundary_avoidance_vector(self):
        LEFT_BOUNDARY, TOP_BOUNDARY, RIGHT_BOUNDARY, BOTTOM_BOUNDARY = get_boundaries()
        out = Vector2(0, 0)
        if self.position.x < LEFT_BOUNDARY:
            out += pygame.Vector2(1, 0)
        if self.position.x > RIGHT_BOUNDARY:
            out += pygame.Vector2(-1, 0)
        if self.position.y < TOP_BOUNDARY:
            out += pygame.Vector2(0, 1)
        if self.position.y > BOTTOM_BOUNDARY:
            out += pygame.Vector2(0, -1)
        print(self.id, out)
        return out.normalize() if out.length() >= 1 else None

    def get_forward_alignment(self):
        direction = self.parent.get_average_direction()
        return direction.normalize()

    def get_center_alignment(self):
        center = self.parent.get_center()
        return (center - self.position).normalize()

    def render(self, screen):
        tip = self.forward.normalize() * 10
        base_points = [
            self.position + tip.rotate(135),
            self.position + tip.rotate(-135),
            self.position + tip
        ]
        pygame.draw.polygon(screen, (255, 255, 255), base_points)


class Flock(GameObject):
    boids = []
    def __init(self):
        self.boids = []

    def add_boid(self, boid):
        self.boids.append(boid)
        boid.set_parent(self)

    def get_center(self):
        center = pygame.Vector2(0, 0)
        for boid in self.boids:
            center += boid.position
        return center / len(self.boids)

    def get_average_direction(self):
        direction = pygame.Vector2(0, 0)
        for boid in self.boids:
            direction += boid.forward
        return direction / len(self.boids)