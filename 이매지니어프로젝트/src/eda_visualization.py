import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

# CSV 불러오기
BASE_DIR = Path(__file__).resolve().parent.parent
csv_path = BASE_DIR / "data" / "strawberry.csv"

df = pd.read_csv(csv_path)

# 그래프 스타일
sns.set_theme(style="whitegrid")
plt.rcParams["figure.figsize"] = (8, 5)

plt.figure()

sns.countplot(
    data=df,
    x="growth_stage",
    order=df["growth_stage"].value_counts().index
)

plt.title("Growth Stage Distribution")
plt.xlabel("Growth Stage")
plt.ylabel("Count")

plt.tight_layout()
plt.show()

plt.figure()

sns.countplot(
    data=df,
    x="kind_type",
    order=df["kind_type"].value_counts().index
)

plt.title("Strawberry Variety")
plt.xlabel("Variety")
plt.ylabel("Count")

plt.xticks(rotation=30)

plt.tight_layout()
plt.show()

plt.figure()

sns.histplot(
    df["temperature"],
    bins=30,
    kde=True
)

plt.title("Temperature Distribution")

plt.tight_layout()
plt.show()

plt.figure()

sns.histplot(
    df["humidity"],
    bins=30,
    kde=True
)

plt.title("Humidity Distribution")

plt.tight_layout()
plt.show()

plt.figure()

sns.histplot(
    df["co2"],
    bins=30,
    kde=True
)

plt.title("CO2 Distribution")

plt.tight_layout()
plt.show()

numeric_df = df.select_dtypes(include="number")

plt.figure(figsize=(12, 8))

sns.heatmap(
    numeric_df.corr(),
    annot=True,
    cmap="coolwarm",
    fmt=".2f"
)

plt.title("Correlation Heatmap")

plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 6))

sns.boxplot(
    data=df[
        [
            "temperature",
            "humidity",
            "co2",
            "light",
            "soil_temp",
            "ec",
            "ph",
        ]
    ]
)

plt.xticks(rotation=20)

plt.title("Boxplot of Environmental Variables")

plt.tight_layout()
plt.show()