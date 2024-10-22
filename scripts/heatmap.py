import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency
from utils.IO_utils import load_from_excel

data = load_from_excel("../data/datasets/numeric_cat_dataset.xlsx")
data = data.drop(["Row.names", "Horodateur", "Plus"], axis=1)

for column in data.columns:
    if data[column].dtype != 'int64' and data[column].dtype != 'float64':
        data[column] = data[column].astype('category')


def cramers_v(confusion_matrix):
    chi2 = chi2_contingency(confusion_matrix)[0]
    n = confusion_matrix.sum().sum()
    r, k = confusion_matrix.shape
    return np.sqrt(chi2 / (n * (min(r, k) - 1)))


def calculate_cramers_v_matrix(data):
    cols = data.columns
    n = len(cols)
    cramers_v_matrix = np.zeros((n, n))

    for i in range(n):
        for j in range(i, n):
            confusion_matrix = pd.crosstab(data[cols[i]], data[cols[j]])

            if not confusion_matrix.empty and confusion_matrix.values.sum() > 0:
                cramers_v_matrix[i, j] = cramers_v(confusion_matrix)
                cramers_v_matrix[j, i] = cramers_v_matrix[i, j]
            else:
                cramers_v_matrix[i, j] = np.nan
                cramers_v_matrix[j, i] = np.nan

    return pd.DataFrame(cramers_v_matrix, index=cols, columns=cols)


cramers_v_matrix = calculate_cramers_v_matrix(data)

plt.figure(figsize=(16, 12))
plt.title("Relations between attributes(Heatmap)")
sns.heatmap(cramers_v_matrix, cmap="coolwarm", annot=True, fmt=".2f", linewidths=0.5, cbar=True, square=True)
plt.show()
