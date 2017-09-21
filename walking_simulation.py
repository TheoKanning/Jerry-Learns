import pygame
import pymunk
import sys
from human_body_constants import collision_types
from human_body_constants import STARTING_X_POSITION
from human_body import HumanBody
from neat import statistics

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
        self.reporter = statistics.StatisticsReporter()

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
        fitness_history = self.reporter.get_fitness_mean()
        start_generation = max(0, len(fitness_history) - 5)
        start_generation += 1  # plus one so this is no longer zero-indexed
        stats = []
        last_five_generations = fitness_history[-5:]
        for gen, fitness in enumerate(last_five_generations):
            stat = "Generation {} Average: {:.0f}".format(gen + start_generation, fitness)
            stats.append(stat)

        return stats


class RunStats:
    """
    Class that maintains the history of a single simulation. Returns fitness score when run is complete.
    """

    def __init__(self):
        self.fall_time = None
        self.max_distance = STARTING_X_POSITION
        self.scaled_distance = STARTING_X_POSITION
        self.last_progress_time = pygame.time.get_ticks()

    def update(self, distance, multiplier):
        """
        Updates internal state with new distance and score multiplier
        :param distance: absolute distance traveled
        :param multiplier: score multiplier based on mody angle etc
        """
        if self.has_fallen():
            # don't update score after falling
            return

        if distance > self.max_distance:
            # multiply new distance by current score multiplier
            self.scaled_distance += multiplier * (distance - self.max_distance)
            self.max_distance = distance
            self.last_progress_time = pygame.time.get_ticks()

    def get_fitness(self):
        return self.scaled_distance - STARTING_X_POSITION

    def fall(self):
        """
        Called to signal that Jerry has fallen, only count first fall time.
        """
        if self.fall_time is None:
            self.fall_time = pygame.time.get_ticks()

    def has_fallen(self):
        return self.fall_time is not None

    def run_complete(self):
        """
        Returns true if the current run should be stopped
        """
        current_time = pygame.time.get_ticks()

        if self.has_fallen() and current_time - self.fall_time > FALL_SIM_TIME:
            return True
        elif current_time - self.last_progress_time > PROGRESS_TIMEOUT:
            return True
        else:
            return False


class WalkingSimulation:
    def __init__(self, record_genomes=False, record_frames=False):
        """
        :param record_genomes: whether or not to store each pickled genome each time one beats the previous max
        """

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.record_genomes = record_genomes

        self.population_stats = PopulationStats()
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

    def evaluate_network(self, network, population_stats):
        # todo determine where these stats should be stored and how to update them
        self.population_stats = population_stats
        clock = pygame.time.Clock()

        run_stats = RunStats()

        def fall_callback():
            run_stats.fall()

        space = create_space(fall_callback)

        body = HumanBody()
        body.add_to_space(space)

        frame = 0

        while not run_stats.run_complete():
            self.screen.fill(pygame.Color("white"))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            run_stats.update(body.get_distance(), body.get_score_multiplier())

            inputs = body.get_state()
            outputs = scale_outputs(network.activate(inputs))
            body.set_rates(outputs)

            self.draw_stats()
            self.draw_vertical_line(self.population_stats.max_fitness + STARTING_X_POSITION)
            self.draw_vertical_line(run_stats.scaled_distance)
            body.draw(self.screen)

            if self.record_frames:
                pygame.image.save(self.screen, "records/{}.jpg".format(frame))
                frame += 1

            space.step(1 / 50.0)
            pygame.display.flip()
            clock.tick(50)

        return run_stats.get_fitness()
