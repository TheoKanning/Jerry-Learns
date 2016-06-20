from math import pi
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
FOOT_HEIGHT_FRACTION = 0.0425

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
FOOT_MIN_ANGLE = -pi / 4
FOOT_MAX_ANGLE = pi / 4

# Size and Weight Constants
TOTAL_MASS = 80  # Made up units
TOTAL_HEIGHT = 300  # Pygame pixels
STARTING_X_POSITION = 300
STARTING_Y_POSITION = 150
SEGMENT_WIDTH = 5


def create_torso():
    """
    Creates a pymunk body and shape to represent the torso
    :returns torso body, torso shape
    """
    mass = TOTAL_MASS * TORSO_WEIGHT_FRACTION
    length = TOTAL_HEIGHT * TORSO_HEIGHT_FRACTION
    inertia = pymunk.moment_for_segment(mass, (0, length / 2), (0, -length / 2))
    torso_body = pymunk.Body(mass, inertia)
    torso_body.position = STARTING_X_POSITION, TOTAL_HEIGHT * HIP_STARTING_HEIGHT_FRACTION + length / 2 + STARTING_Y_POSITION
    torso_shape = pymunk.Segment(torso_body, (0, length / 2), (0, -length / 2), SEGMENT_WIDTH)
    torso_shape.collision_type = BODY_COLLISION_TYPE
    return torso_body, torso_shape


def create_thigh(torso_body, torso_shape):
    """
    Creates the  thigh given a torso and returns its body, shape, and any constraints
    :param torso_body pymunk body for the torso this will be attached to
    :param torso_shape pymunk shape for the torso
    :return: body, shape, pivot, rotary limit, motor
    """
    mass = TOTAL_MASS * THIGH_WEIGHT_FRACTION
    length = TOTAL_HEIGHT * THIGH_HEIGHT_FRACTION
    inertia = pymunk.moment_for_segment(mass, (0, length / 2), (0, -length / 2))

    thigh_body = pymunk.Body(mass, inertia)
    thigh_body.position = STARTING_X_POSITION, TOTAL_HEIGHT * KNEE_STARTING_HEIGHT_FRACTION + length / 2 + STARTING_Y_POSITION

    thigh_shape = pymunk.Segment(thigh_body, (0, length / 2), (0, -length / 2), SEGMENT_WIDTH)
    thigh_shape.collision_type = BODY_COLLISION_TYPE

    pivot = pymunk.PivotJoint(torso_body, thigh_body, torso_shape.b, (0, length / 2))
    rotary_limit = pymunk.RotaryLimitJoint(torso_body, thigh_body, HIP_MIN_ANGLE, HIP_MAX_ANGLE)

    return thigh_body, thigh_shape, pivot, rotary_limit


def create_leg(thigh_body, thigh_shape):
    """
    Creates a lower leg attached to the given thigh
    :param thigh_body: pymunk body of thigh
    :param thigh_shape: pymunk shape of thigh
    :return: body, shape, pivot, rotary limit, motor
    """
    mass = TOTAL_MASS * LEG_WEIGHT_FRACTION
    length = TOTAL_HEIGHT * LEG_HEIGHT_FRACTION
    inertia = pymunk.moment_for_segment(mass, (0, length / 2), (0, -length / 2))

    leg_body = pymunk.Body(mass, inertia)
    leg_body.position = STARTING_X_POSITION + 1, length / 2 + STARTING_Y_POSITION

    leg_shape = pymunk.Segment(leg_body, (0, length / 2), (0, -length / 2), SEGMENT_WIDTH)
    leg_shape.collision_type = BODY_COLLISION_TYPE

    pivot = pymunk.PivotJoint(thigh_body, leg_body, thigh_shape.b, (0, length / 2))
    rotary_limit = pymunk.RotaryLimitJoint(thigh_body, leg_body, KNEE_MIN_ANGLE, KNEE_MAX_ANGLE)

    return leg_body, leg_shape, pivot, rotary_limit


class HumanBody:
    def __init__(self):
        self.torso_body, self.torso_shape = create_torso()
        self.left_thigh_body, self.left_thigh_shape, self.left_hip_pivot, self.left_thigh_rotary_limit = create_thigh(
            self.torso_body, self.torso_shape)
        self.left_leg_body, self.left_leg_shape, self.left_knee_pivot, self.left_knee_rotary_limit = create_leg(
            self.left_thigh_body, self.left_thigh_shape)

    def draw(self, screen):
        """
        Draws all bodies using the supplied pygame screen
        :param screen: pygame screen
        """
        pymunk.pygame_util.draw(screen, self.torso_shape, self.left_thigh_shape, self.left_leg_shape)

    def add_to_space(self, space):
        """
        Adds all relevant bodies, shapes, and constraints to the given pymunk space
        :param space: pymunk space
        :return: nothing
        """
        space.add(self.torso_shape, self.torso_body)
        space.add(self.left_thigh_body, self.left_thigh_shape, self.left_hip_pivot, self.left_thigh_rotary_limit)
        space.add(self.left_leg_body, self.left_leg_shape, self.left_knee_pivot, self.left_knee_rotary_limit)
