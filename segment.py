import pymunk
import pymunk.pygame_util
from pymunk import Vec2d
from conversion import to_pygame
import math
import pygame.transform

SEGMENT_WIDTH = 5
FRICTION = 1

"""
Class that represents one segment of the human body, i.e. upper arm, thigh.
"""


class Segment:
    def __init__(self, mass, length, starting_position, collision_type, image=None):
        """
        :param mass: mass in kilograms
        :param length: length in meters
        :param starting_position: (x, y) tuple of location of center of segment
        :param collision_type: enumerated integer that determines collision behavior
        :return: nothing
        """
        inertia = pymunk.moment_for_segment(mass, (length / 2, 0), (-length / 2, 0))

        self.body = pymunk.Body(mass, inertia)
        self.body.position = starting_position

        self.shape = pymunk.Segment(self.body, (0, length / 2), (0, -length / 2), SEGMENT_WIDTH)
        self.shape.collision_type = collision_type
        self.shape.friction = FRICTION

        self.image = image

    def add_to_space(self, space):
        """
        Adds all pymunk objects to a space
        :param space: pymunk space
        :return: nothing
        """
        space.add(self.body, self.shape)

    def draw(self, screen):
        """
        Draws this object on a pygame screen
        :param screen: pygame screen
        :return: nothing
        """
        if self.image is None:
            pymunk.pygame_util.draw(screen, self.shape, self.body)
        else:
            p = self.body.position
            p = Vec2d(to_pygame(p))

            # we need to rotate 180 degrees because of the y coordinate flip
            angle_degrees = math.degrees(self.body.angle) + 180
            rotated_logo_img = pygame.transform.rotate(self.image, angle_degrees)

            offset = Vec2d(rotated_logo_img.get_size()) / 2.
            p -= offset

            screen.blit(rotated_logo_img, p)
