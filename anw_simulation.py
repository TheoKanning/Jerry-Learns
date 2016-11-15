import pygame
import pymunk
import sys
from human_body_constants import UPPER_COLLISION_TYPE
from human_body_constants import LOWER_COLLISION_TYPE
from human_body_constants import GROUND_COLLISION_TYPE
from human_body import HumanBody
from pygame.locals import *
from pygame.color import *
from pygame.font import Font

SCREEN_WIDTH = 1500

body_hit_ground = False


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
    segment.collision_type = GROUND_COLLISION_TYPE
    space.add(segment)
    return segment


def set_collision_handlers(space):
    """
    Upper and lower body don't collide with themselves or with each other.
    If upper body touches ground, end the simulation
    :param space: pymunk space
    """
    space.add_collision_handler(UPPER_COLLISION_TYPE, UPPER_COLLISION_TYPE, begin=lambda x, y: False)
    space.add_collision_handler(LOWER_COLLISION_TYPE, UPPER_COLLISION_TYPE, begin=lambda x, y: False)
    space.add_collision_handler(LOWER_COLLISION_TYPE, LOWER_COLLISION_TYPE, begin=lambda x, y: False)
    space.add_collision_handler(UPPER_COLLISION_TYPE, GROUND_COLLISION_TYPE, begin=end_simulation)


def end_simulation(x, y):
    global body_hit_ground
    body_hit_ground = True
    print "Hitting ground"
    return True


def draw_text(screen, text_list):
    """
    Draws any number of text strings onto the screen
    :param screen: pygame screen
    :param text_list: list of string to draw
    """
    font = Font(None, 24)
    offset = 8
    for text in text_list:
        surface = font.render(text, 1, (0, 0, 0))
        screen.blit(surface, (8, offset))
        offset += font.get_height()


def calculate_fitness(screen):
    clock = pygame.time.Clock()
    running = True
    global body_hit_ground
    body_hit_ground = False

    space = pymunk.Space()
    space.gravity = (0.0, -900.0)
    set_collision_handlers(space)
    add_ground(space)

    body = HumanBody()
    body.add_to_space(space)

    while running:
        screen.fill(THECOLORS["white"])

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        if body_hit_ground:
            print "Body hit ground"
            running = False

        text_list = ["text 1", "text 2"]
        draw_text(screen, text_list)

        body.draw(screen)
        space.step(1 / 50.0)
        pygame.display.flip()
        clock.tick(50)

    return body.get_distance()


def main():
    pygame.init()
    screen = pygame.display.set_mode((1500, 600))
    pygame.display.set_caption("ANW Simulation")

    calculate_fitness(screen)
    calculate_fitness(screen)


if __name__ == '__main__':
    sys.exit(main())
