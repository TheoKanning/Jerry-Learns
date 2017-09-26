import sys

import fitness
import pygame
import pymunk
from human_body import HumanBody

from jerry import termination
from jerry.human_body_constants import collision_types

SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 600


def scale_outputs(outputs):
    """
    Scale neural network outputs between -3 and 3
    :param outputs: outputs of neural network, scaled from -1 to 1 from tanh activation
    :return: scaled outputs that can be used to set body rate
    """
    return [3 * x for x in outputs]


def add_ground(space):
    """
    Adds a ground line to the specified space object
    :param space: pymunk space
    """
    segment = pymunk.Segment(space.static_body, (-300, 0), (SCREEN_WIDTH, 0), 5)
    segment.friction = .9
    segment.collision_type = collision_types["ground"]
    space.add(segment)


def set_collision_handlers(space, fall_callback):
    """
    Upper and lower body don't collide with themselves or with each other.
    If upper body touches ground, end the simulation
    :param space: pymunk space
    :param fall_callback: function to be called a fall is detected
    """

    def dont_collide(x, y, z):
        return False

    def fall(x, y, z):
        fall_callback()
        return True

    space.add_collision_handler(collision_types["upper"], collision_types["upper"]).begin = dont_collide
    space.add_collision_handler(collision_types["lower"], collision_types["upper"]).begin = dont_collide
    space.add_collision_handler(collision_types["lower"], collision_types["lower"]).begin = dont_collide
    space.add_collision_handler(collision_types["upper"], collision_types["ground"]).begin = fall


def create_space(fall_callback):
    """
    Creates a pymunk space to hold a new simulation, adds default changes
    :param fall_callback: callback that's called when the space detects a fall
    :return: space with collision handlers and ground
    """
    space = pymunk.Space()
    space.gravity = (0.0, -900.0)
    set_collision_handlers(space, fall_callback)
    add_ground(space)
    return space


class WalkingSimulation:
    def __init__(self, population_stats, record_genomes=False, record_frames=False):
        """
        :param record_genomes: whether or not to store each pickled genome each time one beats the previous max
        """

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.record_genomes = record_genomes

        self.population_stats = population_stats
        self.record_frames = record_frames

        pygame.init()
        pygame.display.set_caption("Jerry's First Steps")

    def draw_stats(self):
        """
        Draws all stats on the screen
        """
        font = pygame.font.Font(None, 36)
        offset = 8
        for text in self.population_stats.stats_list():
            surface = font.render(text, 1, (0, 0, 0))
            self.screen.blit(surface, (8, offset))
            offset += font.get_height()

        offset = 8
        for stat in self.population_stats.generation_history():
            surface = font.render(stat, 1, (0, 0, 0))
            self.screen.blit(surface, (300, offset))
            offset += font.get_height()

    def draw_vertical_line(self, x_pos):
        """
        Draws a vertical line at the specified position
        :param x_pos: the x coordinate of this line
        """
        pygame.draw.line(self.screen, (0, 0, 0), (x_pos, 0), (x_pos, SCREEN_HEIGHT))

    def evaluate_network(self, network):
        clock = pygame.time.Clock()

        run_terminator = termination.RunTerminator()
        # todo pass in the class and instantiate here
        fitness_calculator = fitness.WalkingFitnessCalculator()

        def fall_callback():
            run_terminator.fall()

        space = create_space(fall_callback)

        body = HumanBody()
        body.add_to_space(space)

        frame = 0

        while not run_terminator.run_complete():
            self.screen.fill(pygame.Color("white"))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            fitness_calculator.update(body)

            run_terminator.update(body)

            inputs = body.get_state()
            outputs = scale_outputs(network.activate(inputs))
            body.set_rates(outputs)

            self.draw_stats()
            self.draw_vertical_line(self.population_stats.max_fitness)
            self.draw_vertical_line(fitness_calculator.get_fitness())
            body.draw(self.screen)

            if self.record_frames:
                pygame.image.save(self.screen, "records/{}.jpg".format(frame))
                frame += 1

            space.step(1 / 50.0)
            pygame.display.flip()
            clock.tick(50)

        return fitness_calculator.get_fitness()
