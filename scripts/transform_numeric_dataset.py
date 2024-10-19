import pandas as pd
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "../data/datasets/base_cat_dataset.xlsx")

db = pd.read_excel(file_path)

db["Sexe"] = db["Sexe"].replace({"M": 0, "F": 1, "NSP": -1})
db["Race"] = db["Race"].replace(
    {
        "SBI": 1,
        "EUR": 2,
        "NR": 3,
        "MCO": 4,
        "BEN": 5,
        "SAV": 6,
        "PER": 7,
        "ORI": 8,
        "BRI": 9,
        "CHA": 10,
        "RAG": 11,
        "TUV": 12,
        "SPH": 13,
        "Autre": 14,
        "NSP": -1,
    }
)
db["Age"] = db["Age"].replace({"Moinsde1": 0, "1a2": 1, "2a10": 2, "Plusde10": 10})
db["Nombre"] = db["Nombre"].replace({"Plusde5": 6})
db["Logement"] = db["Logement"].replace({"ASB": 1, "AAB": 2, "ML": 3, "MI": 4})
db["Zone"] = db["Zone"].replace({"U": 1, "R": 2, "PU": 3})
db["Abondance"] = db["Abondance"].replace({"NSP": -1})

new_file_path = os.path.join(script_dir, "../data/datasets/numeric_cat_dataset.xlsx")
db.to_excel(new_file_path, index=False)

print("Dataset updated with numeric values.")
