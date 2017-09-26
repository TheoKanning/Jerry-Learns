from neat import statistics


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


