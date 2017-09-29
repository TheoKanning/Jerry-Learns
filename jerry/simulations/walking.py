import os

import neat

from ..calculator import MotionCalculator
from ..config import Config
from ..fitness import FitnessCalculator
from ..human_body import BodyCommand


class NeatWalkingMotionCalculator(MotionCalculator):
    # If more Neat calculators are added, create a super class to handle converting between tuples and Neat arrays
    def __init__(self, network):
        """
        :param network: NEAT network
        """
        super()
        self.network = network

    def calculate(self, body_state):
        """
        Calculate commands from current state
        :param body_state: BodyState object
        :return: BodyCommand object
        """
        outputs = self.scale_outputs(self.network.activate(body_state))
        command = BodyCommand(*outputs)
        return command

    def scale_outputs(self, outputs):
        # todo output scaling is still bad, Jerry hardly reacts to anything
        """
        Scale neural network outputs between -3 and 3
        :param outputs: array of outputs of neural network, scaled from -1 to 1 from tanh activation
        :return: scaled outputs that can be used to set body rate
        """
        return [3 * x for x in outputs]


class WalkingFitnessCalculator(FitnessCalculator):
    # todo subtract starting x position
    def __init__(self):
        self.max_distance = 0
        self.scaled_distance = 0

    def update(self, body):
        distance = body.get_distance()
        multiplier = body.get_score_multiplier()
        if distance > self.max_distance:
            # multiply new distance by current score multiplier
            self.scaled_distance += multiplier * (distance - self.max_distance)
            self.max_distance = distance

    def get_fitness(self):
        return self.scaled_distance


class WalkingConfig(Config):
    def get_motion_calculator(self, network):
        return NeatWalkingMotionCalculator(network)

    def get_fitness_calculator(self):
        return WalkingFitnessCalculator()

    def get_neat_config(self):
        local_dir = os.path.dirname(__file__)
        config_path = os.path.join(local_dir, 'walking_neat_config')
        config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                             neat.DefaultSpeciesSet, neat.DefaultStagnation,
                             config_path)
        return config
