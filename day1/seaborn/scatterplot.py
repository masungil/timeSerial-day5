import seaborn as sns
import koreanize_matplotlib # 한글 폰트 설정을 위한 라이브러리입니다. matplotlib에서 한글이 깨지는 문제를 해결해줍니다.
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression # 회귀 모델 import

# 1. 데이터 로드 (연도별, 월별 항공 탑승객 데이터)
# 1949년부터 1960년까지의 월별 항공 탑승객 수가 기록된 시계열 데이터셋입니다.
flights = sns.load_dataset("flights")

# 2. 회귀선 모델 학습을 위한 데이터 준비
# 그냥 'year' 자체를 숫자로 사용해도 됩니다.
X = flights[['year']] # 독립 변수: 연도 (2차원 배열 필요)
Y = flights['passengers'] # 종속 변수: 탑승객 수

# 선형 회귀 모델 생성 및 학습
model = LinearRegression() # 모델 생성
model.fit(X, Y) # 학습: 데이터에 가장 적합한 직선의 기울기와 절편을 찾음

# 학습된 모델로 예측값 생성 (추세선 그리기 위함)
# 예측할 X값은 기존 'year' 데이터의 범위 내에서 생성
X_pred = np.array([[year] for year in sorted(flights['year'].unique())])
Y_pred = model.predict(X_pred)

# 3. 그래프 그리기
plt.figure(figsize=(12, 7))

# 3-1. 산점도 (개별 데이터 포인트)
sns.scatterplot(
    data=flights, 
    x="year",            # X축: 연도
    y="passengers",      # Y축: 탑승객 수
    hue="month",         # 1단계: 월별 색상 구분
    size="passengers",   # 2단계: 수치에 따른 점 크기 조절, 탑승객이 많을수록 점이 커짐
    palette="ch:s=-.2,r=.6", # 색상 팔레트, 시각적 세련미를 위한 색상 팔레트
                             # 단순한 원색이 아니라 연속적인 색상 변화를 주어 시간의 흐름을 더 자연스럽게 표현합니다.
                             # 'cubehelix' 팔레트 시스템을 사용하여 색상이 점차 변화하도록 설정
                             # palette="viridis": 가장 대중적인 데이터 시각화용 팔레트 (노랑-초록-보라)
                             # palette="rocket": 어두운 빨강에서 밝은 분홍색으로 (열정적인 느낌)
                             # palette="flare": 부드러운 오렌지/분홍 계열
    alpha=0.7,          # 점들이 겹칠 때 뭉쳐 보이지 않게 투명도 설정
    legend='full'       # 모든 범례 표시
)

# 3-2. 추세선 (회귀선) 추가
# Matplotlib의 plot 함수를 직접 사용하여 회귀선을 그립니다.
plt.plot(X_pred, Y_pred, color='red', linestyle='-', linewidth=2, label='탑승객 증가 추세선')


# 4. 그래프 꾸미기
plt.title("연도별 항공기 탑승객 변화 추이 및 증가 추세선")
plt.xlabel("연도 (Year)")
plt.ylabel("탑승객 수 (Passengers)")
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left') # 범례 위치 조정
plt.grid(True, linestyle='--', alpha=0.5)
plt.show()

# 출력결과 설명 : 
# 상관관계: 연도와 탑승객 수는 매우 강한 양(+)의 상관관계가 있습니다.
# 계절성(Seasonality): 점들이 일직선상에 있지 않고 위아래로 퍼져 있는 이유는 월별(휴가철 등) 편차가 존재하기 때문입니다.
# 예측 가능성: 빨간 추세선을 오른쪽으로 연장하면 미래(예: 1961년)의 대략적인 탑승객 수도 예측해 볼 수 있습니다.

