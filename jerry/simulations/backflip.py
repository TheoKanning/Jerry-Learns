import os

import neat

from ..calculator import MotionCalculator
from ..config import Config
from ..fitness import FitnessCalculator
from ..body import BodyCommand
from math import pi
import jerry.body as body

SHOULDER_ANGLE = 0
ELBOW_ANGLE = 0
HIP_ANGLE = 0
KNEE_ANGLE = 0
ANKLE_ANGLE = (pi / 2)

# starting joint angles
joint_angles = body.JointAngles(neck=0,
                                left_shoulder=SHOULDER_ANGLE,
                                left_elbow=ELBOW_ANGLE,
                                right_shoulder=SHOULDER_ANGLE,
                                right_elbow=ELBOW_ANGLE,
                                left_hip=HIP_ANGLE,
                                left_knee=KNEE_ANGLE,
                                left_ankle=ANKLE_ANGLE,
                                right_hip=HIP_ANGLE,
                                right_knee=KNEE_ANGLE,
                                right_ankle=ANKLE_ANGLE)


class NeatBackflipMotionCalculator(MotionCalculator):
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
