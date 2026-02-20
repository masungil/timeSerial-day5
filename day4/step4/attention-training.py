import numpy as np
import pandas as pd
import koreanize_matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf
from tensorflow.keras import layers, Model
from sklearn.preprocessing import MinMaxScaler
import os
import joblib  # 스케일러(MinMaxScaler) 저장을 위한 라이브러리

# 1. 데이터 로드 및 전처리
# flights.csv 데이터를 읽어와서 승객 수(Passengers) 데이터만 추출합니다.
data_df = pd.read_csv('./data/flights.csv')
passengers = data_df['Passengers'].values.astype(float)

# 계절성 차분 (Seasonal Differencing)
# 시계열 데이터의 계절적 패턴을 제거하여 정상성(Stationarity)을 확보합니다.
# 12개월 전의 데이터와 현재 데이터의 차이를 계산합니다.
seasonal_period = 12
diff_passengers = passengers[seasonal_period:] - passengers[:-seasonal_period]
diff_passengers = diff_passengers.reshape(-1, 1)

# 데이터 정규화 (Normalization)
# 신경망 학습의 안정성과 속도를 위해 데이터를 0~1 사이 값으로 변환합니다.
scaler = MinMaxScaler()
data_scaled = scaler.fit_transform(diff_passengers)

# [중요] 스케일러 파일 저장
# 추후 예측 단계(Inference)에서 예측된 값을 다시 원래 단위로 복원(Inverse Transform)하기 위해 저장합니다.
scaler_filename = "./model/air_passengers_scaler.pkl"
if not os.path.exists('./model'):
    os.makedirs('./model')
joblib.dump(scaler, scaler_filename)
print(f"✅ 스케일러 저장 완료: {scaler_filename}")

# 시퀀스 생성 함수
# 과거의 데이터(look_back 기간)를 기반으로 다음 시점의 값을 예측하기 위한 데이터셋을 만듭니다.
def create_dataset(dataset, look_back=12):
    X, y = [], []
    for i in range(len(dataset) - look_back):
        X.append(dataset[i:(i + look_back), 0]) # 과거 12개월 데이터
        y.append(dataset[i + look_back, 0])      # 정답(13개월째 데이터)
    return np.array(X), np.array(y)

look_back = 12
X, y = create_dataset(data_scaled, look_back)

# LSTM 입력을 위한 3차원 변환: (샘플 수, 타임스텝, 특성 수)
X = X.reshape((X.shape[0], X.shape[1], 1))

# 학습/테스트 데이터 분리 (최근 24개월 데이터를 테스트용으로 사용)
train_size = len(X) - 24
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

# 2. Attention 레이어 정의
# LSTM의 모든 시점 출력 중 중요한 부분에 가중치를 부여하는 메커니즘입니다.
@tf.keras.utils.register_keras_serializable() # 모델 저장/로드 시 커스텀 레이어 인식을 위해 등록
class AttentionLayer(layers.Layer):
    def __init__(self, **kwargs):
        super(AttentionLayer, self).__init__(**kwargs)

    def build(self, input_shape):
        # 학습 가능한 가중치(Weight)와 편향(Bias) 정의
        self.W = self.add_weight(name="att_weight", shape=(input_shape[-1], 1), initializer="normal")
        self.b = self.add_weight(name="att_bias", shape=(input_shape[1], 1), initializer="zeros")
        super(AttentionLayer, self).build(input_shape)

    def call(self, inputs):
        # Attention 점수 계산 (Tanh 활성화 함수 사용)
        et = tf.nn.tanh(tf.matmul(inputs, self.W) + self.b)
        # Softmax를 통해 각 시점의 가중치(합계 1) 산출
        at = tf.nn.softmax(et, axis=1)
        # 원본 입력에 가중치를 곱하여 문맥 벡터(Context Vector) 생성
        context = inputs * at
        # 가중치가 적용된 벡터들을 합산하여 최종 출력
        return tf.reduce_sum(context, axis=1), at

    def get_config(self):
        # 모델의 설정을 반환 (저장된 모델을 불러올 때 필요)
        config = super(AttentionLayer, self).get_config()
        return config

# 3. 모델 구축 및 학습
inputs = layers.Input(shape=(look_back, 1))
# return_sequences=True는 모든 시점의 출력을 Attention 레이어로 전달하기 위함입니다.
lstm_out = layers.LSTM(128, return_sequences=True)(inputs)
# Attention 적용: 시계열 데이터 내에서 중요한 패턴이 있는 시점을 강조합니다.
attention_out, _ = AttentionLayer()(lstm_out)
# 최종 예측 값을 위한 Dense 레이어
prediction = layers.Dense(1)(attention_out)

model = Model(inputs=inputs, outputs=prediction)
model.compile(optimizer='adam', loss='mse')

print("🚀 고성능 Attention-LSTM 모델 학습 중...")
# 에포크 300회 학습
model.fit(X_train, y_train, epochs=300, batch_size=16, verbose=0)

# [중요] 학습된 모델 저장
# .h5 형식으로 저장하여 추후 추론 파일에서 불러와 사용할 수 있게 합니다.
model_filename = "./model/air_passengers_best_model.h5"
model.save(model_filename)
print(f"✅ 모델 저장 완료: {model_filename}")

# 4. 성능 검증 (MAPE 확인)
# 테스트 데이터에 대해 예측 수행
y_pred_diff_scaled = model.predict(X_test)
# 정규화된 값을 원래의 차분값 스케일로 복원
y_pred_diff = scaler.inverse_transform(y_pred_diff_scaled).flatten()

# 차분된 값을 원래의 승객 수 단위로 복원 (이전 해의 같은 달 값에 더함)
actual_start_idx = len(passengers) - 24
y_pred_final = []
for i in range(24):
    prev_year_val = passengers[actual_start_idx - seasonal_period + i]
    y_pred_final.append(prev_year_val + y_pred_diff[i])

y_pred_final = np.array(y_pred_final)
y_actual_final = passengers[actual_start_idx:]

# MAPE(Mean Absolute Percentage Error): 평균 절대 백분율 오차
# 실제값 대비 오차가 몇 %인지 나타내는 지표입니다.
mape = np.mean(np.abs((y_actual_final - y_pred_final) / y_actual_final)) * 100
print(f"📊 최종 모델의 오차율: {mape:.2f} %")

# 5. 시각화
plt.figure(figsize=(12, 5))
plt.plot(y_actual_final, label='실제값)', marker='o')
plt.plot(y_pred_final, label=f'예측값, 오차율: {mape:.2f}%', marker='x', color='red')
plt.title('항공기 승객 수 예측 결과 (Attention 기반 LSTM)')
plt.xlabel('기간 (최근 24개월)')
plt.ylabel('승객 수')
plt.legend()
plt.grid(True)
plt.show()