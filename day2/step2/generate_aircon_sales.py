import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose

# 1. 데이터 생성 (CSV 형식으로 바로 저장 가능)
data = {
    'Month': pd.date_range(start='2021-01-01', periods=60, freq='MS'),
    'Sales': [
        10, 12, 25, 35, 60, 120, 180, 170, 50, 20, 15, 12,  # 1년차
        12, 14, 30, 42, 75, 145, 220, 210, 60, 25, 18, 15,  # 2년차
        15, 18, 38, 52, 90, 180, 280, 265, 75, 32, 22, 18,  # 3년차
        18, 22, 45, 65, 110, 220, 350, 330, 95, 40, 28, 22, # 4년차
        22, 26, 55, 78, 135, 270, 430, 410, 115, 50, 35, 28 # 5년차
    ]
}

df = pd.DataFrame(data)
df.set_index('Month', inplace=True)

# CSV 파일로 저장하여 다음에 실행을 하기위해 데이터를 data 폴도에 저장합니다
df.to_csv('aircon_sales.csv')

