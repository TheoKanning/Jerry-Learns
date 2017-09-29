import os
import sys

import neat
from neat import nn, population

from jerry import calculator as calc
from jerry import fitness
from jerry import record, stats
from jerry import simulator

pop_stats = stats.PopulationStats()
sim = simulator.Simulator(pop_stats)
record_genomes = False


def get_fitness_calculator():
    return fitness.WalkingFitnessCalculator()


def population_fitness(genomes, config):
    """
    Calculates the fitness score of each genome in a population
    :param genomes: list of genomes
    :param config: NEAT config
    """
    pop_stats.individual_number = 1
    for genome_id, genome in genomes:
        net = nn.FeedForwardNetwork.create(genome, config)
        calculator = calc.NeatWalkingMotionCalculator(net)
        last_fitness = sim.evaluate(calculator, get_fitness_calculator())
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

    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'neat_config')
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    pop = population.Population(config)
    pop.add_reporter(pop_stats.reporter)
    pop.run(population_fitness, n=10)


if __name__ == '__main__':
    sys.exit(main())
