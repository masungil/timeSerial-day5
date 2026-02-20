import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from pmdarima import auto_arima

# [1] 데이터 로드
file_path = './data/household_daily_usage.csv'
# parse_dates=['dt']: 'dt' 컬럼을 문자열이 아닌 시계열 날짜 객체로 읽어옴
df = pd.read_csv(file_path, parse_dates=['dt'], index_col='dt')

# [2] 시계열 데이터 분해 (Seasonal Decomposition)
# - 시계열 데이터를 구성하는 3요소(추세, 계절성, 잔차)를 시각적으로 분리하여 확인
# - model='additive': 가법 모델 (Trend + Seasonal + Resid)
# - period=7: 주간 주기를 확인하기 위해 7일 설정
print("데이터 분해를 시작합니다 (Trend, Seasonal, Resid 확인)...")
result = seasonal_decompose(df['Global_active_power'], model='additive', period=7)

# 결과 그래프 출력: 추세(상승/하강), 계절성(패턴), 잔차(불규칙 변동)를 한눈에 볼 수 있음
result.plot()
plt.show()

# [3] 최적의 ARIMA 모델 탐색 (auto_arima)
# - ARIMA(p, d, q) 모델의 최적 파라미터를 자동으로 찾아주는 알고리즘
# - m=7: 계절성 주기 (여기서는 7일 단위의 주간 패턴)
# - seasonal=True: SARIMA(Seasonal ARIMA)를 적용하여 계절적 요인 반영
# - stepwise=True: 연산량을 줄이기 위해 최적의 파라미터를 단계별로 검색
print("최적의 ARIMA 파라미터를 찾는 중입니다 (자동 탐색 단계)...")
stepwise_model = auto_arima(df['Global_active_power'], 
                            m=7,                
                            seasonal=True,      
                            stepwise=True,      
                            trace=False         
                            )

# 탐색 완료 후 최적의 모델 요약 정보 출력
print(stepwise_model.summary())

# [4] 학습 및 미래 예측 테스트
# - 마지막 30일을 테스트용 데이터로 사용하여 모델의 정확도 검증
train = df['Global_active_power'][:-30]
test = df['Global_active_power'][-30:]

# 훈련 데이터로 모델 학습
stepwise_model.fit(train)

# 학습된 모델로 테스트 데이터 기간(30일)만큼 미래 예측
future_forecast = stepwise_model.predict(n_periods=30)

# [5] 예측 결과 시각화
# - 실제 데이터(Actual)와 모델의 예측값(Prediction)을 비교
plt.figure(figsize=(12, 6))
plt.plot(test.index, test.values, label='Actual (실제 사용량)')
plt.plot(test.index, future_forecast, label='Auto-ARIMA Prediction (예측치)', color='red')
plt.title('Energy Consumption Prediction with Auto-ARIMA')
plt.legend()
plt.grid(True)
plt.show()