import math

import human_body_constants as body
from joint import Joint
from segment import Segment


class HumanBody:
    def __init__(self):

        # Torso
        self.torso = Segment(body.TORSO_MASS, body.TORSO_LENGTH, body.TORSO_POSITION, image=body.TORSO_IMAGE)

        # Head
        self.head = Segment(body.HEAD_MASS, body.HEAD_LENGTH, body.HEAD_POSITION, image=body.HEAD_IMAGE)
        self.neck = Joint(self.head, self.torso, body.NECK_ANGLES)

        # Right arm
        self.right_upper_arm = Segment(body.UPPER_ARM_MASS, body.UPPER_ARM_LENGTH, self.torso.get_start_point(),
                                       angle=body.RIGHT_SHOULDER_STARTING_ANGLE,
                                       image=body.UPPER_ARM_IMAGE)

        right_elbow_angle = self.right_upper_arm.angle() + body.RIGHT_ELBOW_STARTING_ANGLE
        self.right_forearm = Segment(body.FOREARM_MASS, body.FOREARM_LENGTH, self.right_upper_arm.get_end_point(),
                                     angle=right_elbow_angle, image=body.FOREARM_IMAGE)

        self.right_shoulder = Joint(self.torso, self.right_upper_arm, body.SHOULDER_ANGLES, segment_a_end=False)
        self.right_elbow = Joint(self.right_upper_arm, self.right_forearm, body.ELBOW_ANGLES)

        # Left arm
        self.left_upper_arm = Segment(body.UPPER_ARM_MASS, body.UPPER_ARM_LENGTH, self.torso.get_start_point(),
                                      angle=body.LEFT_SHOULDER_STARTING_ANGLE,
                                      image=body.UPPER_ARM_IMAGE)

        left_elbow_angle = self.left_upper_arm.angle() + body.LEFT_ELBOW_STARTING_ANGLE
        self.left_forearm = Segment(body.FOREARM_MASS, body.FOREARM_LENGTH, self.left_upper_arm.get_end_point(),
                                    angle=left_elbow_angle, image=body.FOREARM_IMAGE)

        self.left_shoulder = Joint(self.torso, self.left_upper_arm, body.SHOULDER_ANGLES, segment_a_end=False)
        self.left_elbow = Joint(self.left_upper_arm, self.left_forearm, body.ELBOW_ANGLES)

        # Left leg
        left_thigh_angle = self.torso.angle() + body.LEFT_HIP_STARTING_ANGLE
        self.left_thigh = Segment(body.THIGH_MASS, body.THIGH_LENGTH, self.torso.get_end_point(),
                                  angle=left_thigh_angle,
                                  image=body.THIGH_IMAGE)

        left_leg_angle = self.left_thigh.angle() + body.LEFT_KNEE_STARTING_ANGLE
        self.left_leg = Segment(body.LEG_MASS, body.LEG_LENGTH, self.left_thigh.get_end_point(),
                                angle=left_leg_angle,
                                image=body.LEG_IMAGE)

        left_foot_angle = self.left_leg.angle() + body.LEFT_ANKLE_STARTING_ANGLE
        self.left_foot = Segment(body.FOOT_MASS, body.FOOT_LENGTH, self.left_leg.get_end_point(),
                                 angle=left_foot_angle,
                                 image=body.FOOT_IMAGE)
        self.left_hip = Joint(self.torso, self.left_thigh, body.HIP_ANGLES)
        self.left_knee = Joint(self.left_thigh, self.left_leg, body.KNEE_ANGLES)
        self.left_ankle = Joint(self.left_leg, self.left_foot, body.ANKLE_ANGLES)

        # Right leg
        right_thigh_angle = self.torso.angle() + body.RIGHT_HIP_STARTING_ANGLE
        self.right_thigh = Segment(body.THIGH_MASS, body.THIGH_LENGTH, self.torso.get_end_point(),
                                   angle=right_thigh_angle,
                                   image=body.THIGH_IMAGE)

        right_leg_angle = self.right_thigh.angle() + body.RIGHT_KNEE_STARTING_ANGLE
        self.right_leg = Segment(body.LEG_MASS, body.LEG_LENGTH, self.right_thigh.get_end_point(),
                                 angle=right_leg_angle,
                                 image=body.LEG_IMAGE)

        right_foot_angle = self.right_leg.angle() + body.RIGHT_ANKLE_STARTING_ANGLE
        self.right_foot = Segment(body.FOOT_MASS, body.FOOT_LENGTH, self.right_leg.get_end_point(),
                                  angle=right_foot_angle,
                                  image=body.FOOT_IMAGE)

        self.right_hip = Joint(self.torso, self.right_thigh, body.HIP_ANGLES)
        self.right_knee = Joint(self.right_thigh, self.right_leg, body.KNEE_ANGLES)
        self.right_ankle = Joint(self.right_leg, self.right_foot, body.ANKLE_ANGLES)

        self.count = 0

    def draw(self, screen):
        """
        Draws all bodies using the supplied pygame screen
        :param screen: pygame screen
        """

        speed = math.sin(self.count / 10.0) * 1
        self.right_hip.set_rate(speed)
        self.left_hip.set_rate(speed)
        self.count += 1
        # print speed, self.left_hip.get_rate()
        print self.right_hip.get_rate()
        # self.left_hip.get_angle()

        # Left arm
        self.left_upper_arm.draw(screen)
        self.left_forearm.draw(screen)

        # Left leg
        self.left_leg.draw(screen)
        self.left_foot.draw(screen)
        self.left_thigh.draw(screen)

        # Right Leg
        self.right_leg.draw(screen)
        self.right_foot.draw(screen)
        self.right_thigh.draw(screen)

        # Torso
        self.torso.draw(screen)

        # Head
        self.head.draw(screen)

        # Right arm
        self.right_upper_arm.draw(screen)
        self.right_forearm.draw(screen)

    def add_to_space(self, space):
        """
        Adds all relevant bodies, shapes, and constraints to the given pymunk space
        :param space: pymunk space
        :return: nothing
        """

        self.right_upper_arm.add_to_space(space)
        self.right_shoulder.add_to_space(space)
        self.right_forearm.add_to_space(space)
        self.right_elbow.add_to_space(space)

        self.left_upper_arm.add_to_space(space)
        self.left_shoulder.add_to_space(space)
        self.left_forearm.add_to_space(space)
        self.left_elbow.add_to_space(space)

        self.torso.add_to_space(space)
        self.head.add_to_space(space)
        self.neck.add_to_space(space)

        self.left_thigh.add_to_space(space)
        self.left_leg.add_to_space(space)
        self.left_foot.add_to_space(space)

        self.left_hip.add_to_space(space)
        self.left_knee.add_to_space(space)
        self.left_ankle.add_to_space(space)

        self.right_thigh.add_to_space(space)
        self.right_leg.add_to_space(space)
        self.right_foot.add_to_space(space)

        self.right_hip.add_to_space(space)
        self.right_knee.add_to_space(space)
        self.right_ankle.add_to_space(space)
