import math

import human_body_constants as body
from human_body_constants import ranges
from human_body_constants import segments
from joint import Joint
from segment import Segment


class HumanBody:
    def __init__(self):
        # Torso
        self.torso = Segment(segments["torso"], body.TORSO_POSITION)
        self.initial_height = self.torso.body.position[1]

        # Head
        self.head = Segment(segments["head"], body.HEAD_POSITION)
        self.neck = Joint(self.head, self.torso, ranges["neck"])

        # Right arm
        self.right_upper_arm = Segment(segments["upper_arm"], self.torso.get_start_point(),
                                       angle=body.RIGHT_SHOULDER_STARTING_ANGLE)

        right_elbow_angle = self.right_upper_arm.get_angle() + body.RIGHT_ELBOW_STARTING_ANGLE
        self.right_forearm = Segment(segments["forearm"], self.right_upper_arm.get_end_point(), angle=right_elbow_angle)

        self.right_shoulder = Joint(self.torso, self.right_upper_arm, ranges["shoulder"], segment_a_end=False)
        self.right_elbow = Joint(self.right_upper_arm, self.right_forearm, ranges["elbow"])

        # Left arm
        self.left_upper_arm = Segment(segments["upper_arm"], self.torso.get_start_point(),
                                      angle=body.LEFT_SHOULDER_STARTING_ANGLE, )

        left_elbow_angle = self.left_upper_arm.get_angle() + body.LEFT_ELBOW_STARTING_ANGLE
        self.left_forearm = Segment(segments["forearm"], self.left_upper_arm.get_end_point(), angle=left_elbow_angle)

        self.left_shoulder = Joint(self.torso, self.left_upper_arm, ranges["shoulder"], segment_a_end=False)
        self.left_elbow = Joint(self.left_upper_arm, self.left_forearm, ranges["elbow"])

        # Left leg
        left_thigh_angle = self.torso.get_angle() + body.LEFT_HIP_STARTING_ANGLE
        self.left_thigh = Segment(segments["thigh"], self.torso.get_end_point(), angle=left_thigh_angle, )

        left_calf_angle = self.left_thigh.get_angle() + body.LEFT_KNEE_STARTING_ANGLE
        self.left_calf = Segment(segments["calf"], self.left_thigh.get_end_point(), angle=left_calf_angle)

        left_foot_angle = self.left_calf.get_angle() + body.LEFT_ANKLE_STARTING_ANGLE
        self.left_foot = Segment(segments["foot"], self.left_calf.get_end_point(), angle=left_foot_angle)

        self.left_hip = Joint(self.torso, self.left_thigh, ranges["hip"])
        self.left_knee = Joint(self.left_thigh, self.left_calf, ranges["knee"])
        self.left_ankle = Joint(self.left_calf, self.left_foot, ranges["ankle"])

        # Right leg
        right_thigh_angle = self.torso.get_angle() + body.RIGHT_HIP_STARTING_ANGLE
        self.right_thigh = Segment(segments["thigh"], self.torso.get_end_point(), angle=right_thigh_angle)

        right_calf_angle = self.right_thigh.get_angle() + body.RIGHT_KNEE_STARTING_ANGLE
        self.right_calf = Segment(segments["calf"], self.right_thigh.get_end_point(), angle=right_calf_angle)

        right_foot_angle = self.right_calf.get_angle() + body.RIGHT_ANKLE_STARTING_ANGLE
        self.right_foot = Segment(segments["foot"], self.right_calf.get_end_point(), angle=right_foot_angle)

        self.right_hip = Joint(self.torso, self.right_thigh, ranges["hip"])
        self.right_knee = Joint(self.right_thigh, self.right_calf, ranges["knee"])
        self.right_ankle = Joint(self.right_calf, self.right_foot, ranges["ankle"])

    def draw(self, screen):
        """
        Draws all bodies using the supplied pygame screen
        :param screen: pygame screen
        """

        # Left arm
        self.left_upper_arm.draw(screen)
        self.left_forearm.draw(screen)

        # Left leg
        self.left_calf.draw(screen)
        self.left_foot.draw(screen)
        self.left_thigh.draw(screen)

        # Right Leg
        self.right_calf.draw(screen)
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
        self.left_calf.add_to_space(space)
        self.left_foot.add_to_space(space)

        self.left_hip.add_to_space(space)
        self.left_knee.add_to_space(space)
        self.left_ankle.add_to_space(space)

        self.right_thigh.add_to_space(space)
        self.right_calf.add_to_space(space)
        self.right_foot.add_to_space(space)

        self.right_hip.add_to_space(space)
        self.right_knee.add_to_space(space)
        self.right_ankle.add_to_space(space)

    def get_state(self):
        """
        Returns an array of all body states
        :return:
        """
        state = [self.torso.get_angle(),
                 # self.torso.get_rate(),
                 self.left_shoulder.get_angle(),
                 # self.left_shoulder.get_rate(),
                 self.left_elbow.get_angle(),
                 # self.left_elbow.get_rate(),
                 self.right_shoulder.get_angle(),
                 # self.right_shoulder.get_rate(),
                 self.right_elbow.get_angle(),
                 # self.right_elbow.get_rate(),
                 self.left_hip.get_angle(),
                 # self.left_hip.get_rate(),
                 self.left_knee.get_angle(),
                 # self.left_knee.get_rate(),
                 self.left_ankle.get_angle(),
                 # self.left_ankle.get_rate(),
                 self.right_hip.get_angle(),
                 # self.right_hip.get_rate(),
                 self.right_knee.get_angle(),
                 # self.right_knee.get_rate(),
                 self.right_ankle.get_angle(),
                 # self.right_ankle.get_rate()
        ]

        return state

    def set_rates(self, rates):
        """
        Takes an array of length 10 and sets the joint rates
        :param rates: array of length 10 containing rates from -1 to 1
        """

        if len(rates) is not 10:
            print "Rate array is not length 10"
            return

        self.left_shoulder.set_rate(rates[0])
        self.left_elbow.set_rate(rates[1])
        self.right_shoulder.set_rate(rates[2])
        self.right_elbow.set_rate(rates[3])
        self.left_hip.set_rate(rates[4])
        self.left_knee.set_rate(rates[5])
        self.left_ankle.set_rate(rates[6])
        self.right_hip.set_rate(rates[7])
        self.right_knee.set_rate(rates[8])
        self.right_ankle.set_rate(rates[9])

    def get_distance(self):
        """
        Returns x position of the torso
        """
        return self.torso.body.position[0]

    def get_angle_score(self):
        """
        Returns a multiplier based on the current torso angle and height, staying vertical and high gives a higher angle
        :return: fraction from 0 to 1
        """
        angle = abs(self.torso.get_angle())
        if angle > math.pi / 6:  # 30 degrees
            return 0
        else:
            angle_score = math.cos(3 * angle)  # smoothly interpolate between 1 at 0 degrees and 0 at 30 degrees

        torso_height = self.torso.body.position[1]
        if torso_height > self.initial_height:
            height_score = 1
        else:
            height_score = torso_height/self.initial_height

        return angle_score*height_score
