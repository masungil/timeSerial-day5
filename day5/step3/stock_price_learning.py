import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import FinanceDataReader as fdr
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

# 1. 데이터 수집 (삼성전자 종목코드: 005930)
# 2018년부터 현재까지의 데이터를 가져옵니다.
df = fdr.DataReader('005930', '2018-01-01')

# 2. 데이터 전처리
# '종가(Close)' 데이터만 사용하며, 0~1 사이로 정규화합니다.
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(df['Close'].values.reshape(-1, 1))

# 3. 학습 데이터 생성
# 과거 60일간의 데이터를 보고 다음날 주가를 예측하도록 설정합니다.
window_size = 60
X, y = [], []

for i in range(window_size, len(scaled_data)):
    X.append(scaled_data[i-window_size:i, 0])
    y.append(scaled_data[i, 0])

X, y = np.array(X), np.array(y)
X = np.reshape(X, (X.shape[0], X.shape[1], 1))

# 학습용과 테스트용 분리 (최근 100일을 테스트용으로 사용)
train_size = int(len(X) * 0.8)
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

# 4. LSTM 모델 구축
model = Sequential([
    LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], 1)),
    Dropout(0.2),
    LSTM(units=50, return_sequences=False),
    Dropout(0.2),
    Dense(units=1)
])

model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(X_train, y_train, epochs=20, batch_size=32)

# 5. 예측 및 결과 시각화
predictions = model.predict(X_test)
predictions = scaler.inverse_transform(predictions) # 정규화 되돌리기
actual = scaler.inverse_transform(y_test.reshape(-1, 1))

plt.figure(figsize=(12, 6))
plt.plot(actual, label='실제 가격')
plt.plot(predictions, label='예상 가격')
plt.title('삼성전자 주가 예측')
plt.legend()
plt.show()