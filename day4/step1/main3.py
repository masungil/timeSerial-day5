import pandas as pd
import numpy as np
import koreanize_matplotlib
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping

plt.rcParams['axes.unicode_minus'] = False    # 마이너스 기호 깨짐 방지

# [단계 1] 데이터 로드 및 시간 변환
df = pd.read_csv('./data/power_usage_dataset_3month.csv')
df['Date'] = pd.to_datetime(df['Date'])

# [단계 2] 특별 처리: 시간 주기성 반영 (Sin/Cos Encoding)
df['hour'] = df['Date'].dt.hour
df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 23)
df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 23)

# 2. 평일/주말 구분 (토=5, 일=6 이면 1, 아니면 0)
#df['is_weekend'] = df['Date'].dt.weekday.map(lambda x: 1 if x >= 5 else 0)
#기존 is_weekend 대신 요일 주기성(Sin/Cos) 적용 예시
df['weekday'] = df['Date'].dt.weekday
df['weekday_sin'] = np.sin(2 * np.pi * df['weekday'] / 6)
df['weekday_cos'] = np.cos(2 * np.pi * df['weekday'] / 6)

# 분석에 사용할 6개 필드: 온도, 전력사용량(Target), 시간_sin, 시간_cos, 주말
#features_list = ['Temperature', 'Usage', 'hour_sin', 'hour_cos']
#features_list = ['Temperature', 'Usage', 'hour_sin', 'hour_cos', 'is_weekend']
features_list = ['Temperature', 'Usage', 'hour_sin', 'hour_cos', 'weekday_sin', 'weekday_cos']
data = df[features_list].values

# [단계 3] 데이터 전처리 (스케일링)
scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(data)

# 슬라이딩 윈도우 데이터 생성 (과거 24시간 기반 예측)
def create_sequences(data, window_size=24):
    X, y = [], []
    for i in range(len(data) - window_size):
        X.append(data[i:i + window_size, :]) # 6개 변수의 과거 24시간 기록
        y.append(data[i + window_size, 1])    # 맞추고자 하는 값 (Usage: 인덱스 1)
    return np.array(X), np.array(y)

window_size = 168
X, y = create_sequences(scaled_data, window_size)

# 학습/테스트 데이터 분할 (순서 유지)
split = int(len(X) * 0.8)
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]

# [단계 4] 모델 설계 및 학습 (단일 LSTM)
model = Sequential([
    # Input shape: (24 타임스텝, 5개 피처)
    LSTM(64, activation='tanh', input_shape=(X_train.shape[1], X_train.shape[2])),
    Dropout(0.2),
    Dense(1)
])

model.compile(optimizer='adam', loss='mse')

early_stop = EarlyStopping(monitor='val_loss', patience=7, restore_best_weights=True)

history = model.fit(
    X_train, y_train,
    epochs=50,
    batch_size=32,
    validation_split=0.1,
    callbacks=[early_stop],
    verbose=1
)

# [단계 5] 예측 및 역스케일링 (실제 값 복원)
predictions_scaled = model.predict(X_test)

def get_original_units(scaled_values, scaler, feature_count, target_idx=1):
    # 역변환을 위해 5열 구조의 더미 배열 생성
    dummy = np.zeros((len(scaled_values), feature_count))
    dummy[:, target_idx] = scaled_values.flatten()
    return scaler.inverse_transform(dummy)[:, target_idx]

# 실제 전력량 단위로 변환
y_test_original = get_original_units(y_test, scaler, len(features_list))
predictions_original = get_original_units(predictions_scaled, scaler, len(features_list))

# [단계 6] 결과 시각화
plt.figure(figsize=(14, 6))
plt.plot(y_test_original[:168], label='실제값', color='#1f77b4', linewidth=2)
plt.plot(predictions_original[:168], label='예측값', color='#ff7f0e', linestyle='--', linewidth=2)
plt.title('다변수 LSTM Model: 스마트 기기 전력 사용량 예측')
plt.xlabel('시간')
plt.ylabel('전력 사용량(kW)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()