import pymunk


class Joint:
    def __init__(self, a, b, angular_range, max_force):
        # todo describe which segment is which, and how the joint will connect them
        """
        Creates a new Joint from two Segment objects and constraints
        :param a: Segment object
        :param b: Segment object
        :param angular_range: (min, max) tuple that specifies the allowable angular range in radians
        :param max_force: maximum force in Newtons exerted by this joint
        :return:
        """
        self.pivot = pymunk.PivotJoint(a, b, a.b, b.a)
        self.rotary_limit = pymunk.RotaryLimitJoint(a, b, angular_range[0], angular_range[1])
        self.motor = pymunk.SimpleMotor(a, b, 0)
        self.motor.max_force = max_force

    def add_to_space(self, space):
        """
        Adds all bodies to a pymunk Space
        :param space: pymunk simulation Space
        :return:
        """
        space.add(self.pivot, self.rotary_limit, self.motor)

    def set_speed(self, rate):
        # todo confirm rate units
        """
        Sets the speed of the motor controlling this joint, motor is still subject to max force and rotary limit constraints
        :param rate: desired angular speed in rad/s
        :return:
        """
        self.motor.rate = rate
