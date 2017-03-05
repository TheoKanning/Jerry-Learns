import pygame
import pymunk
import sys
from human_body_constants import collision_types
from human_body_constants import STARTING_X_POSITION
from human_body import HumanBody
from pygame.locals import *
from pygame.color import *
from pygame.font import Font
from neat import population

SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 600

PROGRESS_TIMEOUT = 2000  # end ig no progress is made for five seconds
FALL_SIM_TIME = 500  # continue simulating for half second after a fall


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


class PopulationStats:
    """
    Class that contains all of the persisted statistics during an entire population simulation
    """

    def __init__(self):
        self.generation = 1
        self.individual_number = 1
        self.max_fitness = 0
        self.last_fitness = 0
        self.reporter = population.StatisticsReporter()

    def stats_list(self):
        """
        :return: a list of strings, each of which is a statistic to be printed
        """
        return ["Generation: {}".format(self.generation),
                "Individual: {}".format(self.individual_number),
                "Max Fitness: {:.0f}".format(self.max_fitness),
                "Last Fitness: {:.0f}".format(self.last_fitness)]

    def generation_history(self):
        """
        :return: A list of strings displaying statistics about the last 5 generations
        """
        fitness_history = self.reporter.get_average_fitness()
        start_generation = max(0, len(fitness_history) - 5)
        start_generation += 1  # plus one so this is no longer zero-indexed
        stats = []
        last_five_generations = fitness_history[-5:]
        for gen, fitness in enumerate(last_five_generations):
            stat = "Generation {} Average: {:.0f}".format(gen + start_generation, fitness)
            stats.append(stat)

        return stats


class WalkingSimulation:
    def __init__(self, record_genomes=False, record_frames=False):
        """
        :param record_genomes: whether or not to store each pickled genome each time one beats the previous max
        """

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.record_genomes = record_genomes

        self.body_hit_ground = False
        self.population_stats = PopulationStats()
        self.record_frames = record_frames
        self.frame = 0

    def create(self):
        # todo give this a better name or move into init
        pygame.init()
        pygame.display.set_caption("Jerry's First Steps")

    def draw_stats(self):
        """
        Draws all stats on the screen
        """
        font = Font(None, 36)
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
        running = True
        self.body_hit_ground = False

        def fall_callback():
            self.body_hit_ground = True

        space = create_space(fall_callback)

        body = HumanBody()
        body.add_to_space(space)

        current_scaled_distance = STARTING_X_POSITION
        max_distance = STARTING_X_POSITION

        last_progress_time = pygame.time.get_ticks()
        fall_time = None

        initial_outputs = None

        while running:
            self.screen.fill(THECOLORS["white"])
            current_time = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()

            if self.body_hit_ground:
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

            self.draw_stats()
            self.draw_vertical_line(self.population_stats.max_fitness + STARTING_X_POSITION)
            self.draw_vertical_line(current_scaled_distance)
            body.draw(self.screen)

            if self.record_frames:
                pygame.image.save(self.screen, "records/{}.jpg".format(self.frame))
                self.frame += 1

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