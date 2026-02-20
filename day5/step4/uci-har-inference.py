import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib

# 1. 데이터 로드 함수 정의
def load_har_data(path, group):
    # 특징값(X) 로드: 561개의 센서 데이터 특징
    X = pd.read_csv(f'{path}/{group}/X_{group}.txt', sep='\\s+', header=None)
    
    # 결과값(y) 로드: 1~6 사이의 행동 라벨
    y = pd.read_csv(f'{path}/{group}/y_{group}.txt', sep='\\s+', header=None)
    
    return X, y

# 데이터 경로 (UCI HAR Dataset 폴더가 있는 위치)
path = './data/dataset/UCI HAR Dataset'
model_save_path = './model/har_model.pkl'

# 테스트 데이터 불러오기
X_test, y_test = load_har_data(path, 'test')

# 라벨 이름 로드 (1: Walking, 2: Walking_Upstairs, ...)
labels = ["Walking", "Walking_Up", "Walking_Down", "Sitting", "Standing", "Laying"]

# 2. 모델 불러오기
loaded_model = joblib.load(model_save_path)

# 3. 추론 및 성능 평가 (Inference & Evaluation)
# 추론 (Inference)
y_pred = loaded_model.predict(X_test)
print("저장된 모델로 추론에 성공했습니다.")

# 성능 리포트 출력
print(f"전체 정확도: {accuracy_score(y_test, y_pred):.4f}")
print("\n[행동별 분류 성능]")
print(classification_report(y_test, y_pred, target_names=labels))


#4. 실전 추론 예시 (Single Sample Inference)
# 테스트 데이터셋에서 임의의 샘플 하나 추출
sample_idx = 200
sample_data = X_test.iloc[sample_idx].values.reshape(1, -1)
actual_label = labels[y_test.iloc[sample_idx, 0] - 1]

# 모델 추론
prediction = loaded_model.predict(sample_data)
predicted_label = labels[prediction[0] - 1]

print(f"--- 단일 데이터 추론 결과 ---")
print(f"실제 행동: {actual_label}")
print(f"모델 예측: {predicted_label}")
