import os

import neat

from ..calculator import MotionCalculator
from ..config import Config
from ..fitness import FitnessCalculator
from ..human_body import BodyCommand
from math import pi

# starting joint angles
joints_angles = {
        "neck": 0,
        "left_shoulder": (- pi / 4),
        "left_elbow": (pi / 4),
        "right_shoulder": (pi / 4),
        "right_elbow": (pi / 4),
        "left_hip": (pi / 6),
        "left_knee": (- pi / 16),
        "left_ankle": (pi / 2),
        "right_hip": (-pi / 12),
        "right_knee": 0,
        "right_ankle": (pi / 2)
    }


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
        """
        Scale neural network outputs between -3 and 3
        :param outputs: array of outputs of neural network, scaled from -1 to 1 from tanh activation
        :return: scaled outputs that can be used to set body rate
        """
        # todo this scaling should be a part of the body since it could change if different command options (torques) are added
        return [3 * x for x in outputs]


class WalkingFitnessCalculator(FitnessCalculator):
    def __init__(self):
        self.max_distance = 0
        self.scaled_distance = 0
        self.includes_start = True

    def update(self, body):
        if self.includes_start:
            # Remove starting distance from calculation
            self.scaled_distance -= body.get_distance()
            self.includes_start = False

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

    def get_joint_angles(self):
        return joints_angles
