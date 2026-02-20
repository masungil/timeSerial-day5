import numpy as np
import pandas as pd
import koreanize_matplotlib
import matplotlib.pyplot as plt
import tensorflow as tf
import joblib
import os

# 1. Attention 레이어 클래스 정의 (로드 시 필수)
# @tf.keras.utils.register_keras_serializable()는 학습 시 등록된 이름을 찾기 위해 필요할 수 있습니다.
@tf.keras.utils.register_keras_serializable(package="Custom")
class AttentionLayer(tf.keras.layers.Layer):
    def __init__(self, **kwargs):
        super(AttentionLayer, self).__init__(**kwargs)

    def build(self, input_shape):
        self.W = self.add_weight(name="att_weight", shape=(input_shape[-1], 1), initializer="normal")
        self.b = self.add_weight(name="att_bias", shape=(input_shape[1], 1), initializer="zeros")
        super(AttentionLayer, self).build(input_shape)

    def call(self, inputs):
        et = tf.nn.tanh(tf.matmul(inputs, self.W) + self.b)
        at = tf.nn.softmax(et, axis=1)
        context = inputs * at
        return tf.reduce_sum(context, axis=1), at

    def get_config(self):
        return super(AttentionLayer, self).get_config()

# 2. 파일 경로 설정
model_path = './model/air_passengers_best_model.h5'
scaler_path = './model/air_passengers_scaler.pkl'
data_path = './data/flights.csv'

# 파일 존재 확인
if not all(os.path.exists(f) for f in [model_path, scaler_path, data_path]):
    print("❌ 필요한 파일(모델, 스케일러, 데이터)이 없습니다. 경로를 확인해주세요.")
else:
    # 3. 모델 및 스케일러 로드
    # 'Custom>AttentionLayer' 에러를 방지하기 위해 custom_object_scope를 사용합니다.
    custom_objects = {'AttentionLayer': AttentionLayer}
    
    with tf.keras.utils.custom_object_scope(custom_objects):
        model = tf.keras.models.load_model(model_path, compile=False)
    
    scaler = joblib.load(scaler_path)
    print("✅ 모델 및 스케일러 로드 완료")

    # 4. 원본 데이터 로드 (미래 예측의 기준점)
    data_df = pd.read_csv(data_path)
    col_name = 'passengers' if 'passengers' in data_df.columns else 'Passengers'
    passengers = data_df[col_name].values.astype(float)

    # 5. 미래 예측 (1961년 12개월)
    # 마지막 12개월의 차분 데이터 준비
    seasonal_period = 12
    diff_passengers = passengers[seasonal_period:] - passengers[:-seasonal_period]
    diff_scaled = scaler.transform(diff_passengers.reshape(-1, 1))
    
    # 마지막 시퀀스 (1960년 패턴)
    current_batch = diff_scaled[-12:].reshape(1, 12, 1)
    
    future_diff_preds = []
    print("🔮 1961년 미래 예측 진행 중...")
    
    for i in range(12):
        pred_scaled = model.predict(current_batch, verbose=0)
        future_diff_preds.append(pred_scaled[0, 0])
        
        # 윈도우 슬라이딩 업데이트
        new_val = pred_scaled.reshape(1, 1, 1)
        current_batch = np.append(current_batch[:, 1:, :], new_val, axis=1)

    # 6. 역변환 및 복원
    future_diff_unscaled = scaler.inverse_transform(np.array(future_diff_preds).reshape(-1, 1)).flatten()
    
    # 1961년 최종값 = 1960년 실제값 + 예측된 증감량
    last_year_1960 = passengers[-12:]
    forecast_1961 = last_year_1960 + future_diff_unscaled

    # 7. 시각화 및 출력
    future_months = pd.date_range(start='1961-01-01', periods=12, freq='MS')
    forecast_series = pd.Series(forecast_1961, index=future_months)

    plt.figure(figsize=(12, 6))
    plt.plot(pd.to_datetime(data_df['Month'])[-24:], passengers[-24:], label='실제값 (1959-1960)', marker='o')
    plt.plot(forecast_series, label='예측값 (1961)', marker='x', color='red', linestyle='--')
    plt.title('항공기 승객 수 미래 예측 (1961년)')
    plt.ylabel('승객 수')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

    print("\n--- 1961년 예측 결과 ---")
    for month, val in zip(future_months, forecast_1961):
        print(f"{month.strftime('%Y-%m')}: {int(val)}명")