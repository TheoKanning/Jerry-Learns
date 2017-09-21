import pygame
from neat import statistics

from human_body_constants import STARTING_X_POSITION

PROGRESS_TIMEOUT = 2000  # end if no progress is made for this many
FALL_SIM_TIME = 500  # continue simulating for half second after a fall


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
        self.last_progress_time = pygame.time.get_ticks()

    def update(self, body):
        """
        Updates internal state with last progress time
        :param body: simulated body object
        """
        if self.has_fallen():
            # don't update score after falling
            return

        distance = body.get_distance()
        if distance > self.max_distance:
            self.last_progress_time = pygame.time.get_ticks()
            self.max_distance = distance

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
