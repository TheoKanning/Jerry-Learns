import sys
import walking_simulation as walk
from neat import nn, population
import os
import record
import neat

stats = walk.PopulationStats()
sim = walk.WalkingSimulation()
record_genomes = False


def population_fitness(genomes, config):
    """
    Calculates the fitness score of each genome in a population
    :param genomes: list of genomes
    :param config: NEAT config
    """
    stats.individual_number = 1
    for genome_id, genome in genomes:
        net = nn.FeedForwardNetwork.create(genome, config)
        last_fitness = sim.evaluate_network(net)
        stats.last_fitness = last_fitness
        genome.fitness = last_fitness

        #  move this logic into population stats
        if last_fitness > stats.max_fitness:
            stats.max_fitness = last_fitness
            if record_genomes:
                record.save_genome(genome, last_fitness, stats.generation)
        stats.individual_number += 1

    stats.generation += 1


def main():
    if record_genomes:
        record.create_folder()

    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'neat_config')
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    pop = population.Population(config)
    pop.add_reporter(stats.reporter)
    pop.run(population_fitness, n=10)


if __name__ == '__main__':
    sys.exit(main())
