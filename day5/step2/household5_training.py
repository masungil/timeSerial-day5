import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from pmdarima import auto_arima
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import joblib
import os

# [1] 데이터 로드 및 전처리 (이전과 동일)
df_energy = pd.read_csv(r'.\data\household_daily_usage.csv', parse_dates=['dt'], index_col='dt')
df_weather = pd.read_csv(r'.\data\paris_weather_data.csv', parse_dates=['time'], index_col='time')

df_weather['temp_est'] = (df_weather['tmin'] + df_weather['tmax']) / 2
df_weather = df_weather[['temp_est', 'tmin', 'tmax', 'prcp']].interpolate().ffill().bfill()
df = df_energy.join(df_weather, how='inner')
df['is_weekend'] = df.index.dayofweek.map(lambda x: 1 if x >= 5 else 0)

# [2] 학습/테스트 데이터 분리
y = df['Global_active_power']
X_vars = df[['temp_est', 'tmin', 'tmax', 'prcp', 'is_weekend']]
train_y, test_y = y[:-30], y[-30:]
train_X, test_X = X_vars[:-30], X_vars[-30:]

# --- [3] 모델 1: SARIMAX 학습 ---
print("SARIMAX 모델을 학습 중입니다...")
sarima_model = auto_arima(train_y, X=train_X, m=7, seasonal=True, stepwise=True)

# --- [4] 모델 2: LSTM 학습 ---
print("LSTM 신경망 모델을 학습 중입니다...")
scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(df[['Global_active_power', 'temp_est', 'tmin', 'tmax', 'prcp', 'is_weekend']])

def create_sequences(data, seq_length):
    X, target = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i:i+seq_length, :])
        target.append(data[i+seq_length, 0])
    return np.array(X), np.array(target)

seq_length = 7
X_seq, y_seq = create_sequences(scaled_data, seq_length)
X_train_lstm = X_seq[:-30]
y_train_lstm = y_seq[:-30]

lstm_model = Sequential([
    LSTM(128, return_sequences=True, input_shape=(seq_length, X_seq.shape[2])),
    Dropout(0.2),
    LSTM(64, return_sequences=False),
    Dense(1)
])
lstm_model.compile(optimizer='adam', loss='mse')
lstm_model.fit(X_train_lstm, y_train_lstm, epochs=50, batch_size=16, verbose=0)

# [5] 모델 및 스케일러 저장 (Persistence)
# - 학습된 결과물을 파일로 저장하여, 나중에 다시 학습할 필요 없이 바로 예측(Inference)에 활용합니다.
if not os.path.exists('./model'):
    os.makedirs('./model')

print("\n--- 모델 저장 프로세스 시작 ---")

# 1. SARIMAX 모델 저장
# - joblib을 사용하여 통계 모델 객체를 .pkl 파일로 직렬화합니다.
joblib.dump(sarima_model, './model/sarima_final.pkl')
print("1. SARIMAX 모델 저장 완료: ./model/sarima_final.pkl")

# 2. LSTM 모델 저장
# - Keras의 .h5(HDF5) 포맷을 사용하여 신경망의 가중치와 구조를 한 번에 저장합니다.
lstm_model.save('./model/lstm_final.h5')
print("2. LSTM 모델 저장 완료: ./model/lstm_final.h5")

# 3. 스케일러(Scaler) 저장 (매우 중요!)
# - 새로운 데이터를 예측할 때도 학습 때와 동일한 '최소/최대' 기준이 필요합니다.
# - 스케일러를 저장하지 않으면 예측 시 데이터 변환의 기준이 달라져 엉뚱한 결과가 나옵니다.
joblib.dump(scaler, './model/scaler.pkl')
print("3. 데이터 스케일러 저장 완료: ./model/scaler.pkl")

print("\n모든 모델 결과물이 성공적으로 저장되었습니다. 이제 Inference 단계를 실행할 수 있습니다.")