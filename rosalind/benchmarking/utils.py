import os

def build_results_dir():
    base_results_dir = os.path.join(os.path.dirname(__file__), "results")

    if not os.path.isdir(base_results_dir):
        os.mkdir(base_results_dir)

    return base_results_dir