import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report


# ==============================
# 경로
# ==============================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(BASE_DIR, "data", "io_train_data.csv")
MODEL_DIR = os.path.join(BASE_DIR, "models")
MODEL_PATH = os.path.join(MODEL_DIR, "io_model.pkl")

os.makedirs(MODEL_DIR, exist_ok=True)


# ==============================
# CSV
# ==============================
df = pd.read_csv(DATA_PATH)

df.columns = [col.upper() for col in df.columns]

print("===== IO 데이터 확인 =====")
print("데이터 수:", len(df))
print("컬럼:", df.columns.tolist())
print()


TARGET = "RISK_LEVEL"

print("===== 라벨 분포 =====")
print(df[TARGET].value_counts())
print()


# ==============================
# 제거 컬럼
# ==============================
drop_cols = [
    "IO_ID",
    "LOT_ID",
    "IO_REASON",
    "RESERVE_RATE",
    "STOCK_RESERVE_QTY",
    "IO_TYPE",
    "STOCK_PREV_QTY",
    "STOCK_AVAIL_QTY",

    # 정답 힌트
    "REMAIN_DAYS"
]

drop_cols = [c for c in drop_cols if c in df.columns]

y = df[TARGET]
X = df.drop(columns=[TARGET] + drop_cols, errors="ignore")


# ==============================
# 결측치
# ==============================
for col in X.columns:
    if X[col].dtype == "object":
        X[col] = X[col].fillna("NONE")
    else:
        X[col] = X[col].fillna(0)


# ==============================
# 컬럼 분리
# ==============================
cat_cols = X.select_dtypes(
    include=["object", "string"]
).columns.tolist()

num_cols = X.select_dtypes(
    exclude=["object", "string"]
).columns.tolist()

print("===== 학습 Feature =====")
print("범주형:", cat_cols)
print("숫자형:", num_cols)
print()


# ==============================
# 전처리
# ==============================
preprocessor = ColumnTransformer(
    transformers=[
        (
            "cat",
            OneHotEncoder(handle_unknown="ignore"),
            cat_cols
        ),
        (
            "num",
            "passthrough",
            num_cols
        )
    ]
)

model = RandomForestClassifier(
    n_estimators=300,
    max_depth=12,
    min_samples_leaf=2,
    random_state=42,
    class_weight="balanced"
)

pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", model)
    ]
)


# ==============================
# 분할
# ==============================
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# ==============================
# 학습
# ==============================
pipeline.fit(X_train, y_train)

pred = pipeline.predict(X_test)

print("===== 학습 결과 =====")
print(
    "정확도:",
    round(
        accuracy_score(
            y_test,
            pred
        ),
        4
    )
)

print()

print(
    classification_report(
        y_test,
        pred
    )
)


# ==============================
# 저장
# ==============================
joblib.dump(
    pipeline,
    MODEL_PATH
)

print()
print("===== 저장 완료 =====")
print(MODEL_PATH)