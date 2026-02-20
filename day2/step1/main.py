import pandas as pd
import koreanize_matplotlib # 한글 폰트 설정을 위한 라이브러리입니다. matplotlib에서 한글이 깨지는 문제를 해결해줍니다.
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose

# 예시 데이터: 월별 항공기 탑승객 수 (Seaborn 등에서 쉽게 구할 수 있음)
# 여기서는 개념 이해를 위해 가상의 데이터를 생성하거나 내장 데이터를 씁니다.
# data = pd.read_csv('https://raw.githubusercontent.com/jbrownlee/Datasets/master/airline-passengers.csv', index_col='Month', parse_dates=True)

# 다음에 실행을 하기위해 데이터를 data 폴도에 저장합니다 
# 아래 코드는 저장된 데이터를 불러옵니다.
# pd.save_csv("./data/airline-passengers.csv")

data = pd.read_csv("./data/airline-passengers.csv", index_col='Month', parse_dates=True)

# 모델 설정: 'multiplicative'(승법 모델)은 변동 폭이 점점 커질 때 주로 사용합니다.
result = seasonal_decompose(data['Passengers'], model='multiplicative')
# 모델 설정: 'Additive'(가법 모델)시간이 지나도 계절 변동의 폭이 일정할 때 사용합니다.
#result = seasonal_decompose(data['Passengers'], model='additive')

# 시각화
plt.rcParams['figure.figsize'] = [10, 8]
result.plot()
plt.show()