import pymunk
import pymunk.pygame_util
from pymunk import Vec2d
from conversion import to_pygame
import math
import pygame.transform

SEGMENT_WIDTH = 5
FRICTION = 1

IMAGE_SIZE_RATIO = 1.15

"""
Class that represents one segment of the human body, i.e. upper arm, thigh.
"""


class Segment:
    def __init__(self, segment_info, starting_position, angle=0,):
        """
        :param segment_info: SegmentInfo object containing all pre-defined segment constants
        :param starting_position: (x, y) tuple of location of attachment point
        :param angle: angle in radians relative to vertical, in absolute coordinates
        :return: nothing
        """
        length = segment_info.length
        inertia = pymunk.moment_for_segment(segment_info.mass, (length / 2, 0), (-length / 2, 0), 1)

        self.body = pymunk.Body(segment_info.mass, inertia)
        self.length = length
        x = length * math.sin(angle)
        y = -length * math.cos(angle)
        self.body.position = (starting_position[0] + x / 2, starting_position[1] + y / 2)
        self.body.angle = angle
        self.shape = pymunk.Segment(self.body, (0, length / 2), (0, -length / 2), SEGMENT_WIDTH)
        self.shape.collision_type = segment_info.collision_type
        self.shape.friction = FRICTION

        image = segment_info.image
        if image is not None:
            ratio = length / image.get_height() * IMAGE_SIZE_RATIO
            new_width = int(image.get_width() * ratio)
            image = pygame.transform.scale(image, (new_width, int(length * IMAGE_SIZE_RATIO)))
        self.image = image

    def get_rate(self):
        """
        :return: angular rate in rad/s
        """
        return self.body.angular_velocity

    def get_angle(self):
        """
        Returns the absolute angle of this segment the pymunk coordinate system
        :return: angle in radians
        """

        return self.body.angle

    def get_start_point(self):
        """
        Returns the coordinates of the shape's start point
        :return: (x,y) tuple of start point coordinates
        """
        return self.shape.body.position + self.shape.a.rotated(self.body.angle)

    def get_end_point(self):
        """
        Returns the coordinates of the shape's end point
        :return: (x,y) tuple of end point coordinates
        """
        return self.shape.body.position + self.shape.b.rotated(self.body.angle)

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
            pymunk.pygame_util.draw(screen, self.shape)
        else:
            p = self.body.position
            p = Vec2d(to_pygame(p))

            # divide by two because it works
            angle_degrees = math.degrees(self.body.angle)
            rotated_logo_img = pygame.transform.rotate(self.image, angle_degrees)

            offset = Vec2d(rotated_logo_img.get_size()) / 2.
            p -= offset

            screen.blit(rotated_logo_img, p)
