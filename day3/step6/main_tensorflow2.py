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

#batch_size를 크게 설정하기 하여 성능 향상하기
#수정: `32` → **`256`** 또는 **`512`**
#        batch_size의 값을 무조건 크게 설정한다고 해서 항상 좋은 것은 아닙니다.
#       32, 64, 128, 256 까지는 결과가 비슷하지만 
#       512 이상부터는 메모리 부족 현상, 결과 값이 다르게 나올 수 있습니다
#       output 폴더에 수치 변경에 따른 결과 파일들을 참고하세요.
#           
#효과: 한 번에 처리하는 데이터 양이 늘어나 GPU의 수천 개 CUDA 코어를 꽉 채워 쓸 수 있습니다. 에포크당 소요 시간이 대폭 줄어듭니다.
#주의: 배치 사이즈를 키우면 한 에포크당 가중치 업데이트 횟수(Iteration)가 줄어드므로, 학습률(`lr`)을 조금 높여주는 것이 좋습니다.
#      # [단계 5] 모델 컴파일 및 학습
#      optimizer='adam' 학습률 기본값 0.001을 의미하는 것입니다
#      model.compile(optimizer=optimizer, loss='mse')
#
#      학습률을 0.002로 높여서 설정 (기본값보다 2배 빠른 보폭)
#      optimizer = Adam(learning_rate=0.002)
#      model.compile(optimizer=optimizer, loss='mse')
#

# 메모리 동적 할당 (RTX 30 시리즈 필수)
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    tf.config.experimental.set_memory_growth(gpus[0], True)

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
    Dense(1)
])

# [단계 5] 모델 컴파일 및 학습
#model.compile(optimizer='adam', loss='mse')
#      학습률을 0.002로 높여서 설정 (기본값보다 2배 빠른 보폭)
optimizer = Adam(learning_rate=0.002)
model.compile(optimizer=optimizer, loss='mse')


# 과적합 방지를 위해 EarlyStopping 유지
early_stop = EarlyStopping(monitor='val_loss', patience=7, restore_best_weights=True)

# 모델 학습
history = model.fit(
    X_train, y_train,
    epochs=50,
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
