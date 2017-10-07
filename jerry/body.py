import math
from collections import namedtuple

from jerry.body_config import joints
from jerry.body_config import segments
from jerry.joint import Joint
from jerry.segment import Segment

# tuple to store current body angle to report to rest of simulation
BodyState = namedtuple('BodyState', 'torso_angle \
                                    torso_rate \
                                    left_shoulder_angle \
                                    left_elbow_angle \
                                    right_shoulder_angle \
                                    right_elbow_angle \
                                    left_hip_angle \
                                    left_knee_angle \
                                    left_ankle_angle \
                                    right_hip_angle \
                                    right_knee_angle \
                                    right_ankle_angle')

# tuple to send a set of joint commands, each torque command should be between -1 and 1
BodyCommand = namedtuple('BodyCommand', 'left_shoulder_torque \
                                        left_elbow_torque \
                                        right_shoulder_torque \
                                        right_elbow_torque \
                                        left_hip_torque \
                                        left_knee_torque \
                                        left_ankle_torque \
                                        right_hip_torque \
                                        right_knee_torque \
                                        right_ankle_torque')

JointAngles = namedtuple('JointAngles', 'neck \
                                        left_shoulder \
                                        left_elbow \
                                        right_shoulder \
                                        right_elbow \
                                        torso \
                                        left_hip \
                                        left_knee \
                                        left_ankle \
                                        right_hip \
                                        right_knee \
                                        right_ankle \
                                        x_position \
                                        y_position')


# todo figure out more extensible way to set rates
class Body:
    def __init__(self, joint_angles):
        # Torso
        torso_position = (joint_angles.x_position, joint_angles.y_position)
        self.torso = Segment(segments["torso"], torso_position, angle=joint_angles.torso)
        self.initial_height = self.torso.body.position[1]

        # Head
        self.head, self.neck = self.create_segment(self.torso,
                                                   segments["head"],
                                                   joints["neck"],
                                                   joint_angles.neck,
                                                   attach_to_end=False)

        # Left arm
        self.left_upper_arm, self.left_shoulder = self.create_segment(self.torso,
                                                                      segments["upper_arm"],
                                                                      joints["shoulder"],
                                                                      joint_angles.left_shoulder,
                                                                      attach_to_end=False)
        self.left_forearm, self.left_elbow = self.create_segment(self.left_upper_arm,
                                                                 segments["forearm"],
                                                                 joints["elbow"],
                                                                 joint_angles.left_elbow)

        # Right arm
        self.right_upper_arm, self.right_shoulder = self.create_segment(self.torso,
                                                                        segments["upper_arm"],
                                                                        joints["shoulder"],
                                                                        joint_angles.right_shoulder,
                                                                        attach_to_end=False)

        self.right_forearm, self.right_elbow = self.create_segment(self.right_upper_arm,
                                                                   segments["forearm"],
                                                                   joints["elbow"],
                                                                   joint_angles.right_elbow)

        # Left leg
        self.left_thigh, self.left_hip = self.create_segment(self.torso,
                                                             segments["thigh"],
                                                             joints["hip"],
                                                             joint_angles.left_hip)
        self.left_calf, self.left_knee = self.create_segment(self.left_thigh,
                                                             segments["calf"],
                                                             joints["knee"],
                                                             joint_angles.left_knee)
        self.left_foot, self.left_ankle = self.create_segment(self.left_calf,
                                                              segments["foot"],
                                                              joints["ankle"],
                                                              joint_angles.left_ankle)

        # Right leg
        self.right_thigh, self.right_hip = self.create_segment(self.torso,
                                                               segments["thigh"],
                                                               joints["hip"],
                                                               joint_angles.right_hip)
        self.right_calf, self.right_knee = self.create_segment(self.right_thigh,
                                                               segments["calf"],
                                                               joints["knee"],
                                                               joint_angles.right_knee)
        self.right_foot, self.right_ankle = self.create_segment(self.right_calf,
                                                                segments["foot"],
                                                                joints["ankle"],
                                                                joint_angles.right_ankle)

    def create_segment(self, base_segment, segment_info, joint_info, starting_angle, attach_to_end=True):
        """
        Creates a new body segment attached to the given segment.
        :param base_segment: Pre-existing Segment to which the new segment will be attached
        :param segment_info: A SegmentInfo object that describes how the new Segment should be created
        :param joint_info: A JointInfo object that describes the joint
        :param starting_angle: Joint starting angle in radians
        :param attach_to_end: If True, the new segment will be attached to the end of the base. If False, it will be
        attached to the start
        :return: new_segment, joint
        """
        if attach_to_end:
            connection_point = base_segment.get_end_point()
        else:
            connection_point = base_segment.get_start_point()
        new_segment_angle = base_segment.get_angle() + starting_angle
        new_segment = Segment(segment_info, connection_point, angle=new_segment_angle)
        new_joint = Joint(base_segment, new_segment, joint_info.range, attach_to_end, joint_info.max_torque)
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
                          self.left_elbow.get_angle(),
                          self.right_shoulder.get_angle(),
                          self.right_elbow.get_angle(),
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

        self.left_shoulder.set_torque(command.left_shoulder_torque)
        self.left_elbow.set_torque(command.left_elbow_torque)
        self.right_shoulder.set_torque(command.right_shoulder_torque)
        self.right_elbow.set_torque(command.right_elbow_torque)
        self.left_hip.set_torque(command.left_hip_torque)
        self.left_knee.set_torque(command.left_knee_torque)
        self.left_ankle.set_torque(command.left_ankle_torque)
        self.right_hip.set_torque(command.right_hip_torque)
        self.right_knee.set_torque(command.right_knee_torque)
        self.right_ankle.set_torque(command.right_ankle_torque)

    def get_distance(self):
        """
        Returns x position of the torso
        """
        return self.torso.body.position[0]

    def get_angle(self):
        return self.torso.get_angle()

    def get_height(self):
        return self.torso.body.position[1]
