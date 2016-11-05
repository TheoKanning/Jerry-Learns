import human_body_constants as body
from joint import Joint
from segment import Segment


class HumanBody:
    def __init__(self):
        self.torso = Segment(body.TORSO_MASS, body.TORSO_LENGTH, body.TORSO_POSITION, image=body.TORSO_IMAGE)
        left_thigh_angle = self.torso.angle() + body.LEFT_HIP_STARTING_ANGLE
        self.left_thigh = Segment(body.THIGH_MASS, body.THIGH_LENGTH, self.torso.get_end_point(),
                                  angle=left_thigh_angle, image=body.THIGH_IMAGE)
        left_leg_angle = self.left_thigh.angle() + body.LEFT_KNEE_STARTING_ANGLE
        self.left_leg = Segment(body.LEG_MASS, body.LEG_LENGTH, self.left_thigh.get_end_point(), angle=left_leg_angle,
                                image=body.LEG_IMAGE)
        left_foot_angle = self.left_leg.angle() + body.LEFT_ANKLE_STARTING_ANGLE
        self.left_foot = Segment(body.FOOT_MASS, body.FOOT_LENGTH, self.left_leg.get_end_point(), angle=left_foot_angle,
                                 image=body.FOOT_IMAGE)

        self.left_hip = Joint(self.torso, self.left_thigh, (body.HIP_MIN_ANGLE, body.HIP_MAX_ANGLE), 100)
        self.left_knee = Joint(self.left_thigh, self.left_leg, (body.KNEE_MIN_ANGLE, body.KNEE_MAX_ANGLE), 100)
        self.left_ankle = Joint(self.left_leg, self.left_foot, (body.ANKLE_MIN_ANGLE, body.ANKLE_MAX_ANGLE), 100)

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
