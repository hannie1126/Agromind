import os
import json
import pandas as pd

# JSON 폴더 경로
folder = "/Users/hannie/Desktop/099.지능형 수직농장 통합 데이터(딸기)/01.데이터/1.Training/라벨링데이터"

rows = []

# 모든 JSON 파일 탐색
for root, dirs, files in os.walk(folder):
    for file in files:
        if file.endswith(".json"):
            path = os.path.join(root, file)

            # JSON 읽기 (오류 발생 시 건너뛰기)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception as e:
                print(f"읽기 실패: {path}")
                print(e)
                continue

            # 데이터 추출
            img = data.get("images", {})
            envs = data.get("envrionments", [])   # JSON 키 확인 (AIHub는 envrionments인 경우가 있음)
            growth = data.get("growth_index", {})

            env = envs[0] if len(envs) > 0 else {}

            rows.append({
                # 이미지 정보
                "image_id": img.get("image_id"),
                "farm_id": img.get("farm_id"),
                "crop": img.get("crops"),
                "kind_type": img.get("kind_type"),
                "growth_stage": img.get("growth_stage"),
                "date_captured": img.get("date_captured"),

                # 객체 검출 결과
                "leaf": img.get("leaf"),
                "plant_body": img.get("plant_body"),

                # 환경 데이터
                "temperature": env.get("ti_value"),
                "humidity": env.get("hi_value"),
                "co2": env.get("ci_value"),
                "light": env.get("ir_value"),
                "soil_temperature": env.get("tl_value"),
                "ec": env.get("ei_value"),
                "ph": env.get("pl_value"),

                # 생육 데이터
                "stem_length": growth.get("stem_length"),
                "leaf_count": growth.get("leaf_cnt"),
                "leaf_width": growth.get("leaf_width"),
                "leaf_length": growth.get("leaf_length"),
                "stem_thickness": growth.get("stem_thick"),
                "fruit_weight": growth.get("fr_weight"),
            })

# DataFrame 생성
df = pd.DataFrame(rows)

# 날짜 형식 변환
df["date_captured"] = pd.to_datetime(df["date_captured"], errors="coerce")

# 숫자형 컬럼
numeric_cols = [
    "leaf",
    "plant_body",
    "temperature",
    "humidity",
    "co2",
    "light",
    "soil_temperature",
    "ec",
    "ph",
    "stem_length",
    "leaf_count",
    "leaf_width",
    "leaf_length",
    "stem_thickness",
    "fruit_weight",
]

# 숫자형 변환
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# 중복 제거
df.drop_duplicates(inplace=True)

# ===========================
# 데이터 확인
# ===========================

print("=" * 60)
print("데이터 크기")
print(df.shape)

print("\n" + "=" * 60)
print("컬럼 목록")
print(df.columns.tolist())

print("\n" + "=" * 60)
print("데이터 타입")
print(df.info())

print("\n" + "=" * 60)
print("앞부분 5개")
print(df.head())

print("\n" + "=" * 60)
print("기초 통계")
print(df.describe())

print("\n" + "=" * 60)
print("생육단계 개수")
print(df["growth_stage"].value_counts(dropna=False))

print("\n" + "=" * 60)
print("결측치 개수")
print(df.isnull().sum())

print("\n" + "=" * 60)
print("결측치 비율(%)")
print((df.isnull().mean() * 100).round(2))

print("\n" + "=" * 60)
print("생육단계별 평균 환경값")
print(
    df.groupby("growth_stage")[
        ["temperature", "humidity", "co2", "light", "soil_temperature"]
    ].mean()
)

print("\n" + "=" * 60)
print("상관계수")
print(df[numeric_cols].corr())

# CSV 저장
output_path = "/Users/hannie/Desktop/이매지니어프로젝트/strawberry_gumsil.csv"
df.to_csv(output_path, index=False, encoding="utf-8-sig")

print("\nCSV 저장 완료!")
print(output_path)