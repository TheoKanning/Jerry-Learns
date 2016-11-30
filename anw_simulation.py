import pygame
import pymunk
import sys
import os
from human_body_constants import UPPER_COLLISION_TYPE
from human_body_constants import LOWER_COLLISION_TYPE
from human_body_constants import GROUND_COLLISION_TYPE
from human_body_constants import STARTING_X_POSITION
from human_body import HumanBody
from pygame.locals import *
from pygame.color import *
from pygame.font import Font
from neat import nn, population

SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 600

PROGRESS_TIMEOUT = 5000  # end ig no progress is made for five seconds
FALL_SIM_TIME = 500  # continue simulating for half second after a fall

body_hit_ground = False

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

NUM_GENERATIONS = 100
generation = 1
individual_number = 1
population_size = 0
max_fitness = 0
last_fitness = 0

reporter = population.StatisticsReporter()


def add_ground(space):
    """
    Adds a ground line to the specified space object
    :param space: pymunk space
    :return: line segment
    """
    segment = pymunk.Segment(space.static_body, (-300, 0), (SCREEN_WIDTH, 0), 5)
    segment.friction = .9
    segment.collision_type = GROUND_COLLISION_TYPE
    space.add(segment)
    return segment


def set_collision_handlers(space):
    """
    Upper and lower body don't collide with themselves or with each other.
    If upper body touches ground, end the simulation
    :param space: pymunk space
    """

    def dont_collide(x, y, z):
        return False

    space.add_collision_handler(UPPER_COLLISION_TYPE, UPPER_COLLISION_TYPE).begin = dont_collide
    space.add_collision_handler(LOWER_COLLISION_TYPE, UPPER_COLLISION_TYPE).begin = dont_collide
    space.add_collision_handler(LOWER_COLLISION_TYPE, LOWER_COLLISION_TYPE).begin = dont_collide
    space.add_collision_handler(UPPER_COLLISION_TYPE, GROUND_COLLISION_TYPE).begin = end_simulation


def end_simulation(x, y, z):
    global body_hit_ground
    body_hit_ground = True
    return True


def draw_stats():
    """
    Draws all stats on the screen
    """
    text_list = ["Generation: {}".format(generation),
                 "Individual: {}".format(individual_number),
                 "Max Fitness: {:.0f}".format(max_fitness),
                 "Last Fitness: {:.0f}".format(last_fitness)]

    font = Font(None, 36)
    offset = 8
    for text in text_list:
        surface = font.render(text, 1, (0, 0, 0))
        screen.blit(surface, (8, offset))
        offset += font.get_height()

    # Show last five generations
    offset = 8
    fitness_history = reporter.get_average_fitness()
    start_generation = max(0, len(fitness_history) - 5)
    start_generation += 1  # plus one so this is no longer zero-indexed
    for gen, fitness in enumerate(fitness_history[-5:]):
        text = "Generation {} Average: {:.0f}".format(gen + start_generation, fitness)
        surface = font.render(text, 1, (0, 0, 0))
        screen.blit(surface, (300, offset))
        offset += font.get_height()


def draw_vertical_line(x_pos):
    """
    Draws a vertical line at the specified position
    :param x_pos: the x coordinate of this line
    """
    pygame.draw.line(screen, (0, 0, 0), (x_pos, 0), (x_pos, SCREEN_HEIGHT))


def population_fitness(genomes):
    """
    Calculates the fitness score of each genome in a population
    :param genomes: list of genomes
    """
    global max_fitness, individual_number, population_size, generation, last_fitness
    population_size = len(genomes)
    individual_number = 1
    for g in genomes:
        net = nn.create_feed_forward_phenotype(g)
        last_fitness = evaluate_network(net)
        g.fitness = last_fitness
        max_fitness = max(last_fitness, max_fitness)
        individual_number += 1
    generation += 1


def scale_outputs(outputs):
    """
    Scale neural network outputs between -3 and 3
    :param outputs: outputs of neural network, scaled from -1 to 1 from tanh activation
    :return: scaled outputs that can be used to set body rate
    """
    return [3 * x for x in outputs]


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

    current_scaled_distance = STARTING_X_POSITION
    max_distance = STARTING_X_POSITION

    last_progress_time = pygame.time.get_ticks()
    fall_time = None

    initial_outputs = None

    while running:
        screen.fill(THECOLORS["white"])
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        if body_hit_ground:
            if fall_time is None:
                fall_time = current_time
            elif current_time - fall_time > FALL_SIM_TIME:
                running = False
        elif body.get_distance() > max_distance:
            # take distance improvement and reward staying vertical
            # only count distance before fall
            current_scaled_distance += body.get_score_multiplier() * (body.get_distance() - max_distance)
            max_distance = body.get_distance()
            last_progress_time = current_time
        elif current_time - last_progress_time > PROGRESS_TIMEOUT:
            running = False  # end if no progress in last three seconds

        inputs = body.get_state()
        outputs = scale_outputs(network.serial_activate(inputs))
        body.set_rates(outputs)

        if initial_outputs is None:
            initial_outputs = outputs

        draw_stats()
        draw_vertical_line(max_fitness + STARTING_X_POSITION)
        draw_vertical_line(current_scaled_distance)
        body.draw(screen)

        space.step(1 / 50.0)
        pygame.display.flip()
        clock.tick(50)

    # uncomment to see how much network outputs are changing
    changes = [abs(a - b) for a, b in zip(outputs, initial_outputs)]
    print sum(changes) / len(changes)
    count = 0
    for x in outputs:
        if x > 2.99 or x < -2.99:
            count += 1
    print count

    return current_scaled_distance - STARTING_X_POSITION


def main():
    pygame.init()
    pygame.display.set_caption("Jerry's First Steps")

    local_dir = os.path.dirname(__file__)

    config_path = os.path.join(local_dir, 'neat_config')
    pop = population.Population(config_path)
    global reporter
    pop.add_reporter(reporter)
    pop.run(population_fitness, NUM_GENERATIONS)


if __name__ == '__main__':
    sys.exit(main())
