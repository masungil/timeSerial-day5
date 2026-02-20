import pandas as pd
import numpy as np

# 1. 2026-01-01 부터 5일 간 날짜 배열을 생성한다
dates = pd.date_range('2026-01-01', periods=5, freq='D')
print(f"dates -> \n{dates}")

# 2. 결측치가 포함된 5일간의 기온 데이터 생성한다
temperature = {'temperature': [2.0, np.nan, 5.0, 4.0, 7.0]}
print(f"temperature -> \n{temperature}")

# 3. 데이터프레임을 생성한다 
df = pd.DataFrame(temperature, index=dates)
print(f"df -> \n{df}")

# 3. 전처리: 결측치 처리 (선형 보간법)
df['interpolated'] = df['temperature'].interpolate()
print(f"결측치 처리 후 df -> \n{df}")

# 4. 전처리: 이동 평균 (2일 기준)
df['moving_avg'] = df['interpolated'].rolling(window=2).mean()
print(f"이동 평균 처리 후 df -> \n{df}")
