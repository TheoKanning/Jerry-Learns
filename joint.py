import pymunk


class Joint:
    def __init__(self, a, b, angular_range, max_force=None):
        # todo describe which segment is which, and how the joint will connect them
        """
        Creates a new Joint from two Segment objects and constraints
        :param a: Segment object
        :param b: Segment object
        :param angular_range: (min, max) tuple that specifies the allowable angular range in radians
        :param max_force: maximum force exerted by this joint
        :return:
        """
        self.body_a = a.body
        self.body_b = b.body
        self.pivot = pymunk.PivotJoint(self.body_a, self.body_b, a.shape.b, b.shape.a)
        self.rotary_limit = pymunk.RotaryLimitJoint(self.body_a, self.body_b, angular_range[0], angular_range[1])
        self.motor = pymunk.SimpleMotor(self.body_a, self.body_b, 0)
        if max_force is not None:
            self.motor.max_force = max_force

    def add_to_space(self, space):
        """
        Adds all bodies to a pymunk Space
        :param space: pymunk simulation Space
        :return:
        """
        space.add(self.pivot, self.rotary_limit, self.motor)

    def set_rate(self, rate):
        # todo confirm rate units
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
        Returns the angular difference between this joint's two bodies
        :return: difference in radians
        """
        print self.body_a.angle, self.body_b.angle
        return self.body_b.angle - self.body_a.angle
