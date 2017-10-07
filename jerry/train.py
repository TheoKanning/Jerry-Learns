import sys

from neat import nn, population

from jerry import record, stats
from jerry import simulator
from jerry.simulations import backflip, walking

pop_stats = stats.PopulationStats()
sim = simulator.Simulator(pop_stats)
record_genomes = False
simulation_config = walking.WalkingConfig()


def population_fitness(genomes, neat_config):
    """
    Calculates the fitness score of each genome in a population
    :param genomes: list of genomes
    :param neat_config: NEAT config
    """
    pop_stats.individual_number = 1
    for genome_id, genome in genomes:
        net = nn.FeedForwardNetwork.create(genome, neat_config)
        body = simulation_config.get_body()
        motion_calculator = simulation_config.get_motion_calculator(net)
        fitness_calculator = simulation_config.get_fitness_calculator()
        last_fitness = sim.evaluate(body, motion_calculator, fitness_calculator)

        pop_stats.last_fitness = last_fitness
        genome.fitness = last_fitness

        # todo move this logic into population stats
        if last_fitness > pop_stats.max_fitness:
            pop_stats.max_fitness = last_fitness
            if record_genomes:
                record.save_genome(genome, last_fitness, pop_stats.generation)
        pop_stats.next_individual()

    pop_stats.next_generation()


def main():
    if record_genomes:
        record.create_folder()

    config = simulation_config.get_neat_config()
    pop = population.Population(config)
    pop.add_reporter(pop_stats.reporter)
    pop.run(population_fitness, n=100)


if __name__ == '__main__':
    sys.exit(main())
