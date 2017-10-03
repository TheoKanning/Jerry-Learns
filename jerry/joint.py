import math
import pymunk


class Joint:
    def __init__(self, base_segment, branch_segment, angular_range, attach_to_end=True, max_force=None):
        """
        Creates a new Joint from two Segment objects and constraints
        :param base_segment: Segment object
        :param branch_segment: Segment object
        :param angular_range: (min, max) tuple that specifies the allowable angular range in radians
        :param attach_to_end: whether the start of b should be connected to the end of a, connects to start of a if False
        :param max_force: maximum force exerted by this joint
        :return:
        """
        self.base_body = base_segment.body
        self.branch_body = branch_segment.body

        if attach_to_end:
            segment_a_position = base_segment.shape.b
        else:
            segment_a_position = base_segment.shape.a

        self.pivot = pymunk.PivotJoint(self.base_body, self.branch_body, segment_a_position, branch_segment.shape.a)
        self.rotary_limit = pymunk.RotaryLimitJoint(self.base_body, self.branch_body, angular_range[0], angular_range[1])
        self.rotary_limit.max_force = 5000000  # finite limit prevents bouncing, double the max motor force
        self.motor = pymunk.SimpleMotor(self.base_body, self.branch_body, 0)
        if max_force is not None:
            self.motor.max_force = max_force
        else:
            self.motor.max_force = 2000000  # High enough to be strong but won't break rotary limit constraints

    def add_to_space(self, space):
        """
        Adds all bodies to a pymunk Space
        :param space: pymunk simulation Space
        :return:
        """
        space.add(self.pivot, self.rotary_limit, self.motor)

    def set_rate(self, rate):
        """
        Sets the speed of the motor controlling this joint, motor is still subject to max force and rotary limit constraints
        :param rate: desired angular speed in rad/s
        :return:
        """
        self.motor.rate = rate

    def get_rate(self):
        """
        Returns the angular rate of change of this joint, defined as the angular velocity of body a minus that of body b
        :return: the rate at which this joint's angle is changing, in radians/second
        """
        return self.base_body.angular_velocity - self.branch_body.angular_velocity

    def get_angle(self):
        """
        Returns the angular difference between this joint's two bodies, adds pi because the second joint is technically
        upside down when they overlap
        :return: difference in radians
        """
        return self.base_body.angle - self.branch_body.angle + math.pi
