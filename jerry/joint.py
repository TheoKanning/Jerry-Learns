import math
import pymunk

ROTARY_JOINT_MAX_TORQUE = 5000000  # The maximum torque that can be exerted to keep the joint within range
MOTOR_MAX_TORQUE = 1500000  # The maximum torque that the muscles of this joint, lower than rotary joint max force
MAX_SPEED = 20  # rad/s


class Joint:
    def __init__(self, base_segment, branch_segment, angular_range, attach_to_end=True, max_torque=MOTOR_MAX_TORQUE):
        """
        Creates a new Joint from two Segment objects and constraints
        :param base_segment: Segment object
        :param branch_segment: Segment object
        :param angular_range: (min, max) tuple that specifies the allowable angular range in radians
        :param attach_to_end: whether the start of b should be connected to the end of a, connects to start of a if False
        :param max_torque: maximum torwue exerted by the muscles of this joint
        :return:
        """
        self.base_body = base_segment.body
        self.branch_body = branch_segment.body

        if attach_to_end:
            segment_a_position = base_segment.shape.b
        else:
            segment_a_position = base_segment.shape.a

        self.pivot = pymunk.PivotJoint(self.base_body, self.branch_body, segment_a_position, branch_segment.shape.a)
        self.rotary_limit = pymunk.RotaryLimitJoint(self.base_body, self.branch_body, *angular_range)
        self.rotary_limit.max_force = ROTARY_JOINT_MAX_TORQUE
        self.motor = pymunk.SimpleMotor(self.base_body, self.branch_body, 0)
        self.motor.max_force = max_torque
        self.max_torque = max_torque

    def add_to_space(self, space):
        """
        Adds all bodies to a pymunk Space
        :param space: pymunk simulation Space
        :return:
        """
        space.add(self.pivot, self.rotary_limit, self.motor)

    def set_rate(self, rate):
        """
        Sets the speed of the motor controlling this joint, motor is still subject to max torque and rotary limit
        :param rate: desired angular speed in rad/s
        """
        self.motor.rate = rate
        self.motor.max_force = self.max_torque

    def set_torque(self, torque):
        """
        Sets the torque of this joint's motor. Torque can be between [-1, 1], and will be scaled to the maximum torque
        this joint can provide
        :param torque: Fraction of maximum torque to provide, between -1 and 1
        """
        clamped_torque = max(-1, min(1, torque))
        self.motor.max_force = abs(clamped_torque) * self.max_torque
        self.motor.rate = MAX_SPEED * (1 if torque > 0 else -1)

    def get_rate(self):
        """
        Returns the angular rate of change of this joint, defined as the angular velocity of body a minus that of body b
        :return: the rate at which this joint's angle is changing, in radians/second
        """
        return (self.base_body.angular_velocity - self.branch_body.angular_velocity) / 10  # hack to reduce weight in NN

    def get_angle(self):
        """
        Returns the angular difference between this joint's two bodies, adds pi because the second joint is technically
        upside down when they overlap
        :return: difference in radians
        """
        return self.base_body.angle - self.branch_body.angle + math.pi
