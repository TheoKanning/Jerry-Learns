from math import pi
from joint import Joint
from segment import Segment
import pymunk
import pymunk.pygame_util

# Collision Types #
BODY_COLLISION_TYPE = 25

# Weight Fractions #
HEAD_WEIGHT_FRACTION = 0.0826
TORSO_WEIGHT_FRACTION = 0.551
UPPER_ARM_WEIGHT_FRACTION = 0.0325
FOREARM_WEIGHT_FRACTION = 0.0187 + 0.0065  # Including hand
THIGH_WEIGHT_FRACTION = 0.105
LEG_WEIGHT_FRACTION = 0.0475
FOOT_WEIGHT_FRACTION = 0.0143

# Height Fractions #
HEAD_HEIGHT_FRACTION = 0.1075
TORSO_HEIGHT_FRACTION = 0.3
UPPER_ARM_HEIGHT_FRACTION = 0.172
FOREARM_HEIGHT_FRACTION = 0.157  # Not including hand
THIGH_HEIGHT_FRACTION = 0.232
LEG_HEIGHT_FRACTION = 0.247
FOOT_HEIGHT_FRACTION = 0.1  # Counts foot length, not height

# Starting Height Fractions #
SHOULDER_STARTING_HEIGHT_FRACTION = LEG_HEIGHT_FRACTION + THIGH_HEIGHT_FRACTION + TORSO_HEIGHT_FRACTION
ELBOW_STARTING_HEIGHT_FRACTION = LEG_HEIGHT_FRACTION + THIGH_HEIGHT_FRACTION + TORSO_HEIGHT_FRACTION - UPPER_ARM_HEIGHT_FRACTION / 2
HIP_STARTING_HEIGHT_FRACTION = LEG_HEIGHT_FRACTION + THIGH_HEIGHT_FRACTION
KNEE_STARTING_HEIGHT_FRACTION = LEG_HEIGHT_FRACTION
FOOT_STARTING_HEIGHT_FRACTION = 0

# Joint Constraints #
ELBOW_MIN_ANGLE = 0
ELBOW_MAX_ANGLE = 3 * pi / 4
SHOULDER_MIN_ANGLE = -pi / 2
SHOULDER_MAX_ANGLE = pi
HIP_MIN_ANGLE = 0
HIP_MAX_ANGLE = 3 * pi / 4
KNEE_MIN_ANGLE = -2 * pi / 3
KNEE_MAX_ANGLE = 0
ANKLE_MIN_ANGLE = -pi / 4
ANKLE_MAX_ANGLE = pi / 4

# Size and Weight Constants
TOTAL_MASS = 80  # Made up units
TOTAL_HEIGHT = 300  # Pygame pixels
STARTING_X_POSITION = 300
STARTING_Y_POSITION = 150
SEGMENT_WIDTH = 5
FRICTION = 1

# Segment Masses
TORSO_MASS = TOTAL_MASS * TORSO_WEIGHT_FRACTION
THIGH_MASS = TOTAL_MASS * THIGH_WEIGHT_FRACTION
LEG_MASS = TOTAL_MASS * LEG_WEIGHT_FRACTION
FOOT_MASS = TOTAL_MASS * FOOT_WEIGHT_FRACTION

# Segment Lengths
TORSO_LENGTH = TORSO_HEIGHT_FRACTION * TOTAL_HEIGHT
THIGH_LENGTH = THIGH_HEIGHT_FRACTION * TOTAL_HEIGHT
LEG_LENGTH = LEG_HEIGHT_FRACTION * TOTAL_HEIGHT
FOOT_LENGTH = FOOT_HEIGHT_FRACTION * TOTAL_HEIGHT

# Starting Positions
TORSO_POSITION = STARTING_X_POSITION, TOTAL_HEIGHT * HIP_STARTING_HEIGHT_FRACTION + TORSO_LENGTH / 2 + STARTING_Y_POSITION
THIGH_POSITION = STARTING_X_POSITION + 1, TOTAL_HEIGHT * KNEE_STARTING_HEIGHT_FRACTION + THIGH_LENGTH / 2 + STARTING_Y_POSITION
LEG_POSITION = STARTING_X_POSITION, LEG_LENGTH / 2 + STARTING_Y_POSITION
FOOT_POSITION = STARTING_X_POSITION + FOOT_LENGTH / 2, STARTING_Y_POSITION


class HumanBody:
    def __init__(self):
        self.torso = Segment(TORSO_MASS, TORSO_LENGTH, TORSO_POSITION, BODY_COLLISION_TYPE)
        self.left_thigh = Segment(THIGH_MASS, THIGH_LENGTH, THIGH_POSITION, BODY_COLLISION_TYPE)
        self.left_leg = Segment(LEG_MASS, LEG_LENGTH, LEG_POSITION, BODY_COLLISION_TYPE)
        self.left_foot = Segment(FOOT_MASS, FOOT_LENGTH, FOOT_POSITION, BODY_COLLISION_TYPE)

        self.left_hip = Joint(self.torso, self.left_thigh, (HIP_MIN_ANGLE, HIP_MAX_ANGLE), 100)
        self.left_knee = Joint(self.left_thigh, self.left_leg, (KNEE_MIN_ANGLE, KNEE_MAX_ANGLE), 100)
        self.left_ankle = Joint(self.left_leg, self.left_foot, (ANKLE_MIN_ANGLE, ANKLE_MAX_ANGLE), 100)

    def draw(self, screen):
        """
        Draws all bodies using the supplied pygame screen
        :param screen: pygame screen
        """
        self.torso.draw(screen)
        self.left_thigh.draw(screen)
        self.left_leg.draw(screen)
        self.left_foot.draw(screen)

    def add_to_space(self, space):
        """
        Adds all relevant bodies, shapes, and constraints to the given pymunk space
        :param space: pymunk space
        :return: nothing
        """
        self.torso.add_to_space(space)
        self.left_thigh.add_to_space(space)
        self.left_leg.add_to_space(space)
        self.left_foot.add_to_space(space)
        self.left_hip.add_to_space(space)
        self.left_knee.add_to_space(space)
        self.left_ankle.add_to_space(space)
