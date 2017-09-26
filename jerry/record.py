import os
import pickle
from datetime import datetime

record_dir = "records/"
folder_path = os.path.join(record_dir, datetime.today().strftime("%B_%d_%Y_%I_%M%p"))


def save_genome(genome, score, generation):
    """ Pickle the and save it into the run's folder using generation and score as labels
    :param genome: neat-python genome to be stored
    :param score: fitness score
    :param generation: generation number
    """
    filename = "gen_{}_score_{:.0f}.pickle".format(generation, score)
    file_path = os.path.join(folder_path, filename)

    with open(file_path, 'wb') as handle:
        pickle.dump(genome, handle)


def create_folder():
    """ Creates a new folder named after the start time """

    # make record folder if not made already
    if not os.path.exists(record_dir):
        os.mkdir(record_dir)

    # make new folder for this run
    os.mkdir(folder_path)
