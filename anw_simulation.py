import pygame

import math
import pymunk
import sys
import os
from human_body_constants import UPPER_COLLISION_TYPE
from human_body_constants import LOWER_COLLISION_TYPE
from human_body_constants import GROUND_COLLISION_TYPE
from human_body import HumanBody
from pygame.locals import *
from pygame.color import *
from pygame.font import Font
from neat import nn, population, statistics

SCREEN_WIDTH = 1500

body_hit_ground = False

screen = pygame.display.set_mode((1500, 600))

generation = 0
individual_number = 0
population_size = 0
max_fitness = 0


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


def population_fitness(genomes):
    """
    Calculates the fitness score of each genome in a population
    :param genomes: list of genomes
    """
    global max_fitness, individual_number, population_size
    population_size = len(genomes)
    individual_number = 1
    for g in genomes:
        net = nn.create_feed_forward_phenotype(g)
        fitness = evaluate_network(net)
        g.fitness = fitness
        max_fitness = max(fitness, max_fitness)
        individual_number += 1


def evaluate_network(network):
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

    current_distance = 0

    while running:
        screen.fill(THECOLORS["white"])

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        if body_hit_ground:
            running = False

        inputs = body.get_state()
        outputs = network.serial_activate(inputs)
        body.set_rates(outputs)

        current_distance = body.get_distance()
        text_list = ["Generation: {}".format(generation),
                     "Individual: {}/{}".format(individual_number, population_size),
                     "Max Distance: {:.0f}".format(max_fitness),
                     "Current distance: {:.0f}".format(current_distance)]
        draw_text(screen, text_list)

        body.draw(screen)
        space.step(1 / 50.0)
        pygame.display.flip()
        clock.tick(50)

    return current_distance


def main():
    pygame.init()
    pygame.display.set_caption("ANW Simulation")

    local_dir = os.path.dirname(__file__)

    config_path = os.path.join(local_dir, 'neat_config')
    pop = population.Population(config_path)
    pop.run(population_fitness, 5)


if __name__ == '__main__':
    sys.exit(main())
