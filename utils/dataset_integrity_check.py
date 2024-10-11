# TASK I (Modelling)


def usability_of_dataset(data, config_data):

    can_be_used = True

    missing_values = data.isnull().sum()
    duplicates = data.duplicated()

    if missing_values.any():
        for column, count in missing_values.items():
            if count > 0 and column != "Plus":  # ONLY the Plus column can have no value
                can_be_used = False
                print(f"Column '{column}': Has {count} missing values")

    if duplicates.any():
        can_be_used = False
        print("\nDuplicated rows found:")
        print(data[duplicates])

    for col in data.columns:
        for index, value in data[col].items():
            if (
                isinstance(value, str) and len(value.split()) > 1 and col != "Plus"
            ):  # ONLY the Plus column can have more words in a cell
                can_be_used = False
                print(
                    f"Column '{col}', Index {index}: '{value}' contains unwanted added data!"
                )

            if col in config_data:
                expected_values = config_data[col]["unique_values"]
                if value not in expected_values:
                    print(
                        f"Column '{col}', Index {index}: '{value}' shouldn't be part of this dataset."
                    )

    return can_be_used


def inconsistent_number_of_unique_values(data, config_data):
    can_be_used = True
    for col in data.columns:
        if col != "Plus":

            count = data[col].nunique()

            if col in config_data:
                expected_count = config_data[col]["expected_count"]
                if count > expected_count:
                    can_be_used = False
                    print(
                        f"Alert: '{col}' has more unique values ({count}) than it was expected ({expected_count})."
                    )

    return can_be_used
