import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt

# 시계열 데이터인 flights 데이터셋에서 histplot()을 사용하면, 특정 구간(예: 승객 수 200~600명 사이)에 데이터가 얼마나 자주 분포했는지, 혹은 시간이 흐름에 따라 전체적인 승객 규모가 어떻게 이동했는지를 분석할 수 있습니다.
# histplot() 함수를 사용하여 1949년부터 1960년까지의 항공 탑승객 수 분포 변화를 시각화해 봅시다.
# 데이터의 범위 변화: 1949년 근처의 데이터(보라색 계열)는 왼쪽(100~200명 사이)에 몰려 있지만, 1960년 근처의 데이터(노란색 계열)는 오른쪽(400~600명 사이)에 넓게 퍼져 있음을 알 수 있습니다.
# 치우침(Skewness): 시계열 데이터가 성장세에 있다면 히스토그램은 보통 우측으로 꼬리가 긴 형태이거나, 시간이 지날수록 봉우리가 오른쪽으로 이동하는 모습을 보입니다.
# 성장성 확인: kde 곡선의 봉우리가 오른쪽으로 이동하는 것은 항공 산업의 시장 규모 자체가 커졌음을 의미하는 아주 확실한 증거가 됩니다.

# 1. 데이터 로드
flights = sns.load_dataset("flights")

# 2. 히스토그램 시각화
plt.figure(figsize=(10, 6))
sns.histplot(
    data=flights, 
    x="passengers",      # X축: 탑승객 수 (수치형 데이터)
    hue="year",          # 색상: 연도별로 구분하여 분포 변화 관찰
    kde=True,            # (Kernel Density Estimate): 밀도 곡선, 막대그래프 위에 부드러운 선을 그려줍니다. 
                         # 이는 데이터의 전반적인 확률 밀도를 보여주며, 분포의 '모양'을 파악하기 쉽게 해줍니다.
    multiple="stack",    # stack: 연도별 데이터를 겹치지 않고 쌓아서 표현
                         # "dodge"는 막대를 옆으로 나열하고, "fill"은 비율을 보여줍니다.
    palette="viridis",   # 색상 팔레트
    bins=20              # 막대 개수 설정
)

# 3. 그래프 꾸미기
plt.title("1949-1960 항공 탑승객 수 분포 변화 (Histplot)")
plt.xlabel("탑승객 수 (Passengers)")
plt.ylabel("빈도 (Count)")
plt.show()