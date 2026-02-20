import os
# TensorFlow의 oneDNN 최적화 관련 로그 메시지를 억제합니다.
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import numpy as np
import FinanceDataReader as fdr
import joblib
from tensorflow.keras.models import load_model

# 1. 저장된 모델과 스케일러 불러오기
# 학습 과정(learning.py)에서 저장된 LSTM 모델 파일을 로드합니다.
model = load_model('./model/samsung_model.h5')
# 학습 데이터 정규화에 사용했던 스케일러를 로드하여 동일한 기준으로 전처리합니다.
scaler = joblib.load('./model/stock_scaler.pkl')

# 2. 최신 데이터 가져오기
# 모델이 다음 날을 예측하기 위해서는 과거 60일치(window_size)의 데이터가 필요합니다.
# FinanceDataReader를 사용하여 삼성전자의 전체 주가 데이터를 가져옵니다.
df = fdr.DataReader('005930')

# 가장 최근 60일치 종가(Close) 데이터를 추출하고 모델 입력에 맞는 2차원 배열 형태로 변환합니다.
last_60_days_prices = df['Close'].values[-60:].reshape(-1, 1)

# 3. 데이터 전처리 (학습 때와 동일한 스케일러 적용)
# 모델은 0~1 사이의 정규화된 데이터로 학습되었으므로, 입력 데이터도 동일하게 변환해야 합니다.
last_60_days_scaled = scaler.transform(last_60_days_prices)

# 4. 모델 입력 형태에 맞게 변환 (1, 60, 1)
# LSTM 모델의 입력 텐서 형태인 (샘플 수, 타임스텝, 특성 수)에 맞게 차원을 변경합니다.
# 여기서는 1개의 샘플에 대해 60일치 데이터를 1개의 특성(종가)으로 입력합니다.
X_input = np.reshape(last_60_days_scaled, (1, 60, 1))

# 5. 예측 수행
# 학습된 모델을 사용하여 다음 영업일의 주가를 예측합니다.
predicted_stock_price = model.predict(X_input)

# 6. 정규화된 값을 실제 가격으로 복원
# 모델의 출력값(0~1 사이)을 scaler를 이용해 실제 주가 단위(원)로 역변환합니다.
predicted_stock_price = scaler.inverse_transform(predicted_stock_price)

print(f"모델이 예측한 다음 영업일의 삼성전자 주가는: {int(predicted_stock_price[0][0])}원 입니다.")
