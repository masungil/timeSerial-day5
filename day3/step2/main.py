import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

# 1. 데이터 로드
# 전력 사용량 데이터셋을 불러옵니다.
df = pd.read_csv('./data/power_usage_dataset.csv')
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values('Date')

# --- 2. 결측치 처리 (선형 보간법) ---
# 데이터가 가진 '시간적 연속성'을 보장하기 위해 시간축을 재설정하고 보정합니다.
df = df.set_index('Date').resample('h').asfreq() # 비어있는 시간대 생성
df['Usage'] = df['Usage'].interpolate(method='linear') # 선형 보간법 적용
# 시간축을 재설정하고 보정합니다.
df = df.reset_index()

# --- 3. 시간 정보 분해 (Feature Engineering) ---
# 모델이 시간적 패턴을 파악할 수 있도록 '시간'과 '요일' 정보를 추출합니다.
df['hour'] = df['Date'].dt.hour
df['day_of_week'] = df['Date'].dt.dayofweek # 월요일: 0, 일요일: 6

# --- 4. 정규화 (Min-Max Scaling) ---
# 전력 사용량(Usage) 데이터를 0과 1 사이로 변환합니다.
scaler = MinMaxScaler()
df['Usage_scaled'] = scaler.fit_transform(df[['Usage']])

# --- 5. 지도 학습 데이터셋 생성 (Sliding Window) ---
# 예: 과거 3시간 데이터를 feature(X)로 사용
df['t-1'] = df['Usage'].shift(1)
df['t-2'] = df['Usage'].shift(2)
df['t-3'] = df['Usage'].shift(3)

# 과거 24시간의 사용량을 입력(X)으로, 현재 사용량을 정답(y)으로 설정
window_size = 24
X, y = [], []

scaled_data = df['Usage_scaled'].values

for i in range(window_size, len(scaled_data)):
    X.append(scaled_data[i-window_size:i]) # 과거 24시간 데이터
    y.append(scaled_data[i])               # 현재 시점의 정답

X_final = np.array(X)
y_final = np.array(y)

print(f"변환된 데이터 셋 크기: X={X_final.shape}, y={y_final.shape}")

# 별도의 학습용 데이터프레임을 만들어 저장 합니다.
# (X의 각 시점을 컬럼으로, y를 마지막 컬럼으로)
train_df = pd.DataFrame(X_final, columns=[f't-{i}' for i in range(window_size, 0, -1)])
train_df['target_y'] = y_final
train_df.to_csv('./data/processed_power_usage_dataset.csv', index=False)

df.to_csv('./data/power_usage_dataset_output.csv', index=False)
