import os
from datetime import datetime

folder_name = None
record_dir = "records/"

def save_best_genome():
    """ Pickle the best genome from the last generation and save it into the run's folder """


def create_folder():
    """ Creates a new folder named after the start time """

    # make record folder if not made already
    if not os.path.exists(record_dir):
        os.mkdir(record_dir)

    global folder_name
    folder_name = os.path.join(record_dir, datetime.today().strftime("%B_%d_%Y_%I_%M%p"))

    # make new folder for this run
    os.mkdir(folder_name)
