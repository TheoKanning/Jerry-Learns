class FitnessCalculator:
    def update(self, body):
        """
        Update internal fitness calculations using the given body object
        :param body: simulated body
        """
        pass

    def get_fitness(self):
        """
        :return: current best fitness
        """


class WalkingFitnessCalculator(FitnessCalculator):
    # todo subtract starting x position
    def __init__(self):
        self.max_distance = 0
        self.scaled_distance = 0

    def update(self, body):
        distance = body.get_distance()
        multiplier = body.get_score_multiplier()
        if distance > self.max_distance:
            # multiply new distance by current score multiplier
            self.scaled_distance += multiplier * (distance - self.max_distance)
            self.max_distance = distance

    def get_fitness(self):
        return self.scaled_distance
