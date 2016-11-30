from math import pi
import pygame

WALKING_START = True

# Size and Weight Constants
TOTAL_MASS = 80  # Made up units
TOTAL_HEIGHT = 350  # Pygame pixels
STARTING_X_POSITION = 100
STARTING_Y_POSITION = 5
STARTING_SPEED = 0, 0  # pixels/sec?

# Mass Fractions #
mass_fractions = {
    "head": 0.0826,
    "torso": 0.551,
    "upper_arm": 0.0325,
    "forearm": 0.0187 + 0.0065,  # Including hand
    "thigh": 0.105,
    "calf": 0.0475,
    "foot": 0.0143
}

# Segment Masses
masses = {}
for segment in mass_fractions:
    masses[segment] = mass_fractions[segment] * TOTAL_MASS

# Height Fractions #
height_fractions = {
    "head": 0.2,  # Larger for cartoon, anatomically correct is 0.1075
    "torso": 0.3,
    "upper_arm": 0.172,
    "forearm": 0.157 + 0.057,  # Including hand
    "thigh": 0.25,  # standard is .232
    "calf": 0.23,  # standard is .247
    "foot": 0.1  # Counts foot length, not height
}

# Segment Lengths
lengths = {}
for segment in height_fractions:
    lengths[segment] = height_fractions[segment] * TOTAL_HEIGHT

# Starting Height Fractions #
# todo all of these height calculation assume a completely vertical start. They should be calculated dynamically or
# removed
SHOULDER_STARTING_HEIGHT_FRACTION = height_fractions["calf"] + height_fractions["thigh"] + height_fractions["torso"]
HIP_STARTING_HEIGHT_FRACTION = height_fractions["calf"] + height_fractions["thigh"]

# Starting Positions
HEAD_POSITION = STARTING_X_POSITION, TOTAL_HEIGHT * SHOULDER_STARTING_HEIGHT_FRACTION + lengths[
    "head"] + STARTING_Y_POSITION  # subtract to prevent weird head bounce at start
TORSO_POSITION = STARTING_X_POSITION, TOTAL_HEIGHT * HIP_STARTING_HEIGHT_FRACTION + lengths[
    "torso"] + STARTING_Y_POSITION

# Joint Constraints #
ranges = {
    "neck": (0, 0),
    "elbow": (0, 3 * pi / 4),
    "shoulder": (-pi / 2, pi),
    "hip": (-pi / 8, pi / 3),
    "knee": (-2 * pi / 3, 0),
    "ankle": (0, 2 * pi / 3)
}

# Joint Starting Angles #
# todo make a dictionary for these
if WALKING_START:
    NECK_STARTING_ANGLE = 0
    LEFT_SHOULDER_STARTING_ANGLE = - pi / 4
    LEFT_ELBOW_STARTING_ANGLE = pi / 4
    RIGHT_SHOULDER_STARTING_ANGLE = pi / 4
    RIGHT_ELBOW_STARTING_ANGLE = pi / 4
    LEFT_HIP_STARTING_ANGLE = pi / 6
    LEFT_KNEE_STARTING_ANGLE = - pi / 16
    LEFT_ANKLE_STARTING_ANGLE = pi / 2
    RIGHT_HIP_STARTING_ANGLE = -pi / 12
    RIGHT_KNEE_STARTING_ANGLE = 0
    RIGHT_ANKLE_STARTING_ANGLE = pi / 2
else:
    NECK_STARTING_ANGLE = 0
    LEFT_SHOULDER_STARTING_ANGLE = 0
    LEFT_ELBOW_STARTING_ANGLE = 0
    RIGHT_SHOULDER_STARTING_ANGLE = 0
    RIGHT_ELBOW_STARTING_ANGLE = 0
    LEFT_HIP_STARTING_ANGLE = - pi / 128  # just enough hip angle to fall forward
    LEFT_KNEE_STARTING_ANGLE = 0
    LEFT_ANKLE_STARTING_ANGLE = pi / 2
    RIGHT_HIP_STARTING_ANGLE = -pi / 128
    RIGHT_KNEE_STARTING_ANGLE = 0
    RIGHT_ANKLE_STARTING_ANGLE = pi / 2

# Collision Types #
# todo make dictionary for these
UPPER_COLLISION_TYPE = 1
GROUND_COLLISION_TYPE = 2
LOWER_COLLISION_TYPE = 3

collision_types = {
    "torso": UPPER_COLLISION_TYPE,
    "head": UPPER_COLLISION_TYPE,
    "upper_arm": UPPER_COLLISION_TYPE,
    "forearm": UPPER_COLLISION_TYPE,
    "thigh": UPPER_COLLISION_TYPE,
    "calf": LOWER_COLLISION_TYPE,
    "foot": LOWER_COLLISION_TYPE
}

# Images
images = {
    "torso": pygame.image.load("jerry/torso.bmp"),
    "head": pygame.image.load("jerry/head.bmp"),
    "upper_arm": pygame.image.load("jerry/upper_arm.bmp"),
    "forearm": pygame.image.load("jerry/forearm.bmp"),
    "thigh": pygame.image.load("jerry/thigh.bmp"),
    "calf": pygame.image.load("jerry/leg.bmp"),
    "foot": pygame.image.load("jerry/foot.bmp")
}


class SegmentInfo:
    """
    All starting info for a body segment
    """

    def __init__(self, mass, length, image, collision_type):
        self.mass = mass
        self.length = length
        self.image = image
        self.collision_type = collision_type
        self.start_speed = STARTING_SPEED


segments = {}
for key in mass_fractions:
    segments[key] = SegmentInfo(masses[key], lengths[key], images[key], collision_types[key])
