import pandas as pd
import numpy as np
import joblib
from tensorflow.keras.models import load_model

# [1] 저장된 모델 및 스케일러 불러오기
# - 학습 때 저장했던 최종 결과물들을 메모리에 로드합니다.
print("추론을 위한 모델과 스케일러를 로딩 중입니다...")
sarima_model = joblib.load('./model/sarima_final.pkl')
# compile=False: 추론만 할 것이므로 학습 설정은 불러오지 않아 속도를 높임
lstm_model = load_model('./model/lstm_final.h5', compile=False) 
scaler = joblib.load('./model/scaler.pkl')

# [2] 미래 예측을 위한 기반 데이터(날씨) 준비
# - 미래 시점의 전력량은 모르지만, '미래의 날씨 예보 데이터'는 알고 있다고 가정합니다.
# - 여기서는 데이터의 가장 마지막 7일치를 미래 예보 데이터로 시뮬레이션합니다.
weather_path = '.\data\paris_weather_data.csv'
df_weather = pd.read_csv(weather_path, parse_dates=['time'], index_col='time')
df_weather['temp_est'] = (df_weather['tmin'] + df_weather['tmax']) / 2
df_weather = df_weather[['temp_est', 'tmin', 'tmax', 'prcp']].interpolate().ffill().bfill()

future_X = df_weather.iloc[-7:].copy()
future_X['is_weekend'] = future_X.index.dayofweek.map(lambda x: 1 if x >= 5 else 0)

# [3] SARIMAX 미래 예측
# - 외생 변수(미래 날씨)를 입력받아 즉시 7일치를 예측합니다.
sarima_forecast = sarima_model.predict(n_periods=7, X=future_X)

# [4] LSTM 미래 예측 (Recursive Prediction)
# - LSTM은 '과거 7일'의 데이터가 필요하므로, 루프를 돌며 예측된 값을 다음 예측의 입력으로 넣는 과정이 필요합니다.
lstm_predictions = []

# - (A) 가장 최근의 실제 날씨 정보를 담은 입력 데이터 틀 생성 (6개 컬럼: 전력, 온도3종, 강수, 주말)
test_input_raw = np.zeros((7, 6))
test_input_raw[:, 1:] = future_X.values # 미래 날씨 정보 채우기
current_input_scaled = scaler.transform(test_input_raw) # 스케일링 적용
current_input_scaled = current_input_scaled.reshape(1, 7, 6) # (Batch, Window, Feature)

print("\n미래 7일간의 에너지 소비량 추론을 시작합니다...")

for i in range(7):
    # - (B) 현재 윈도우 데이터로 다음 시점(1일) 예측
    lstm_scaled_pred = lstm_model.predict(current_input_scaled, verbose=0)
    
    # - (C) 예측값 역스케일링: 원래 단위(kW)로 복원하여 저장
    pred_val_scaled = lstm_scaled_pred.flatten()[0]
    dummy_output = np.zeros((1, 6))
    dummy_output[0, 0] = pred_val_scaled 
    inv_pred = scaler.inverse_transform(dummy_output)[0, 0]
    lstm_predictions.append(inv_pred)
    
    # - (D) 다음 예측을 위한 '윈도우 이동' 업데이트
    # i+1일의 날씨 정보를 가져와서 새로운 입력 행 구성
    new_row = np.zeros((1, 1, 6))
    new_row[0, 0, 0] = pred_val_scaled # 방금 예측한 전력량을 다음 날의 '과거 전력량'으로 사용
    if i < 6: 
        # 다음 날의 날씨 정보로 업데이트
        next_weather_scaled = scaler.transform(test_input_raw)[i+1, 1:]
        new_row[0, 0, 1:] = next_weather_scaled
    
    # 맨 앞 데이터는 버리고, 새로운 예측값+날씨 행을 맨 뒤에 추가 (Sliding Window)
    current_input_scaled = np.append(current_input_scaled[:, 1:, :], new_row, axis=1)

# [5] 최종 앙상블 결과 출력 (SARIMAX 40% + LSTM 60%)
print("\n" + "="*45)
print(f"{'예측 날짜':<12} | {'상태':<8} | {'예측 소비량(kW)':<15}")
print("-" * 45)

for i in range(7):
    ensemble_val = (sarima_forecast.values[i] * 0.4) + (lstm_predictions[i] * 0.6)
    target_date = future_X.index[i].strftime('%Y-%m-%d')
    weekend_str = "주말" if future_X['is_weekend'].iloc[i] == 1 else "평일"
    print(f"{target_date} | {weekend_str:<6} | {ensemble_val:>14.2f}")

print("="*45)
print("위 예측치는 통계 모델과 딥러닝 모델의 앙상블 결과입니다.")