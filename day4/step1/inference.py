import pandas as pd
import numpy as np
import joblib
from tensorflow.keras.models import load_model
from tensorflow.keras import mixed_precision

# 혼합 정밀도(mixed_float16) 정책 설정
policy = mixed_precision.Policy('mixed_float16')
mixed_precision.set_global_policy(policy)


# 1. 저장된 자원 로드 (불러오기)
# 컴파일 설정을 불러오지 않음
# 학습 시에는 '정답과 얼마나 틀렸는지' 계산하는 MSE(Loss) 정보가 필수적이지만, 예측 시에는 '입력을 넣고 출력만 뽑는' 연산만 수행하기 때문입니다.
model = load_model('./model/power_usage_lstm_model.h5', compile=False)
scaler = joblib.load('./model/power_usage_scaler.pkl')

# 2. 데이터 준비 (데이터 가공)
# 실제 데이터셋에서 2025-09-20 01:00 ~ 2025-09-21 00:00 (24시간) 데이터를 추출합니다.
df = pd.read_csv('./data/power_usage_dataset_3month.csv')
df['Date'] = pd.to_datetime(df['Date'])

# 예측 기준 시간 설정
target_time = pd.to_datetime('2025-09-21 01:00')
start_time = target_time - pd.Timedelta(hours=24)
end_time = target_time - pd.Timedelta(hours=1)

# 과거 24시간 데이터 필터링
past_24h = df[(df['Date'] >= start_time) & (df['Date'] <= end_time)].copy()

# [단계 3] 특성 공학: 시간 및 요일 주기성 반영
past_24h['hour'] = past_24h['Date'].dt.hour
past_24h['hour_sin'] = np.sin(2 * np.pi * past_24h['hour'] / 23)
past_24h['hour_cos'] = np.cos(2 * np.pi * past_24h['hour'] / 23)
past_24h['weekday'] = past_24h['Date'].dt.weekday
past_24h['weekday_sin'] = np.sin(2 * np.pi * past_24h['weekday'] / 6)
past_24h['weekday_cos'] = np.cos(2 * np.pi * past_24h['weekday'] / 6)


# 과거 데이터에 시간 특성 추가
input_features = past_24h[['Temperature', 'Usage', 'hour_sin', 'hour_cos', 'weekday_sin', 'weekday_cos']].values

# 4. 정규화 및 텐서 변환
# 학습 때 사용한 스케일러로 데이터를 0~1 사이로 변환합니다.
scaled_input = scaler.transform(input_features)
# 모델 입력 모양에 맞게 변환: (Batch, Time, Features) -> (1, 24, 6)
X_input = scaled_input.reshape(1, 24, 6)

# 5. 예측 (Inference)
pred_scaled = model.predict(X_input, verbose=0)

# 6. 결과 복원 (결과 활용)
# 예측된 0~1 사이 값을 실제 전력량(kW) 단위로 되돌립니다.
# 21일 01시의 온도(19.5도라 가정)와 함께 역스케일링을 수행합니다.
target_temp = 19.5  # 21일 01시 온도
target_hour_sin = np.sin(2 * np.pi * target_time.hour / 23)
target_hour_cos = np.cos(2 * np.pi * target_time.hour / 23)
target_weekday_sin = np.sin(2 * np.pi * target_time.weekday() / 6)
target_weekday_cos = np.cos(2 * np.pi * target_time.weekday() / 6)

# 역스케일링을 위해 더미 행렬 생성 (4개 특성 규격을 맞춤)
dummy = np.zeros((1, 6))
dummy[0, 0] = target_temp      # 온도
dummy[0, 1] = pred_scaled[0,0] # 예측된 전력량
dummy[0, 2] = target_hour_sin  # 시간 sin
dummy[0, 3] = target_hour_cos  # 시간 cos
dummy[0, 4] = target_weekday_sin  # 요일 sin
dummy[0, 5] = target_weekday_cos  # 요일 cos

# 예측된 전력량 역스케일링해서 얻기 
final_prediction = scaler.inverse_transform(dummy)[0, 1]

print("-" * 50)
print(f"📅 예측 대상 시간: {target_time}")
print(f"🌡️ 입력된 기온: {target_temp}°C")
print(f"⚡ 예측된 전력 사용량: {final_prediction:.4f} kW")
print("-" * 50)