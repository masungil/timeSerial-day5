import pandas as pd
import numpy as np
import koreanize_matplotlib # 한글 폰트 설정을 위한 라이브러리입니다. matplotlib에서 한글이 깨지는 문제를 해결해줍니다.
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Input

# 1. 데이터 로드 및 정렬
df = pd.read_csv('./data/clean_power_usage_dataset.csv')
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values('Date')

# 2. 결측치 처리 (시간축 생성 및 선형 보간)
df = df.set_index('Date').resample('h').asfreq()
df['Usage'] = df['Usage'].interpolate(method='linear')
df = df.reset_index()

# 3. 정규화 (Min-Max Scaling)
scaler = MinMaxScaler()
# 학습 시 2차원 배열을 사용했음을 기억하세요.
df['Usage_scaled'] = scaler.fit_transform(df[['Usage']])

# 4. 지도 학습 데이터셋 생성 (Sliding Window)
window_size = 24
X, y = [], []
scaled_data = df['Usage_scaled'].values

for i in range(window_size, len(scaled_data)):
    X.append(scaled_data[i-window_size:i]) # 과거 24시간
    y.append(scaled_data[i])               # 현재 시점 (정답)

X = np.array(X)
y = np.array(y)

# LSTM 입력을 위해 3차원 변환: (샘플 수, 타임스텝, 특성 수)
X = X.reshape((X.shape[0], X.shape[1], 1))

# 학습/테스트 데이터 분할 (8:2)
train_size = int(len(X) * 0.8)
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

print(f"학습 데이터 크기: {X_train.shape}")
print(f"테스트 데이터 크기: {X_test.shape}")

# 5. LSTM 모델 설계 (최신 Keras 방식 적용)
model = Sequential([
    Input(shape=(window_size, 1)), 
    LSTM(64, activation='tanh'),
    Dense(32, activation='tanh'),
    Dense(1)
])

model.compile(optimizer='adam', loss='mse')

# 6. 모델 학습
print("모델 학습 시작...")
history = model.fit(X_train, y_train, epochs=50, batch_size=16, validation_split=0.1, verbose=1)

# 7. 결과 예측 및 차원 오류 수정
predictions_scaled = model.predict(X_test)

# inverse_transform에는 반드시 2D 배열이 들어가야 함
predictions = scaler.inverse_transform(predictions_scaled)

# y_test는 (N,) 형태의 1차원이므로 .reshape(-1, 1)로 2차원 변환 후 복원
y_test_unscaled = scaler.inverse_transform(y_test.reshape(-1, 1))

# 8. 시각화
plt.figure(figsize=(12, 6))
plt.plot(y_test_unscaled, label='Actual Usage', color='blue')
plt.plot(predictions, label='Predicted Usage', color='red', linestyle='--')
plt.title('Smart Device Power Usage Prediction')
plt.xlabel('Time (Hours)')
plt.ylabel('Usage')
plt.legend()
plt.grid(True)
plt.show()

plt.plot(history.history['loss'], label='학습손실')
plt.plot(history.history['val_loss'], label='검증손실')
plt.legend()
plt.show()