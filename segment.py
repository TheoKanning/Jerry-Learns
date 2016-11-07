import pymunk
import pymunk.pygame_util
from pymunk import Vec2d
from conversion import to_pygame
from human_body_constants import BODY_COLLISION_TYPE
from resizeimage import resizeimage
import math
import pygame.transform

SEGMENT_WIDTH = 5
FRICTION = 1

IMAGE_SIZE_RATIO = 1.3

"""
Class that represents one segment of the human body, i.e. upper arm, thigh.
"""


class Segment:
    def __init__(self, mass, length, starting_position, collision_type=BODY_COLLISION_TYPE, angle=0,
                 image=None):
        """
        :param mass: mass in kilograms
        :param length: length in meters
        :param starting_position: (x, y) tuple of location of attachment point
        :param angle: angle in radians relative to vertical, in absolute coordinates
        :param collision_type: enumerated integer that determines collision behavior
        :param image: pygame surface
        :return: nothing
        """
        inertia = pymunk.moment_for_segment(mass, (length / 2, 0), (-length / 2, 0))

        self.body = pymunk.Body(mass, inertia)
        self.length = length
        x = length * math.sin(angle)
        y = -length * math.cos(angle)
        self.body.position = (starting_position[0] + x / 2, starting_position[1] + y / 2)
        self.body.angle = angle
        self.shape = pymunk.Segment(self.body, (0, length / 2), (0, -length / 2), SEGMENT_WIDTH)
        self.shape.collision_type = collision_type
        self.shape.friction = FRICTION

        if image is not None:
            ratio = length / image.get_height() * IMAGE_SIZE_RATIO
            new_width = int(image.get_width() * ratio)
            image = pygame.transform.scale(image, (new_width, int(length * IMAGE_SIZE_RATIO)))
            angle_degrees = math.degrees(self.angle())
            image = pygame.transform.rotate(image, angle_degrees)
        self.image = image

    def angle(self):
        """
        Returns the absolute angle of this segment the pymunk coordinate system
        :return: angle in radians
        """

        return self.body.angle

    def get_start_point(self):
        """
        Returns the coordinates of the shape's start point calculated using the current center point, length, and angle.
        Assumes that shapes are symmetrical around body position
        :return: (x,y) tuple of start point coordinates
        """
        x = self.body.position[0] - math.sin(self.angle()) * self.length / 2
        y = self.body.position[1] + math.cos(self.angle()) * self.length / 2
        return x, y

    def get_end_point(self):
        """
        Returns the coordinates of the shape's end point calculated using the current center point, length, and angle.
        Assumes that shapes are symmetrical around body position
        :return: (x,y) tuple of end point coordinates
        """
        x = self.body.position[0] + math.sin(self.angle()) * self.length / 2
        y = self.body.position[1] - math.cos(self.angle()) * self.length / 2
        return x, y

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

            angle_degrees = math.degrees(self.body.angle)
            rotated_logo_img = pygame.transform.rotate(self.image, angle_degrees)

            offset = Vec2d(rotated_logo_img.get_size()) / 2.
            p -= offset

            screen.blit(rotated_logo_img, p)
