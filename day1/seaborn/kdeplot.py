import seaborn as sns
import koreanize_matplotlib # 한글 폰트 설정을 위한 라이브러리입니다. matplotlib에서 한글이 깨지는 문제를 해결해줍니다.
import matplotlib.pyplot as plt

# kdeplot()(Kernel Density Estimate)은 히스토그램의 거친 막대들을 부드러운 곡선 형태로 연결하여, 
# 데이터가 어디에 얼마나 집중되어 있는지 확률 밀도를 보여주는 그래프입니다.

# flights 데이터셋에 이를 적용하면 연도별로 승객 수의 중심점이 어떻게 이동하고, 
# 분포가 얼마나 넓어지는지를 한눈에 파악할 수 있습니다.

# kdeplot()를 통해 분석할 수 있는 주요 포인트는 다음과 같습니다:
# 중심의 이동 (Trend): 그래프의 가장 높은 봉우리(최빈값)가 왼쪽(낮은 승객 수)에서 오른쪽(높은 승객 수)으로 이동하는 것을 통해 항공 시장의 성장을 확인할 수 있습니다.
# 분포의 확산 (Variance): 과거(보라색) 곡선은 좁고 높지만, 최근(노란색) 곡선은 완만하고 옆으로 넓게 퍼집니다. 이는 시간이 지날수록 성수기와 비성수기의 승객 차이가 더 커졌음을 의미합니다.
# 밀집 구간 확인: 특정 승객 수 구간에서 곡선이 솟아오른 정도를 보고, 해당 시기에 승객이 주로 어느 정도 규모로 유지되었는지 파악할 수 있습니다.

# 실무 활용 팁: histplot과의 결합
# 만약 정확한 빈도(막대)와 부드러운 곡선을 동시에 보고 싶다면, 
# 앞서 배운 histplot() 함수에 kde=True 옵션을 추가하는 것만으로도 두 그래프의 장점을 합칠 수 있습니다.

# 1. 데이터 로드
flights = sns.load_dataset("flights")

# 2. KDE 플롯 시각화
plt.figure(figsize=(10, 6))
sns.kdeplot(
    data=flights, 
    x="passengers",      # X축: 탑승객 수
    hue="year",          # 색상: 연도별로 분포 곡선 분리
    fill=True,           # 곡선 아래 영역 채우기
    palette="viridis",   # 색상 팔레트 적용
    alpha=0.4,           # 투명도 조절 (겹치는 구간 확인용)
    linewidth=1.5        # 곡선 굵기
)

# 3. 그래프 꾸미기
plt.title("1949-1960 연도별 항공 탑승객 밀도 분포 (KDE Plot)")
plt.xlabel("탑승객 수 (Passengers)")
plt.ylabel("밀도 (Density)")
plt.show()