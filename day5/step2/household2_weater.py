import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pmdarima import auto_arima

# [1] 데이터 로딩
# - 전력 사용량 데이터와 파리(Paris) 날씨 데이터를 각각 불러옴
df_energy = pd.read_csv('./data/household_daily_usage.csv', parse_dates=['dt'], index_col='dt')
df_weather = pd.read_csv('./data/paris_weather_data.csv', parse_dates=['time'], index_col='time')

# [2] 날씨 데이터 전처리
# - tmin(최저기온), tmax(최고기온), prcp(강수량) 컬럼 선택
weather_cols = ['tmin', 'tmax', 'prcp']
df_weather = df_weather[weather_cols].copy()

# - 분석에 필요한 '평균 온도(temp_est)' 계산
df_weather['temp_est'] = (df_weather['tmin'] + df_weather['tmax']) / 2

# - 날씨 데이터 결측치 처리: 시계열 데이터이므로 선형 보간(interpolate)과 ffill/bfill로 연속성을 유지하며 채움
df_weather = df_weather.interpolate().ffill().bfill()

# [3] 전력 데이터와 날씨 데이터 병합 (Merge)
# - 두 데이터의 인덱스(날짜)가 일치하는 구간만 병합(inner join)
df = df_energy.join(df_weather, how='inner')

# [4] 파생 변수 생성: 주말 여부 (is_weekend)
# - 가정: 가계 전력 소비는 평일과 주말의 패턴이 매우 다를 것임
# - dayofweek: 0(월) ~ 6(일). 5와 6이면 1(주말), 나머지는 0(평일)으로 설정
df['is_weekend'] = df.index.dayofweek.map(lambda x: 1 if x >= 5 else 0)

# [5] 분석 데이터(Target & Features) 준비
# - y (Target): 예측하고자 하는 목표인 '전력 사용량(Global_active_power)'
y = df['Global_active_power']
# - X (Exogenous Variables): 예측에 도움을 줄 외부 변수들 (기온, 강수량, 주말 여부)
X = df[['temp_est', 'tmin', 'tmax', 'prcp', 'is_weekend']]

# - 마지막 30일을 테스트용으로 분리 (훈련 셋과 테스트 셋의 X, y 구간을 동일하게 맞춤)
train_y, test_y = y[:-30], y[-30:]
train_X, test_X = X[:-30], X[-30:]

# [6] SARIMAX 모델 학습
# - X=train_X: 외부 변수(Exogenous)를 반영하여 학습을 수행
# - 날씨와 주말 정보를 모두 고려하여 전력 소비의 패턴을 파악함
print("외부 변수(날씨, 주말) 정보를 반영하여 최적의 SARIMAX 모델을 학습 중입니다...")
stepwise_model = auto_arima(train_y, 
                            X=train_X, 
                            m=7, 
                            seasonal=True, 
                            stepwise=True, 
                            trace=True)

# [7] 예측 수행 및 결과 시각화
# - 예측 시에도 미래 시점의 날씨 정보(test_X)가 반드시 필요함
future_forecast = stepwise_model.predict(n_periods=30, X=test_X)

plt.figure(figsize=(12, 6))
plt.plot(test_y.index, test_y.values, label='Actual (실제)', color='blue')
plt.plot(test_y.index, future_forecast, label='SARIMAX Prediction (날씨+주말 반영)', color='green', linestyle='--')
plt.title('Energy Prediction with Weather & Weekend Factor')
plt.legend()
plt.grid(True)
plt.show()