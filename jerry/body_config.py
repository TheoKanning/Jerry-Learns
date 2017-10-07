from collections import namedtuple
from math import pi

import pygame

# Size and Weight Constants
TOTAL_MASS = 20  # Made up units
TOTAL_HEIGHT = 350  # Pygame pixels
STARTING_SPEED = 0, 0  # pixels/sec?
BASE_STRENGTH = 1500000

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

# Joint Constraints #
joint_ranges = {
    "neck": (3 * pi / 4, 5 * pi / 4),
    "elbow": (0, 3 * pi / 4),
    "shoulder": (-pi / 2, pi),
    "hip": (-pi / 8, pi / 2),
    "knee": (-3 * pi / 4, 0),
    "ankle": (0, 2 * pi / 3)
}

joint_strengths = {
    "neck": .15 * BASE_STRENGTH,
    "elbow": .3 * BASE_STRENGTH,
    "shoulder": .5 * BASE_STRENGTH,
    "hip": .8 * BASE_STRENGTH,
    "knee": .8 * BASE_STRENGTH,
    "ankle": .4 * BASE_STRENGTH
}

# Collision Types #
collision_types = {
    "upper": 1,
    "lower": 2,
    "ground": 3
}

body_collision_types = {
    "torso": collision_types["upper"],
    "head": collision_types["upper"],
    "upper_arm": collision_types["upper"],
    "forearm": collision_types["upper"],
    "thigh": collision_types["upper"],
    "calf": collision_types["lower"],
    "foot": collision_types["lower"]
}

# Images
images = {
    "torso": pygame.image.load("images/torso.bmp"),
    "head": pygame.image.load("images/head.bmp"),
    "upper_arm": pygame.image.load("images/upper_arm.bmp"),
    "forearm": pygame.image.load("images/forearm.bmp"),
    "thigh": pygame.image.load("images/thigh.bmp"),
    "calf": pygame.image.load("images/leg.bmp"),
    "foot": pygame.image.load("images/foot.bmp")
}

SegmentInfo = namedtuple('SegmentInfo', 'mass length start_speed collision_type image')

segments = {}
# todo I don't like this loop, it assumes that all other dictionaries have the same keys
for key in mass_fractions:
    segments[key] = SegmentInfo(masses[key], lengths[key], STARTING_SPEED, body_collision_types[key], images[key])

JointInfo = namedtuple('JointInfo', 'range max_torque')
joints = {}
for key in joint_ranges:
    joints[key] = JointInfo(joint_ranges[key], joint_strengths[key])
