import matplotlib.pyplot as plt
from MewsMatch.utils import load_from_excel, load_from_json
import os

data = load_from_excel(
    "../data/datasets/numeric_cat_dataset.xlsx"
)  ####################
config_data = load_from_json(
    "../config/numeric_dataset_characteristics.json"
)  ##################
data = data.drop(columns=["Row.names", "Horodateur", "Plus"])

os.makedirs(f"../data/plots/all_breed/", exist_ok=True)

for col in data.columns:

    fig, axs = plt.subplots(1, 2, figsize=(12, 5))
    data[col].value_counts().reindex(
        config_data[col]["unique_values"], fill_value=0
    ).plot(kind="bar", ax=axs[0], color="purple", edgecolor="black")
    axs[0].set_title(f"Histogram of {col}")
    axs[0].set_xlabel(col)
    axs[0].set_ylabel("Frequency")
    axs[0].tick_params(axis="x", rotation=0)

    if data[col].dtype in ["int64", "float64"]:
        data[[col]].boxplot(ax=axs[1], vert=False)
        axs[1].set_title(f"Boxplot of {col}")
        axs[1].set_xlabel(col)
    else:
        axs[1].axis("off")

    file_path = f"../data/plots/all_breed/{col}_histogram.png"
    plt.tight_layout()
    plt.savefig(file_path)
    plt.close(fig)

    print(f"Saved {file_path}")

breed_column = "Race"

for breed in data[breed_column].unique():
    breed_data = data[data[breed_column] == breed]

    for col in breed_data.columns:
        if col == breed_column:
            continue

        fig, axs = plt.subplots(1, 2, figsize=(12, 5))
        breed_data[col].value_counts().reindex(
            config_data[col]["unique_values"], fill_value=0
        ).plot(kind="bar", ax=axs[0], color="purple", edgecolor="black")
        axs[0].set_title(f"Histogram of {col} for {breed}")
        axs[0].set_xlabel(col)
        axs[0].set_ylabel("Frequency")
        axs[0].tick_params(axis="x", rotation=0)

        if breed_data[col].dtype in ["int64", "float64"]:
            breed_data[[col]].boxplot(ax=axs[1], vert=False)
            axs[1].set_title(f"Boxplot of {col} for {breed}")
            axs[1].set_xlabel(col)
        else:
            axs[1].axis("off")

        os.makedirs(f"../data/plots/{breed}/", exist_ok=True)
        file_path = f"../data/plots/{breed}/{col}_histogram.png"
        plt.tight_layout()
        plt.savefig(file_path)
        plt.close(fig)

        print(f"Saved {file_path}")
