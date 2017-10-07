import os

import neat

from ..calculator import MotionCalculator
from ..config import Config
from ..fitness import FitnessCalculator
from ..body import BodyCommand
from math import pi
import jerry.body as body

SHOULDER_ANGLE = -pi / 6
ELBOW_ANGLE = 0
HIP_ANGLE = pi / 2
KNEE_ANGLE = -pi / 2
ANKLE_ANGLE = (2 * pi / 3)

# starting joint angles
joint_angles = body.JointAngles(neck=pi,
                                left_shoulder=SHOULDER_ANGLE,
                                left_elbow=ELBOW_ANGLE,
                                right_shoulder=SHOULDER_ANGLE,
                                right_elbow=ELBOW_ANGLE,
                                torso=-pi / 6,
                                left_hip=HIP_ANGLE,
                                left_knee=KNEE_ANGLE,
                                left_ankle=ANKLE_ANGLE,
                                right_hip=HIP_ANGLE,
                                right_knee=KNEE_ANGLE,
                                right_ankle=ANKLE_ANGLE,
                                x_position=700,
                                y_position=220)


class NeatBackflipMotionCalculator(MotionCalculator):
    def __init__(self, network):
        """
        :param network: NEAT network
        """
        super()
        self.network = network
        self.first_outputs = None

    def calculate(self, body_state):
        """
        Calculate commands from current state
        :param body_state: BodyState object
        :return: BodyCommand object
        """
        outputs = self.network.activate(body_state)
        command = BodyCommand(*outputs)
        if self.first_outputs is None:
            self.first_outputs = outputs
            print("\n\nStarting new simulation")

        sum_error = 0
        for (first, current) in zip(self.first_outputs, outputs):
            sum_error += abs(first - current)

        print("{0:.3f}".format(sum_error/len(outputs)))
        return command


class BackflipFitnessCalculator(FitnessCalculator):
    def __init__(self):
        self.max_distance = 0
        self.total_rotation = 0
        self.last_angle = None

    def update(self, body):
        angle = body.get_angle()
        if self.last_angle is not None:
            self.total_rotation += angle - self.last_angle

        self.last_angle = angle

    def get_fitness(self):
        return self.total_rotation * 50


class BackflipConfig(Config):
    def get_motion_calculator(self, network):
        return NeatBackflipMotionCalculator(network)

    def get_fitness_calculator(self):
        return BackflipFitnessCalculator()

    def get_neat_config(self):
        local_dir = os.path.dirname(__file__)
        config_path = os.path.join(local_dir, 'backflip_neat_config')
        config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                             neat.DefaultSpeciesSet, neat.DefaultStagnation,
                             config_path)
        return config

    def get_body(self):
        return body.Body(joint_angles)
