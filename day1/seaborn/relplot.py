import seaborn as sns
import koreanize_matplotlib # 한글 폰트 설정을 위한 라이브러리입니다. matplotlib에서 한글이 깨지는 문제를 해결해줍니다.
import matplotlib.pyplot as plt

# relplot()은 col 또는 row 파라미터를 사용해 데이터를 여러 개의 서브플롯(격자)으로 자동 분할하여 분석할 수 있습니다.
# relplot()을 사용하여 분기별(Quarter) 항공 탑승객 수 변화를 시각화해 봅시다.
# 전체적인 추세: 모든 분기(1Q~4Q)에서 연도가 지날수록 탑승객이 우상향하고 있음을 확인합니다.
# 분기별 특징: 3분기(Summer) 그래프의 Y축 수치가 다른 분기보다 훨씬 높게 형성되는 것을 통해 여름 휴가철의 압도적인 영향력을 시각적으로 즉시 파악할 수 있습니다.
# 성장 속도 비교: 특정 분기의 선 기울기가 더 가파르다면, 그 시즌의 항공 시장 성장이 더 빠르게 일어났음을 분석할 수 있습니다.

# 1. 데이터 로드 및 전처리 (분기 정보 추가)
flights = sns.load_dataset("flights")

# 월 데이터를 바탕으로 분기(Quarter) 정보 생성 (분석을 풍부하게 하기 위함)
month_to_quarter = {
    'Jan': '1/4', 'Feb': '1/4', 'Mar': '1/4',
    'Apr': '2/4', 'May': '2/4', 'Jun': '2/4',
    'Jul': '3/4', 'Aug': '3/4', 'Sep': '3/4',
    'Oct': '4/4', 'Nov': '4/4', 'Dec': '4/4'
}
flights['분기'] = flights['month'].map(month_to_quarter)

# 2. relplot 실행
g = sns.relplot(
    data=flights,
    x="year", 
    y="passengers",
    hue="month",      # 선의 색상을 월별로 구분
    col="분기",    # 중요: 분기별로 그래프를 옆으로 나눔 (4개의 서브플롯)
    col_wrap=2,       # 한 줄에 그래프 2개씩 배치
    kind="line",      # 선 그래프 형태 지정
    marker="o",       # 데이터 포인트 표시
    palette="viridis",
    facet_kws={'sharey': False} # 각 서브플롯의 Y축 범위를 데이터에 맞게 조정
)

# 3. 그래프 꾸미기
g.fig.suptitle("분기별 항공 탑승객 성장 추세 (relplot)", y=1.05)
g.set_axis_labels("연도", "탑승객 수")
plt.show()