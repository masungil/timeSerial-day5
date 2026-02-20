import seaborn as sns
import koreanize_matplotlib # 한글 폰트 설정을 위한 라이브러리입니다. matplotlib에서 한글이 깨지는 문제를 해결해줍니다.
import matplotlib.pyplot as plt

# lineplot() 분석으로 알 수 있는 것
#1. 성장 추세 (Trend): 모든 월별 선이 오른쪽 위로 향하고 있으므로, 항공 산업이 매년 꾸준히 성장했음을 알 수 있습니다.
#2. 계절 변동 (Seasonality): 매년 여름(7~8월) 즈음에 선들이 위로 솟구치는 '산' 모양이 반복됩니다. 이는 항공 승객 수에 강한 계절적 패턴이 있음을 시사합니다.
#3. 변동폭의 확대: 연도가 지날수록 선들 사이의 간격이 점점 벌어집니다. 이는 시간이 흐를수록 성수기와 비성수기의 승객 수 차이가 더 극명해졌음을 의미합니다.

# 1. 데이터 로드
flights = sns.load_dataset("flights")

# 2. 라인플롯 시각화
plt.figure(figsize=(12, 6))
sns.lineplot(
    data=flights, 
    x="year",           # X축: 시간(연도)
    y="passengers",     # Y축: 수치(탑승객 수)
    hue="month",        # 색상: 월별로 선을 분리하여 계절성 비교
    style="month",      # 스타일: 월별로 선의 모양(실선, 점선 등) 차별화
    markers=True,       # 마커: 각 데이터 포인트에 점 표시
    dashes=False        # 모든 선을 실선으로 유지 (선택 사항)
)

# 3. 그래프 꾸미기
plt.title("1949-1960 월별 항공 탑승객 변화 추이 (Line Plot)")
plt.xlabel("연도 (Year)")
plt.ylabel("탑승객 수 (Passengers)")
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left')
plt.grid(True, linestyle='--', alpha=0.5)
plt.show()