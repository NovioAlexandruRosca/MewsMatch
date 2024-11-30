import pandas as pd
import numpy as np
from sklearn.utils import resample
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
from imblearn.combine import SMOTETomek
from sklearn.preprocessing import LabelEncoder


REQUIRED_COLUMNS = [
    "Sexe",
    "Age",
    "Race",
    "Nombre",
    "Logement",
    "Zone",
    "Ext",
    "Obs",
    "Timide",
    "Calme",
    "Effraye",
    "Intelligent",
    "Vigilant",
    "Perseverant",
    "Affectueux",
    "Amical",
    "Solitaire",
    "Brutal",
    "Dominant",
    "Agressif",
    "Impulsif",
    "Previsible",
    "Distrait",
    "Abondance",
    "PredOiseau",
    "PredMamm",
]


def load_and_prepare_data(excel_path, target_column):
    try:
        df = pd.read_excel(excel_path)
        print(f"Successfully loaded {len(df)} rows from Excel file")

        missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Required columns missing from dataset: {missing_cols}")

        df = df[REQUIRED_COLUMNS]
        print(f"\nKept only the {len(REQUIRED_COLUMNS)} required columns")

        print("\nInitial class distribution:")
        print(df[target_column].value_counts())
        print("\nClass distribution percentage:")
        print(df[target_column].value_counts(normalize=True) * 100)

        missing_counts = df.isnull().sum()
        if missing_counts.any():
            print("\nWarning: Found missing values:")
            print(missing_counts[missing_counts > 0])
            print("\nRemoving rows with missing values...")
            df = df.dropna()
            print(f"Remaining rows after removing missing values: {len(df)}")

        features = [col for col in REQUIRED_COLUMNS if col != target_column]

        X = df[features].copy()
        categorical_columns = X.select_dtypes(include=["object", "category"]).columns

        if len(categorical_columns) > 0:
            print(
                "\nConverting categorical columns to numeric:",
                categorical_columns.tolist(),
            )
            for col in categorical_columns:
                le = LabelEncoder()
                X[col] = le.fit_transform(X[col].astype(str))
                mapping = dict(zip(le.classes_, le.transform(le.classes_)))
                print(f"\nEncoding for {col}:")
                print(mapping)

        y = df[target_column]
        if y.dtype == "object" or y.dtype.name == "category":
            le = LabelEncoder()
            y = le.fit_transform(y.astype(str))
            print(f"\nEncoded target classes for {target_column}:")
            print(dict(zip(le.classes_, le.transform(le.classes_))))

        return X.values, y, features

    except Exception as e:
        print(f"Error loading data: {str(e)}")
        raise


def save_balanced_data(
    X_balanced, y_balanced, feature_names, target_column, method, output_path=None
):

    df_balanced = pd.DataFrame(X_balanced, columns=feature_names)
    df_balanced[target_column] = y_balanced

    if output_path is None:
        output_path = (
            f'balanced_dataset_{method}_{pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")}'
        )

    excel_path = f"{output_path}.xlsx"
    df_balanced.to_excel(excel_path, index=False)
    print(f"\nSaved balanced dataset to Excel: {excel_path}")

    csv_path = f"{output_path}.csv"
    df_balanced.to_csv(csv_path, index=False)
    print(f"Saved balanced dataset to CSV: {csv_path}")

    return excel_path, csv_path


def balance_dataset(X, y, method="random_undersample", random_state=42):
    print(f"\nApplying {method} balancing technique...")
    original_counts = pd.Series(y).value_counts()
    print("Original class distribution:", dict(original_counts))

    if method == "random_undersample":
        undersample = RandomUnderSampler(random_state=random_state)
        X_balanced, y_balanced = undersample.fit_resample(X, y)

    elif method == "random_oversample":
        majority_class = pd.Series(y).value_counts().index[0]
        minority_class = pd.Series(y).value_counts().index[-1]

        df_majority = pd.DataFrame(X[y == majority_class])
        df_minority = pd.DataFrame(X[y == minority_class])

        df_minority_upsampled = resample(
            df_minority,
            replace=True,
            n_samples=len(df_majority),
            random_state=random_state,
        )

        X_balanced = pd.concat([df_majority, df_minority_upsampled])
        y_balanced = pd.concat(
            [
                pd.Series(y[y == majority_class]),
                pd.Series(minority_class, index=df_minority_upsampled.index),
            ]
        )

    elif method == "smote":
        smote = SMOTE(random_state=random_state)
        X_balanced, y_balanced = smote.fit_resample(X, y)

    elif method == "hybrid":
        smote_tomek = SMOTETomek(random_state=random_state)
        X_balanced, y_balanced = smote_tomek.fit_resample(X, y)

    elif method == "balanced_subsample":
        min_class_size = pd.Series(y).value_counts().min()
        class_indices = {label: np.where(y == label)[0] for label in np.unique(y)}

        balanced_indices = []
        for indices in class_indices.values():
            sampled_indices = np.random.choice(
                indices, size=min_class_size, replace=False
            )
            balanced_indices.extend(sampled_indices)

        X_balanced = X[balanced_indices]
        y_balanced = y[balanced_indices]

    else:
        raise ValueError(f"Unknown method: {method}")

    balanced_counts = pd.Series(y_balanced).value_counts()
    print("Balanced class distribution:", dict(balanced_counts))
    print(f"Total samples after balancing: {len(y_balanced)}")

    return X_balanced, y_balanced


def main():
    excel_path = "../data/datasets/numeric_cat_dataset.xlsx"
    target_column = "Race"
    output_folder = "../data/datasets/balanced_outputs"

    import os

    os.makedirs(output_folder, exist_ok=True)

    try:
        X, y, feature_names = load_and_prepare_data(excel_path, target_column)

        methods = [
            "random_undersample",
            "random_oversample",
            "smote",
            "hybrid",
            "balanced_subsample",
        ]
        saved_files = {}

        for method in methods:
            try:
                print(f"\nApplying {method} method...")
                X_balanced, y_balanced = balance_dataset(X, y, method=method)

                output_path = os.path.join(output_folder, f"balanced_{method}")
                excel_path, csv_path = save_balanced_data(
                    X_balanced,
                    y_balanced,
                    feature_names,
                    target_column,
                    method,
                    output_path,
                )

                saved_files[method] = {
                    "excel": excel_path,
                    "csv": csv_path,
                    "sample_count": len(y_balanced),
                    "class_distribution": pd.Series(y_balanced)
                    .value_counts()
                    .to_dict(),
                }

            except Exception as e:
                print(f"Error applying {method}: {str(e)}")

        print("\nSummary of all balancing methods:")
        for method, info in saved_files.items():
            print(f"\n{method}:")
            print(f"Total samples: {info['sample_count']}")
            print("Class distribution:", info["class_distribution"])
            print(f"Saved to Excel: {info['excel']}")
            print(f"Saved to CSV: {info['csv']}")

    except Exception as e:
        print(f"Error in main execution: {str(e)}")


if __name__ == "__main__":
    main()
