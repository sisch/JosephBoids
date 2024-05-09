import logging
import math
import random

import pygame
from pygame import Vector2
from pygame.math import lerp

from common_classes import GameObject, PhysicsMixin


class Flock:
    boids_by_group = {}

    def __init__(self):
        self.boids_by_group = {}

    def add_boid(self, boid):
        if boid.group not in self.boids_by_group:
            self.boids_by_group[boid.group] = []
        self.boids_by_group[boid.group].append(boid)
        boid.parent = self

    def get_boids(self, group):
        return self.boids_by_group.get(group, [])

    def get_center(self, group):
        boids = self.get_boids(group)
        center = pygame.Vector2(0, 0)
        for boid in boids:
            center += boid.position
        return center / len(boids)

    def get_boids_alignment(self, group, width, height):
        boids = self.get_boids(group)
        average_angle = sum([boid.angle for boid in boids]) / len(boids)

        trajectory = Vector2(0, 1).rotate(average_angle)
        center = self.get_center(group)
        aim = center + 2*trajectory
        new_direction_x = new_direction_y = Vector2(0, 0)
        if aim.x < 100 or aim.x > width-100:
            new_direction_x = Vector2(0, 1)
            if math.fabs(new_direction_x.angle_to(trajectory)) > math.fabs((-new_direction_x).angle_to(trajectory)):
                new_direction_x *= -1
        if aim.y > height-100 or aim.y < 100:
            new_direction_y = Vector2(1, 0)
            if math.fabs(new_direction_y.angle_to(trajectory)) > math.fabs((-new_direction_y).angle_to(trajectory)):
                new_direction_y *= -1

        new_direction = new_direction_x + new_direction_y
        average_direction = Vector2(0, 1).rotate(average_angle)
        return (2*average_direction + 5*new_direction + 3*(Vector2(width//2, height//2) - center).normalize()).normalize()

    def get_span(self, group):
        boids = self.get_boids(group)
        if not boids:
            return 0
        max_span = 0
        for boid in boids:
            for other in boids:
                span = boid.position.distance_to(other.position)
                if span > max_span:
                    max_span = span
        return max_span

    def remove_boid(self, boid):
        self.boids_by_group[boid.group].remove(boid)

    def get_all_boids(self):
        out = []
        for group in sorted(self.boids_by_group.keys()):
            out.extend(self.boids_by_group[group])
        return out


class Boid(PhysicsMixin, GameObject):
    group: int
    id: int
    parent: Flock
    avoid_distance = 5
    min_speed = 35
    max_speed = 35

    def __init__(self, position, velocity, group, id=1, angle=0):
        super().__init__(position)
        if isinstance(velocity, tuple):
            velocity = pygame.Vector2(velocity)
        self.velocity = velocity
        self.group = group
        self.id = id
        self.angle = angle

    def update(self, dt, time):
        vel = self.get_new_velocity(self.parent.get_boids(self.group))
        sep = self.get_separation_vector(self.parent.get_boids(self.group))
        coherence = self.get_coherence_vector(self.parent.get_boids(self.group))
        if sep is None:
            sep = Vector2(0, 0)
        self.angle = self.get_new_angle()
        self.velocity = Vector2(0, 1) * lerp(self.velocity.length(), vel.length()+random.uniform(-5, 5), dt)
        self.position += self.velocity.rotate(self.angle)*dt*self.min_speed
        print(self.position, self.velocity.rotate(self.angle), self.angle)

    def get_separation_vector(self, boids):
        total = pygame.Vector2(0, 0)
        for boid in boids:
            distance = self.position.distance_to(boid.position)
            if 0 < distance < self.avoid_distance:
                separation_force = (self.position - boid.position) / (distance ** 2)
                total += separation_force
            elif distance == 0:
                # Maximum separation force when boids are at the same position
                total += pygame.Vector2(1, 1)
        if total.length() > 0:
            return total.normalize()
        return Vector2(0, 0)

    def get_coherence_vector(self, boids):
        center = self.parent.get_center(self.group)
        return (center - self.position).normalize()

    def get_new_velocity(self, boids):
        if not boids:
            return Vector2(0, 1)

        total_velocity = Vector2(0, 0)
        for boid in boids:
            total_velocity += boid.velocity
        average_velocity = total_velocity / len(boids)
        if average_velocity.length() == 0:
            return Vector2(0, 1)
        return average_velocity.normalize()

    def get_new_angle(self):
        forward = Vector2(0, 1).rotate(self.angle).normalize()
        target = self.parent.get_boids_alignment(self.group, 1920, 1080)
        angle = forward.angle_to(target-self.position)
        return lerp(self.angle, self.angle + angle, 0.1)

    def render(self, screen: pygame.Surface):
        bottom_right = Vector2(3, -5).rotate(self.angle)
        bottom_left = Vector2(-3, -5).rotate(self.angle)
        top_center = Vector2(0, 5).rotate(self.angle)

        bottom_right += self.position
        bottom_left += self.position
        top_center += self.position

        pygame.draw.lines(screen, (255, 255, 255), True, [top_center, bottom_right, bottom_left], 2)

    def __repr__(self):
        return f"Boid {self.id} at {self.position} with velocity {self.velocity} in group {self.group}"


if __name__ == '__main__':
    flock = Flock()
    b1 = Boid((0, 0), (1, 1), 1)
    b2 = Boid((100, 100), (1, 1), 1, 2)
    b3 = Boid((200, 200), (1, 1), 2, 3)
    print(b1.id, b2.id, b3.id)
    flock.add_boid(b1)
    flock.add_boid(b2)
    flock.add_boid(b3)
    print(flock.get_all_boids())
    print(flock.get_boids(1))
    print(flock.get_boids(2))

    for i in range(10):
        b1.update(1, i)
        print(b1)
