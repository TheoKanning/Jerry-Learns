import sys
import walking_simulation as walk
from neat import nn, population
import os
import record

stats = walk.PopulationStats()
sim = walk.WalkingSimulation()
record_genomes = False


def population_fitness(genomes):
    """
    Calculates the fitness score of each genome in a population
    :param genomes: list of genomes
    """
    stats.individual_number = 1
    for g in genomes:
        net = nn.create_feed_forward_phenotype(g)
        last_fitness = sim.evaluate_network(net)
        stats.last_fitness = last_fitness
        g.fitness = last_fitness

        #  move this logic into population stats
        if last_fitness > stats.max_fitness:
            stats.max_fitness = last_fitness
            if record_genomes:
                record.save_genome(g, last_fitness, stats.generation)
        stats.individual_number += 1

    stats.generation += 1


def main():
    if record_genomes:
        record.create_folder()

    sim.create()

    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'neat_config')
    pop = population.Population(config_path)
    pop.add_reporter(stats.reporter)
    pop.run(population_fitness, 10)


if __name__ == '__main__':
    sys.exit(main())
