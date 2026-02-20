import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.regularizers import l2
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import mixed_precision

# 혼합 정밀도(Mixed Precision) 사용 : 16비트와 32비트 연산 혼합
# GPU는 Tensor Core라는 딥러닝 전용 가속기가 있습니다. 
# 기본 32비트 연산을 16비트로 낮춰 연산하면 속도는 2배 빨라지고 
# 메모리 사용량은 절반으로 줄어듭니다.




# 메모리 동적 할당 (RTX 30 시리즈 필수)
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    tf.config.experimental.set_memory_growth(gpus[0], True)

# 혼합 정밀도 정책 설정
policy = mixed_precision.Policy('mixed_float16')
mixed_precision.set_global_policy(policy)

# -한글 폰트 설정
plt.rcParams['font.family'] = 'NanumGothic'
plt.rcParams['axes.unicode_minus'] = False 

# [단계 1] 데이터 로드 및 시간 변환
df = pd.read_csv('./data/power_usage_dataset_3month.csv')
df['Date'] = pd.to_datetime(df['Date'])

# [단계 2] 특성 공학: 시간 및 요일 주기성 반영
df['hour'] = df['Date'].dt.hour
df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 23)
df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 23)

df['weekday'] = df['Date'].dt.weekday
df['weekday_sin'] = np.sin(2 * np.pi * df['weekday'] / 6)
df['weekday_cos'] = np.cos(2 * np.pi * df['weekday'] / 6)

# 분석에 사용할 6개 필드
features_list = ['Temperature', 'Usage', 'hour_sin', 'hour_cos', 'weekday_sin', 'weekday_cos']
data = df[features_list].values

# [단계 3] 데이터 전처리 (스케일링)
scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(data)

def create_sequences(data, window_size=168):
    X, y = [], []
    for i in range(len(data) - window_size):
        X.append(data[i:i + window_size, :]) 
        y.append(data[i + window_size, 1])    # Target: Usage
    return np.array(X), np.array(y)

window_size = 168 # 1주일(168시간) 패턴 학습
X, y = create_sequences(scaled_data, window_size)

# 데이터 분할
split = int(len(X) * 0.8)
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]

# [단계 4] 모델 설계: Stacked LSTM + Dropout + L2 규제 적용
model = Sequential([
    # 첫 번째 LSTM 계층: L2 규제 추가
    LSTM(128, activation='tanh', 
         input_shape=(X_train.shape[1], X_train.shape[2]), 
         return_sequences=True,
         kernel_regularizer=l2(0.0001)), # L2 규제 (가중치 제한)
    Dropout(0.2), # 드롭아웃 (20% 뉴런 비활성화)
    
    # 두 번째 LSTM 계층: L2 규제 추가
    LSTM(64, activation='tanh', 
         return_sequences=False,
         kernel_regularizer=l2(0.0001)),
    Dropout(0.1),
    
    # 출력 계층
    Dense(1, dtype='float32')
])

# [단계 5] 모델 컴파일 및 학습
#model.compile(optimizer='adam', loss='mse')
#      학습률을 0.002로 높여서 설정 (기본값보다 2배 빠른 보폭)
optimizer = Adam(learning_rate=0.001)
model.compile(optimizer=optimizer, loss='mse')


# 과적합 방지를 위해 EarlyStopping 유지
early_stop = EarlyStopping(monitor='val_loss', patience=7, restore_best_weights=True)

# 모델 학습
history = model.fit(
    X_train, y_train,
    epochs=100,
#    batch_size=32,
    batch_size=256, # 수정 : batch_size를 크게 설정하기 하여 성능 향상하기
    validation_split=0.1,
   callbacks=[early_stop],
    verbose=1
)

# [단계 5] 예측 및 역스케일링
predictions_scaled = model.predict(X_test)

def get_original_units(scaled_values, scaler, feature_count, target_idx=1):
    dummy = np.zeros((len(scaled_values), feature_count))
    dummy[:, target_idx] = scaled_values.flatten()
    return scaler.inverse_transform(dummy)[:, target_idx]

y_test_original = get_original_units(y_test, scaler, len(features_list))
predictions_original = get_original_units(predictions_scaled, scaler, len(features_list))

# [단계 6] 결과 시각화
plt.figure(figsize=(14, 6))
plt.plot(y_test_original[:168], label='실제값', color='#1f77b4', linewidth=2)
plt.plot(predictions_original[:168], label='예측값', color='#ff7f0e', linestyle='--', linewidth=2)
plt.title('Stacked LSTM Model: 스마트 기기 전력 사용량 예측')
plt.xlabel('시간')
plt.ylabel('전력 사용량(kW)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
