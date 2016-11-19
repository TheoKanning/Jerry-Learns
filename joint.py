import math
import pymunk


class Joint:
    def __init__(self, a, b, angular_range, segment_a_end=True, max_force=None):
        # todo describe which segment is which, and how the joint will connect them
        """
        Creates a new Joint from two Segment objects and constraints
        :param a: Segment object
        :param b: Segment object
        :param angular_range: (min, max) tuple that specifies the allowable angular range in radians
        :param segment_a_end: whether the start of b should be connected to the end of a, connects to start of a if False
        :param max_force: maximum force exerted by this joint
        :return:
        """
        self.body_a = a.body
        self.body_b = b.body

        if segment_a_end:
            segment_a_position = a.shape.b
        else:
            segment_a_position = a.shape.a

        self.pivot = pymunk.PivotJoint(self.body_a, self.body_b, segment_a_position, b.shape.a)
        self.rotary_limit = pymunk.RotaryLimitJoint(self.body_a, self.body_b, angular_range[0], angular_range[1])
        self.rotary_limit.max_force = 1000000 # finite limit prevents bouncing
        self.motor = pymunk.SimpleMotor(self.body_a, self.body_b, 0)
        if max_force is not None:
            self.motor.max_force = max_force
        else:
            self.motor.max_force = 1000000  # High enough to be strong but won't break rotary limit constraints

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
        return self.body_a.angular_velocity - self.body_b.angular_velocity

    def get_angle(self):
        """
        Returns the angular difference between this joint's two bodies, adds pi because the second joint is technically
        upside down when they overlap
        :return: difference in radians
        """
        return self.body_a.angle - self.body_b.angle + math.pi
