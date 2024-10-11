from utils.IO_utils import load_from_excel, load_from_json
from utils.dataset_integrity_check import (
    usability_of_dataset,
    count_of_unique_elements_per_class,
)


def run_dataset_quality_check(file_path, config_path):

    data = load_from_excel(file_path)
    config_data = load_from_json(config_path)

    print("Inconsistencies and Statistics:")

    if usability_of_dataset(data) and count_of_unique_elements_per_class(
        data, config_data
    ):
        print("\nThe dataset is consistent and ready to be used")
    else:
        print("\nThe dataset is not consistent or usable and needs changes")


run_dataset_quality_check(
    "../data/datasets/base_cat_dataset.xlsx",
    "../config/number_of_unique_instances_base_dataset.json",
)
