import pygame

PROGRESS_TIMEOUT = 5000  # end if no progress is made for this many
FALL_SIM_TIME = 1000  # number of milliseconds to simulate after a fall


class RunTerminator:
    """
    Class that maintains the active state of the current run. Determines when simulation should be stopped
    """

    def __init__(self):
        self.fall_time = None
        self.last_progress_time = pygame.time.get_ticks()
        self.last_distance = 0

    def update(self, body):
        """
        Checks if body is still moving forward, run will terminate if no progress is made for duration of
        PROGRESS_TIMEOUT
        """
        if body.get_distance() > self.last_distance:
            self.last_distance = body.get_distance()
            self.last_progress_time = pygame.time.get_ticks()

    def fall(self):
        """
        Called to signal that Jerry has fallen, only count first fall time.
        """
        if self.fall_time is None:
            self.fall_time = pygame.time.get_ticks()

    def has_fallen(self):
        return self.fall_time is not None

    def run_complete(self):
        """
        Returns true if the current run should be stopped
        """
        current_time = pygame.time.get_ticks()

        if self.has_fallen() and current_time - self.fall_time > FALL_SIM_TIME:
            return True
        elif current_time - self.last_progress_time > PROGRESS_TIMEOUT:
            return True
        else:
            return False
