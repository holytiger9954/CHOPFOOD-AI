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
# 경로 설정
# ==============================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(BASE_DIR, "data", "work_train_data.csv")
MODEL_DIR = os.path.join(BASE_DIR, "models")
MODEL_PATH = os.path.join(MODEL_DIR, "work_model.pkl")

os.makedirs(MODEL_DIR, exist_ok=True)


# ==============================
# CSV 로드
# ==============================
df = pd.read_csv(DATA_PATH)
df.columns = [col.upper() for col in df.columns]

print("===== WORK 데이터 확인 =====")
print("데이터 수:", len(df))
print("컬럼:", df.columns.tolist())
print()


# ==============================
# 타깃 설정
# ==============================
TARGET = "RISK_LEVEL"

if TARGET not in df.columns:
    raise ValueError(f"{TARGET} 컬럼이 없습니다. CSV 컬럼명을 확인하세요.")

print("===== 라벨 분포 =====")
print(df[TARGET].value_counts())
print()


# ==============================
# 답지성 컬럼 제거
# ==============================
drop_cols = [
    "WORK_ID",
    "WORK_DATE",
    "WORK_FDATE",
    "PLAN_ID",
    "WORK_WORKER",
    "WORK_DIRECTOR",

    # 결과값/정답 힌트
    "DELAY_DAYS"
]

drop_cols = [col for col in drop_cols if col in df.columns]

y = df[TARGET]
X = df.drop(columns=[TARGET] + drop_cols, errors="ignore")


# ==============================
# 결측치 처리
# ==============================
for col in X.columns:
    if X[col].dtype == "object":
        X[col] = X[col].fillna("NONE")
    else:
        X[col] = X[col].fillna(0)


# ==============================
# 컬럼 타입 분리
# ==============================
cat_cols = X.select_dtypes(include=["object", "string"]).columns.tolist()
num_cols = X.select_dtypes(exclude=["object", "string"]).columns.tolist()

print("===== 학습 Feature =====")
print("범주형:", cat_cols)
print("숫자형:", num_cols)
print()


# ==============================
# 전처리 + 모델
# ==============================
preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
        ("num", "passthrough", num_cols)
    ]
)

model = RandomForestClassifier(
    n_estimators=300,
    max_depth=14,
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
# 학습 / 검증 데이터 분리
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
print("정확도:", round(accuracy_score(y_test, pred), 4))
print()
print(classification_report(y_test, pred))


# ==============================
# 모델 저장
# ==============================
joblib.dump(pipeline, MODEL_PATH)

print()
print("===== 저장 완료 =====")
print(MODEL_PATH)