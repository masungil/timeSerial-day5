import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from pmdarima import auto_arima
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.metrics import mean_squared_error

# [1] 데이터 로드 및 전처리 (이전과 동일)
df_energy = pd.read_csv(r'.\data\household_daily_usage.csv', parse_dates=['dt'], index_col='dt')
df_weather = pd.read_csv(r'.\data\paris_weather_data.csv', parse_dates=['time'], index_col='time')

df_weather['temp_est'] = (df_weather['tmin'] + df_weather['tmax']) / 2
df_weather = df_weather[['temp_est', 'tmin', 'tmax', 'prcp']].interpolate().ffill().bfill()
df = df_energy.join(df_weather, how='inner')
df['is_weekend'] = df.index.dayofweek.map(lambda x: 1 if x >= 5 else 0)

# [2] 데이터 분리
# - 공통 테스트셋 구간 (마지막 30일)을 설정하여 두 모델을 공정하게 비교합니다.
y = df['Global_active_power']
X_vars = df[['temp_est', 'tmin', 'tmax', 'prcp', 'is_weekend']]

train_y, test_y = y[:-30], y[-30:]
train_X, test_X = X_vars[:-30], X_vars[-30:]

# --- [3] 모델 1: SARIMAX (통계적 모델) ---
# - 통계적 추론을 기반으로 시계열의 선형적 패턴과 계절성을 잘 포착합니다.
print("Step 1: SARIMAX 학습 및 예측 수행 중...")
sarima_model = auto_arima(train_y, X=train_X, m=7, seasonal=True, stepwise=True)
sarima_pred = sarima_model.predict(n_periods=30, X=test_X)

# --- [4] 모델 2: LSTM (딥러닝 모델) ---
# - 신경망을 통해 데이터의 비선형적인 복잡한 관계를 학습합니다.
print("Step 2: LSTM 학습 및 예측 수행 중...")
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
X_test_lstm = X_seq[-30:]

lstm_model = Sequential([
    LSTM(128, return_sequences=True, input_shape=(seq_length, X_seq.shape[2])),
    Dropout(0.2),
    LSTM(64, return_sequences=False),
    Dense(1)
])
lstm_model.compile(optimizer='adam', loss='mse')
lstm_model.fit(X_train_lstm, y_train_lstm, epochs=50, batch_size=16, verbose=0)

# - LSTM 예측 결과 역스케일링
lstm_raw_pred = lstm_model.predict(X_test_lstm)
dummy = np.zeros((30, 6))
dummy[:, 0] = lstm_raw_pred.flatten()
lstm_pred = scaler.inverse_transform(dummy)[:, 0]

# --- [5] 모델 결합: Weighted Ensemble ---
# - 두 모델의 예측값을 가중 평균하여 최종 예측값을 도출합니다.
# - 여기서는 SARIMAX에 40%, LSTM에 60% 비중을 두어 시너지 효과를 노립니다.
print("Step 3: 두 모델의 예측 결과를 결합하여 최종 앙상블 생성 중...")
ensemble_pred = (sarima_pred.values * 0.4) + (lstm_pred * 0.6)

# [6] 최종 예측 결과 시각화
plt.figure(figsize=(12, 6))
plt.plot(test_y.index, test_y.values, label='Actual (실제)', color='black', alpha=0.3)
plt.plot(test_y.index, sarima_pred, label='SARIMAX Prediction', linestyle='--', alpha=0.6)
plt.plot(test_y.index, lstm_pred, label='LSTM Prediction', linestyle='--', alpha=0.6)
plt.plot(test_y.index, ensemble_pred, label='Ensemble Result (Combined)', color='red', linewidth=2)
plt.title('SARIMAX & LSTM Ensemble Energy Prediction')
plt.legend()
plt.grid(True)
plt.show()

# [7] 성능 지표 평가 (RMSE)
# - 실제값과 예측값의 차이를 수치로 확인하여 어떤 모델이 우수한지 판단합니다. (낮을수록 좋음)
print("\n--- 모델 성능 평가 (RMSE) ---")
sarima_rmse = np.sqrt(mean_squared_error(test_y, sarima_pred))
lstm_rmse = np.sqrt(mean_squared_error(test_y, lstm_pred))
ensemble_rmse = np.sqrt(mean_squared_error(test_y, ensemble_pred))

print(f"1. SARIMAX RMSE : {sarima_rmse:.4f}")
print(f"2. LSTM RMSE    : {lstm_rmse:.4f}")
print(f"3. Ensemble RMSE: {ensemble_rmse:.4f} (최종 모델)")