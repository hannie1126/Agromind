import os
import json
import pandas as pd

folder = "/Users/hannie/Desktop/099.지능형 수직농장 통합 데이터(딸기)/01.데이터/1.Training/라벨링데이터"

rows = []

for root, dirs, files in os.walk(folder):
    for file in files:
        if file.endswith(".json"):
            path = os.path.join(root, file)

            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)

            img = data.get("images", {})
            envs = data.get("envrionments", [])
            growth = data.get("growth_index", {})

            env = envs[0] if len(envs) > 0 else {}

            rows.append({
                "image_id": img.get("image_id"),
                "farm_id": img.get("farm_id"),
                "crop": img.get("crops"),
                "kind_type": img.get("kind_type"),
                "growth_stage": img.get("growth_stage"),
                "date_captured": img.get("date_captured"),
                "leaf": img.get("leaf"),
                "plant_body": img.get("plant_body"),

                "temperature": env.get("ti_value"),
                "humidity": env.get("hi_value"),
                "co2": env.get("ci_value"),
                "light": env.get("ir_value"),
                "soil_temp": env.get("tl_value"),
                "ec": env.get("ei_value"),
                "ph": env.get("pl_value"),

                "stem_length": growth.get("stem_length"),
                "leaf_cnt": growth.get("leaf_cnt"),
                "leaf_width": growth.get("leaf_width"),
                "leaf_length": growth.get("leaf_length"),
                "stem_thick": growth.get("stem_thick"),
                "fruit_weight": growth.get("fr_weight"),
            })

df = pd.DataFrame(rows)

numeric_cols = [
    "leaf", "plant_body",
    "temperature", "humidity", "co2", "light", "soil_temp",
    "ec", "ph",
    "stem_length", "leaf_cnt", "leaf_width",
    "leaf_length", "stem_thick", "fruit_weight"
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

print("데이터 크기:", df.shape)
print("\n컬럼 목록:")
print(df.columns)

print("\n생육단계 개수:")
print(df["growth_stage"].value_counts())

print("\n결측치 개수:")
print(df.isnull().sum())

print("\n생육단계별 평균 환경값:")
print(df.groupby("growth_stage")[["temperature", "humidity", "co2", "light", "soil_temp"]].mean())

output_path = "/Users/hannie/Desktop/이매지니어프로젝트/strawberry_gumsil.csv"
df.to_csv(output_path, index=False, encoding="utf-8-sig")

print("\nCSV 저장 완료:", output_path)