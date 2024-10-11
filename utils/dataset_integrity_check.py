# TASK I (Modelling)


def usability_of_dataset(data):

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

            # if col == 'Column1' and value not in ['ExpectedValue1', 'ExpectedValue2']:
            #     print(f"Coloana '{col}', Index {index}: '{value}' nu se încadrează în clasificarea așteptată.")

    if can_be_used:
        print("There were no usability problems found")
    else:
        print("Usability problems have been found")
    return can_be_used


def count_of_unique_elements_per_class(data, config_data):
    can_be_used = True
    print("\nCount of unique instances and their value:")
    for col in data.columns:
        if col != "Plus":
            unique_values = data[col].unique()
            count = data[col].nunique()
            print(f"\nColumn '{col}': has {count} unique instaces")
            if col not in ["Row.names", "Horodateur"]:
                print(f"Values: {unique_values.tolist()}")

            if col in config_data:
                expected_count = config_data[col]
                if count > expected_count:
                    can_be_used = False
                    print(
                        f"Alert: '{col}' has more unique values ({count}) than it was expected ({expected_count})."
                    )

    return can_be_used
