import pandas as pd
from utils.IO_utils import load_from_excel
import json

data = load_from_excel(f"../data/datasets/base_cat_dataset.xlsx")
data = data.drop(["Row.names", "Horodateur", "Plus"], axis=1)

df = pd.DataFrame(data)


def generate_mappings_from_dataset(df):
    result = {}

    for column in df.columns:
        unique_values = df[column].unique().tolist()
        expected_count = len(unique_values)

        result[column] = {
            "expected_count": expected_count,
            "unique_values": unique_values,
            "mappings": {}
        }

    return result


mappings = generate_mappings_from_dataset(df)
print(json.dumps(mappings, indent=4))
