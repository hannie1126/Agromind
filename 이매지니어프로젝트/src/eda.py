from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
csv_path = BASE_DIR / "data" / "strawberry.csv"

df = pd.read_csv(csv_path)

print("=" * 60)
print("데이터 기본 정보")
print("=" * 60)

print(df.info())

print("\n데이터 크기")
print(df.shape)

print("\n기술통계")
print(df.describe())

print("\n결측치 개수")
print(df.isnull().sum())

print("\n결측치 비율(%)")
print((df.isnull().sum() / len(df) * 100).round(2))

print("\n생육단계 분포")
print(df["growth_stage"].value_counts())

print("\n품종")
print(df["kind_type"].value_counts())

env_cols = [
    "temperature",
    "humidity",
    "co2",
    "light",
    "soil_temp",
    "ec",
    "ph"
]

print("\n환경 변수 평균")
print(df[env_cols].mean())

print("\n중복 데이터 개수")
print(df.duplicated().sum())