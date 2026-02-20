import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Input

# 1. 데이터 로드 및 정렬
df = pd.read_csv('./data/power_usage_dataset.csv')
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values('Date')

# 2. 결측치 처리 (시간축 생성 및 선형 보간)
df = df.set_index('Date').resample('h').asfreq()
df['Usage'] = df['Usage'].interpolate(method='linear')
df = df.reset_index()

# 3. 조정된 데이터 저장 (선형 보간된 데이터)
df.to_csv('./data/clean_power_usage_dataset.csv', index=False)

print("데이터 정제 완료. 'clean_power_usage_dataset.csv' 파일로 저장되었습니다.")