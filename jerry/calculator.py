from jerry import human_body


class MotionCalculator:
    """
    Class that can take a set of body states and generate a set of commands. Usage will be specific to simulation type
    """

    def calculate(self, body_state):
        pass


class NeatWalkingMotionCalculator(MotionCalculator):
    # If more Neat calculators are added, create a super class to handle converting between tuples and Neat arrays
    def __init__(self, network):
        """
        :param network: NEAT network
        """
        super()
        self.network = network

    def calculate(self, body_state):
        """
        Calculate commands from current state
        :param body_state: BodyState object
        :return: BodyCommand object
        """
        outputs = self.scale_outputs(self.network.activate(body_state))
        command = human_body.BodyCommand(*outputs)
        return command

    def scale_outputs(self, outputs):
        """
        Scale neural network outputs between -3 and 3
        :param outputs: array of outputs of neural network, scaled from -1 to 1 from tanh activation
        :return: scaled outputs that can be used to set body rate
        """
        return [3 * x for x in outputs]
