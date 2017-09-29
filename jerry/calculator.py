class MotionCalculator:
    """
    Class that can take a set of body states and generate a set of commands. Usage will be specific to simulation type
    """

    def calculate(self, body_state):
        """
        Calculates the desired body commands based on the given state
        :param body_state: BodyState containing current joint data
        :return: BodyCommand containing desired joint data
        """
        pass

