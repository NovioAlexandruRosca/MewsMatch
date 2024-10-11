from utils.IO_utils import load_from_excel, load_from_json
from utils.dataset_integrity_check import (
    usability_of_dataset,
    inconsistent_number_of_unique_values,
)


def run_dataset_quality_check(file_path, config_path):

    data = load_from_excel(file_path)
    config_data = load_from_json(config_path)

    print("Inconsistencies:")

    if usability_of_dataset(data, config_data) and inconsistent_number_of_unique_values(
        data, config_data
    ):
        print("\nThe dataset is consistent and ready to be used")
    else:
        print("\nThe dataset is not consistent or usable and needs changes")


run_dataset_quality_check(
    "../data/datasets/base_cat_dataset.xlsx",
    "../config/base_dataset_characteristics.json",
)
