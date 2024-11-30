from utils.IO_utils import load_from_excel
import pandas as pd


def count_instances_for_race(data):
    if "Race" in data.columns:
        race_counts = data["Race"].value_counts()
        print("\nCounts for each instance of race:")
        print(race_counts)


def attribute_statistics(data):
    print("\nCount of unique instances and their value:")
    for col in data.columns:
        if col != "Plus":

            unique_values = data[col].unique()
            count = data[col].nunique()

            value_counts = data[col].value_counts()

            print(f"\nColumn '{col}':\n1.Unique Values: {count}")
            if col not in ["Row.names", "Horodateur"]:
                print(f"2.Values: {unique_values.tolist()}")
                print(f"3.Total count over the entire dataset:\n {value_counts}")
                print(
                    f"4.Frequency over the entire dataset:\n {value_counts / data.shape[0]}"
                )

                if col != "Race":
                    class_frequencies = data.groupby("Race")[col].value_counts()
                    print(f"5.Total count over class':\n {class_frequencies}")
                    print(
                        f"6.Frequency over class':\n {class_frequencies/ data.groupby('Race')[col].size()}"
                    )


def race_correlations(data):
    data_correlation = data.drop(columns=["Plus", "Horodateur", "Nombre", "Row.names"])
    print("\nCorrelation between each race and its attributes:")
    for race in data_correlation["Race"].unique():
        race_data = data_correlation[data_correlation["Race"] == race]
        if not race_data.empty:
            correlation = race_data.corr()
            print(f"\nCorrelations for each race {race}:")
            print(correlation)


def average_by_race(data):
    data_correlation = data.drop(columns=["Plus", "Horodateur", "Nombre", "Row.names"])
    mean_values = data_correlation.groupby("Race").mean()
    print("\nAverage for each race:")
    print(mean_values.to_string(index=True, header=True))


data = load_from_excel("../data/datasets/numeric_cat_dataset.xlsx")
# data = load_from_excel("../data/datasets/base_cat_dataset.xlsx")
count_instances_for_race(data)
attribute_statistics(data)
race_correlations(data)
average_by_race(data)
