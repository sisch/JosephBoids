import random

import pygame
from pygame.math import lerp, Vector2

from common_classes import GameObject, PhysicsMixin
from config import get_boundaries, logger


class Boid(PhysicsMixin, GameObject):
    parent = None
    turn_speed = 540
    avoid_radius = 25

    def __init__(self, position, speed, forward):
        super().__init__(position)
        self.speed = speed
        self.forward = forward
        self.heading = (self.forward.angle_to(Vector2(0, -1)) + 360) % 360

    def set_parent(self, parent):
        self.parent = parent

    def update(self, dt, time):
        self.position += self.forward * (self.speed * dt)
        flock_avoidance = self.parent.get_avoidance(self)
        if flock_avoidance is not None:
            self.position += flock_avoidance * (0.2 * self.speed * dt)
        center_direction = self.parent.get_center() - self.position
        self.position += center_direction.normalize() * (0.1 * self.speed * dt)
        avoidance_angle = self.get_avoidance_direction()
        angle_direction = 0
        if avoidance_angle > 0:
            angle_direction = 1
        elif avoidance_angle < 0:
            angle_direction = -1
        angle = angle_direction * self.turn_speed * dt
        self.heading += angle
        if abs(angle) < 0.03:
            self.heading += self.get_flock_direction_angle() * 0.7 * self.turn_speed * dt
        self.heading %= 360
        self.forward = Vector2(0, -1).rotate(self.heading).normalize()

    def get_flock_direction_angle(self):
        alignment = self.parent.get_average_direction()
        alignment_angle = self.forward.angle_to(alignment)
        center_angle = 0
        boids_in_avoidance_range = 0
        for boid in self.parent.boids:
            distance = self.position.distance_to(boid.position)
            if 0 < distance < 10:
                boids_in_avoidance_range += 1
        if boids_in_avoidance_range == 0:
            center = self.parent.get_center()
            center_direction = (center - self.position).normalize()
            center_angle = self.forward.angle_to(center_direction)
        average_angle = 0.8 * alignment_angle + 0.2 * center_angle
        if average_angle < 0:
            return -1
        return 1

    def get_avoidance_direction(self):
        avoidance_vector = self.get_boundary_avoidance_vector()
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
    target = None

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
        average_direction = direction / len(self.boids)
        if self.target:
            target_direction = (self.target - self.get_center()).normalize()
            return 0.5 * average_direction + 0.5 * target_direction
        return average_direction

    def get_avoidance(self, boid):
        avoidance = Vector2(0, 0)
        for other in self.boids:
            if other == boid:
                continue
            distance = boid.position.distance_to(other.position)
            if distance < boid.avoid_radius:
                direction = boid.position - other.position
                if direction.length() == 0:
                    direction = Vector2(1, 0).rotate(360 * random.random())
                avoidance += direction.normalize()
        if avoidance.length() == 0:
            return None
        return avoidance.normalize()