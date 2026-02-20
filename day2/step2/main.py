import pandas as pd
import koreanize_matplotlib # 한글 폰트 설정을 위한 라이브러리입니다. matplotlib에서 한글이 깨지는 문제를 해결해줍니다.
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose

# generate_aircon_sales.py에서 저장한 CSV 파일을 읽어서 사용합니다   
data = pd.read_csv("./data/aircon_sales.csv", index_col='Month', parse_dates=True)

# 2. 시계열 분해 (승법 모델 선택: 추세에 따라 계절 진폭이 커지므로)
# model='multiplicative' (승법) 또는 'additive' (가법)
result = seasonal_decompose(data['Sales'], model='multiplicative')

# 3. 결과 시각화
plt.rcParams['figure.figsize'] = [10, 8]
result.plot()
plt.show()
