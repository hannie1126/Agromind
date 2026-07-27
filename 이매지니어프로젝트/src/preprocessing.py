from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
csv_path = BASE_DIR / "data" / "strawberry.csv"

df = pd.read_csv(csv_path)

print("원본 데이터 크기:", df.shape)

print("=" * 50)
print("결측치 개수")
print("=" * 50)

print(df.isnull().sum())

print("\n결측치 비율 (%)")

missing = (df.isnull().sum() / len(df) * 100).round(2)
print(missing)

numeric_cols = [
    "temperature",
    "humidity",
    "co2",
    "light",
    "soil_temp",
    "ec",
    "ph"
]

df[numeric_cols] = df[numeric_cols].fillna(
    df[numeric_cols].mean()
)

categorical_cols = [
    "growth_stage",
    "kind_type"
]

for col in categorical_cols:
    df[col] = df[col].fillna(df[col].mode()[0])

print("\n처리 후 결측치")

print(df.isnull().sum())

before = len(df)

df = df.drop_duplicates()

after = len(df)

print(f"\n중복 제거: {before-after}개")

Q1 = df[numeric_cols].quantile(0.25)
Q3 = df[numeric_cols].quantile(0.75)

IQR = Q3 - Q1

outlier = (
    (df[numeric_cols] < (Q1 - 1.5 * IQR))
    | (df[numeric_cols] > (Q3 + 1.5 * IQR))
)

print(outlier.sum())

from sklearn.preprocessing import LabelEncoder

encoder_stage = LabelEncoder()
encoder_kind = LabelEncoder()

df["growth_stage"] = encoder_stage.fit_transform(df["growth_stage"])

df["kind_type"] = encoder_kind.fit_transform(df["kind_type"])

save_path = BASE_DIR / "data" / "strawberry_preprocessed.csv"

df.to_csv(save_path, index=False)

print("저장 완료")