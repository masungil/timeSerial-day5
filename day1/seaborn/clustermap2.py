import seaborn as sns
import koreanize_matplotlib # 한글 폰트 설정을 위한 라이브러리입니다. matplotlib에서 한글이 깨지는 문제를 해결해줍니다.
import matplotlib.pyplot as plt

# flights 시계열 데이터 활용 (진면목 확인)
# clustermap의 진정한 강력함은 시계열 데이터에서 **패턴이 비슷한 월(Month)이나 연도(Year)**를 묶어볼 때 나타납니다.
# 이 그래프를 그리면 여름 휴가철인 7월과 8월이 하나의 그룹으로 묶이는 것을 볼 수 있습니다. 
# 이는 두 달의 승객 수 변화 패턴이 매우 유사함을 의미합니다. 
# 또한, 연도별로도 항공 산업이 급격히 팽창했던 특정 구간끼리 묶이는 것을 확인할 수 있습니다.


# 1. 데이터 로드
flights = sns.load_dataset("flights")
flights_pivot = flights.pivot(index="month", columns="year", values="passengers")

# 3. clustermap 실행
# standard_scale=1 옵션을 주면 데이터를 0~1 사이로 정규화하여 비교가 쉬워집니다.
g = sns.clustermap(
    data=flights_pivot, 
    annot=True,          # 수치 표시
    fmt=".2f",           # 소수점 자리수
    cmap="mako",         # 색상 팔레트
    figsize=(10, 8),      # 그래프 크기
    linewidths=0.3,      # 칸 사이 간격
    dendrogram_ratio=(0.1, 0.1), # 덴드로그램(가지 모양 선)이 차지하는 비중
    cbar_pos=(0.02, 0.8, 0.03, 0.15) # 컬러바 위치를 살짝 옮겨 공간 확보
)

# 4. 제목 설정 (clustermap은 객체 구조가 달라 제목 설정 방식이 조금 다릅니다)
g.figure.suptitle("연도별/월별 항공 탑승객 클러스터맵 분석")
# 상단 여백을 강제로 만들어 제목이 잘리지 않게 합니다.
plt.subplots_adjust(top=0.92)
plt.show()