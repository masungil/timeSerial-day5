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

# 학습 및 테스트 데이터 불러오기
X_train, y_train = load_har_data(path, 'train')
X_test, y_test = load_har_data(path, 'test')

# 라벨 이름 로드 (1: Walking, 2: Walking_Upstairs, ...)
labels = ["Walking", "Walking_Up", "Walking_Down", "Sitting", "Standing", "Laying"]

# 2. 모델 학습 (Training)
# 모델 생성 (결정 트리 100개를 사용하는 랜덤 포레스트)
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)

# 학습 시작
print("모델 학습 중...")
rf_model.fit(X_train, y_train.values.ravel())
print("학습 완료!")

# 3. 추론 및 성능 평가 (Inference & Evaluation)
# 추론 (Inference)
y_pred = rf_model.predict(X_test)

# 성능 리포트 출력
print(f"전체 정확도: {accuracy_score(y_test, y_pred):.4f}")
print("\n[행동별 분류 성능]")
print(classification_report(y_test, y_pred, target_names=labels))

# 4. 모델 저장하기
model_save_path = './model/har_model.pkl'
joblib.dump(rf_model, model_save_path)
print(f"모델이 {model_save_path}에 저장되었습니다.")

