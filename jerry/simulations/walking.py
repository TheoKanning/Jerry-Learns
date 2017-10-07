import os

import neat

from ..calculator import MotionCalculator
from ..config import Config
from ..fitness import FitnessCalculator
from ..body import BodyCommand
from math import pi
import jerry.body as body

joint_angles = body.JointAngles(neck=pi,
                                left_shoulder=-pi / 4,
                                left_elbow=pi / 4,
                                right_shoulder=pi / 4,
                                right_elbow=pi / 4,
                                torso=-0,
                                left_hip=pi / 6,
                                left_knee=-pi / 6,
                                left_ankle=pi / 2,
                                right_hip=-pi / 12,
                                right_knee=0,
                                right_ankle=pi / 2,
                                x_position=100,
                                y_position=278)


class NeatWalkingMotionCalculator(MotionCalculator):
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
        outputs = self.network.activate(body_state)
        command = BodyCommand(*outputs)
        return command


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

    def get_body(self):
        return body.Body(joint_angles)
