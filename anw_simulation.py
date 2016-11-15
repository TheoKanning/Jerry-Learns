import pygame
import pymunk
import sys
from human_body_constants import BODY_COLLISION_TYPE
from human_body import HumanBody
from pygame.locals import *
from pygame.color import *

SCREEN_WIDTH = 1500


def add_ground(space):
    """
    Adds a ground line to the specified space object
    :param space: pymunk space
    :return: line segment
    """
    line_body = pymunk.Body()
    line_body.position = (0, 0)
    segment = pymunk.Segment(line_body, (-300, 0), (SCREEN_WIDTH, 0), 5)
    segment.friction = 1
    space.add(segment)
    return segment


def main():
    pygame.init()
    screen = pygame.display.set_mode((1500, 600))
    pygame.display.set_caption("ANW Simulation")
    clock = pygame.time.Clock()
    running = True

    space = pymunk.Space()
    space.gravity = (0.0, -900.0)
    space.add_collision_handler(BODY_COLLISION_TYPE, BODY_COLLISION_TYPE, begin=lambda x, y: False)

    add_ground(space)

    body = HumanBody()
    body.add_to_space(space)

    while running:
        screen.fill(THECOLORS["white"])

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        body.draw(screen)
        space.step(1 / 50.0)
        pygame.display.flip()
        clock.tick(50)


if __name__ == '__main__':
    sys.exit(main())
