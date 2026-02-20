import os
# TensorFlow의 oneDNN 최적화 관련 로그 메시지를 억제합니다. (0: 모두 표시, 1: INFO 억제, 2: WARNING 억제, 3: ERROR 억제)
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import pandas as pd
import numpy as np
import koreanize_matplotlib # 한글 폰트 설정을 위한 라이브러리입니다. matplotlib에서 한글이 깨지는 문제를 해결해줍니다.
import matplotlib.pyplot as plt
import FinanceDataReader as fdr
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import joblib # 학습 시 사용한 전처리 도구(스케일러)를 저장하기 위한 라이브러리

# 1. 데이터 수집 및 저장
# 삼성전자(종목코드: 005930)의 2018년 1월 1일부터 현재까지의 주가 데이터를 가져옵니다.
df = fdr.DataReader('005930', '2018-01-01')
# 수집한 데이터를 CSV 파일로 저장하여 추후 분석이나 재학습에 활용합니다.
df.to_csv('./data/price.csv')

# 2. 데이터 전처리
# LSTM 모델은 데이터의 범위에 민감하므로 0과 1 사이의 값으로 정규화(Normalization)합니다.
scaler = MinMaxScaler(feature_range=(0, 1))
# 'Close'(종가) 컬럼을 추출하여 2차원 배열 형태로 변환 후 스케일링을 적용합니다.
scaled_data = scaler.fit_transform(df['Close'].values.reshape(-1, 1))

# 예측 단계에서 정규화된 값을 다시 실제 가격으로 복원하기 위해 스케일러 객체를 저장합니다.
joblib.dump(scaler, './model/stock_scaler.pkl')

# 3. 학습 데이터 생성
# window_size: 모델이 예측을 위해 참고할 과거 데이터의 일수 (여기서는 60일치 데이터를 보고 다음 날을 예측)
window_size = 60
X, y = [], []

# 전체 데이터에서 60일씩 슬라이딩하며 학습 데이터(X)와 정답 데이터(y)를 생성합니다.
for i in range(window_size, len(scaled_data)):
    # X: i번째 날 이전의 60일치 주가 데이터
    X.append(scaled_data[i-window_size:i, 0])
    # y: i번째 날의 주가 데이터 (예측 목표)
    y.append(scaled_data[i, 0])

# 리스트를 numpy 배열로 변환합니다.
X, y = np.array(X), np.array(y)
# LSTM 입력을 위해 데이터를 3차원 형태로 변환합니다: (샘플 수, 타임스텝, 특성 수)
X = np.reshape(X, (X.shape[0], X.shape[1], 1))

# 데이터를 학습용(80%)과 테스트용(20%)으로 분리합니다.
train_size = int(len(X) * 0.8)
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

# 4. LSTM 모델 구축 및 학습
model = Sequential([
    # 첫 번째 LSTM 레이어: 50개의 유닛, return_sequences=True는 다음 LSTM 레이어로 시퀀스를 전달함을 의미
    LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], 1)),
    # 과적합 방지를 위해 20%의 뉴런을 무작위로 비활성화합니다.
    Dropout(0.2),
    # 두 번째 LSTM 레이어: 마지막 단계의 출력값만 전달
    LSTM(units=50, return_sequences=False),
    Dropout(0.2),
    # 최종 예측값을 위한 Dense 레이어 (주가 1개를 예측하므로 유닛은 1)
    Dense(units=1)
])

# 모델 설정: 최적화 도구로 'adam'을, 손실 함수로 '평균제곱오차(MSE)'를 사용합니다.
model.compile(optimizer='adam', loss='mean_squared_error')
# 모델 학습: 20번 반복(epochs)하며, 32개씩 묶어서(batch_size) 가중치를 업데이트합니다.
model.fit(X_train, y_train, epochs=20, batch_size=32)

# --- [추가] 모델 저장 ---
# 학습된 모델의 구조와 가중치를 H5 형식의 파일로 저장합니다.
model.save('./model/samsung_model.h5')
print("모델과 스케일러가 저장되었습니다.")

# 5. 미래 주가 예측 (예: 향후 5일)
future_days = 5
# 모델의 입력으로 사용할 가장 최근 60일치 데이터를 가져옵니다.
last_60_days = scaled_data[-window_size:]
# 모델 예측을 위해 (1, 60, 1) 형태로 차원을 확장합니다.
current_batch = last_60_days.reshape((1, window_size, 1))

future_predictions = []

for i in range(future_days):
    # 현재 배치 데이터를 바탕으로 다음 날 주가를 예측합니다.
    current_pred = model.predict(current_batch)[0]
    future_predictions.append(current_pred)

    # 예측한 값을 다음 예측의 입력 데이터로 포함시키는 Sliding Window 방식을 적용합니다.
    # [1:, :, :]을 통해 가장 오래된 데이터를 제외하고 방금 예측한 값을 끝에 추가합니다.
    current_pred_reshaped = current_pred.reshape(1, 1, 1)
    current_batch = np.append(current_batch[:, 1:, :], current_pred_reshaped, axis=1)

# 0~1로 정규화되었던 예측값을 실제 주가 단위(원)로 복원합니다.
future_predictions = scaler.inverse_transform(future_predictions)

print(f"\n향후 {future_days}일간의 예상 주가:")
for i, price in enumerate(future_predictions, 1):
    print(f"{i}일 후: {int(price[0])}원")
