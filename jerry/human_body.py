import math

from jerry.joint import Joint

from jerry import human_body_constants as body
from jerry.human_body_constants import ranges
from jerry.human_body_constants import segments
from jerry.human_body_constants import joints
from jerry.segment import Segment

from collections import namedtuple

# tuple to store current body angle to report to rest of simulation
BodyState = namedtuple('BodyState', 'torso_angle \
                                    torso_rate \
                                    left_shoulder_angle \
                                    right_shoulder_angle \
                                    left_hip_angle \
                                    left_knee_angle \
                                    left_ankle_angle \
                                    right_hip_angle \
                                    right_knee_angle \
                                    right_ankle_angle')

# tuple to send a set of joint commands
BodyCommand = namedtuple('BodyCommand', 'left_shoulder_rate \
                                        right_shoulder_rate \
                                        left_hip_rate \
                                        left_knee_rate \
                                        left_ankle_rate \
                                        right_hip_rate \
                                        right_knee_rate \
                                        right_ankle_rate')


# todo figure out more extensible way to set rates
class HumanBody:
    def __init__(self):
        # Torso
        self.torso = Segment(segments["torso"], body.TORSO_POSITION)
        self.initial_height = self.torso.body.position[1]

        # Head
        self.head = Segment(segments["head"], body.HEAD_POSITION)
        self.neck = Joint(self.head, self.torso, ranges["neck"])

        # Right arm
        self.right_upper_arm, self.right_shoulder = self.create_segment(self.torso,
                                                                        segments["upper_arm"],
                                                                        joints["right_shoulder"],
                                                                        attach_to_end=False)

        self.right_forearm, self.right_elbow = self.create_segment(self.right_upper_arm,
                                                                   segments["forearm"],
                                                                   joints["right_elbow"])

        # Left arm
        self.left_upper_arm, self.left_shoulder = self.create_segment(self.torso,
                                                                      segments["upper_arm"],
                                                                      joints["left_shoulder"],
                                                                      attach_to_end=False)
        self.left_forearm, self.left_elbow = self.create_segment(self.left_upper_arm,
                                                                 segments["forearm"],
                                                                 joints["left_elbow"])

        # Right leg
        self.right_thigh, self.right_hip = self.create_segment(self.torso,
                                                               segments["thigh"],
                                                               joints["right_hip"])
        self.right_calf, self.right_knee = self.create_segment(self.right_thigh,
                                                               segments["calf"],
                                                               joints["right_knee"])
        self.right_foot, self.right_ankle = self.create_segment(self.right_calf,
                                                                segments["foot"],
                                                                joints["right_ankle"])

        # Left leg
        self.left_thigh, self.left_hip = self.create_segment(self.torso,
                                                             segments["thigh"],
                                                             joints["left_hip"])
        self.left_calf, self.left_knee = self.create_segment(self.left_thigh,
                                                             segments["calf"],
                                                             joints['left_knee'])
        self.left_foot, self.left_ankle = self.create_segment(self.left_calf,
                                                              segments["foot"],
                                                              joints["left_ankle"])

    def create_segment(self, base_segment, segment_info, joint_info, attach_to_end=True):
        """
        Creates a new body segment attached to the given segment.
        :param base_segment: Pre-existing Segment to which the new segment will be attached
        :param segment_info: A SegmentInfo object that describes how the new Segment should be created
        :param joint_info: A JointInfo object that describes how the joint should be created
        :param attach_to_end: If True, the new segment will be attached to the end of the base. If False, it will be
        attached to the start
        :return: new_segment, joint
        """
        if attach_to_end:
            connection_point = base_segment.get_end_point()
        else:
            connection_point = base_segment.get_start_point()
        new_segment_angle = base_segment.get_angle() + joint_info.starting_angle
        new_segment = Segment(segment_info, connection_point, angle=new_segment_angle)
        new_joint = Joint(base_segment, new_segment, joint_info.range, attach_to_end)
        return new_segment, new_joint

    def draw(self, screen):
        """
        Draws all bodies using the supplied pygame screen. Must be draw in the correct order to ensure that they overlap
        correctly
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
        Returns a BodyState containing all relevant state info
        :return: BodyState object
        """
        state = BodyState(self.torso.get_angle(),
                          self.torso.get_rate(),
                          self.left_shoulder.get_angle(),
                          self.right_shoulder.get_angle(),
                          self.left_hip.get_angle(),
                          self.left_knee.get_angle(),
                          self.left_ankle.get_angle(),
                          self.right_hip.get_angle(),
                          self.right_knee.get_angle(),
                          self.right_ankle.get_angle())

        return state

    def set_rates(self, command):
        """
        Takes a BodyCommand object and sets the corresponding rates
        """

        self.left_shoulder.set_rate(command.left_shoulder_rate)
        self.right_shoulder.set_rate(command.right_shoulder_rate)
        self.left_hip.set_rate(command.left_hip_rate)
        self.left_knee.set_rate(command.left_knee_rate)
        self.left_ankle.set_rate(command.left_ankle_rate)
        self.right_hip.set_rate(command.right_hip_rate)
        self.right_knee.set_rate(command.right_knee_rate)
        self.right_ankle.set_rate(command.right_ankle_rate)

    def get_distance(self):
        """
        Returns x position of the torso
        """
        return self.torso.body.position[0]

    def get_score_multiplier(self):
        # todo move this to WalkingFitnessCalculator
        """
        Returns a multiplier based on the current torso angle and height, staying vertical and high gives a higher score
        :return: score from 0 to 1
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
            height_score = torso_height / self.initial_height

        return angle_score * height_score
