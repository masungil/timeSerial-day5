import seaborn as sns
import koreanize_matplotlib # 한글 폰트 설정을 위한 라이브러리입니다. matplotlib에서 한글이 깨지는 문제를 해결해줍니다.
import matplotlib.pyplot as plt

# 히트맵은 시계열 데이터의 계절성을 볼 때도 탁월합니다.
# 아래와 같이 그리면 **"매년 여름(7~8월)에 색이 유독 진해지는 현상"**을 통해 항공 
# 승객의 계절적 집중도를 단번에 보여줄 수 있습니다.
# 차트는 2개가 그려지며, 첫 번째는 월별 승객 수의 변화를,
# 두 번째는 년도별 승객 상관관계를 히트맵으로 나타냅니다


# 1. flights 데이터를 연도(index)와 월(columns)로 재구조화
flights = sns.load_dataset("flights")
flights_pivot = flights.pivot(index="month", columns="year", values="passengers")

# 시각화
sns.heatmap(flights_pivot, cmap="YlGnBu", annot=True, fmt="d")

# 2. 수치형 데이터만 선택하여 상관계수 행렬 계산
# numeric_only=True는 최신 pandas 버전에서 수치형 데이터만 골라내기 위해 사용합니다.
corr = flights_pivot.corr(numeric_only=True)

# 3. heatmap 시각화
plt.figure(figsize=(8, 6))
sns.heatmap(
    data=corr, 
    annot=True,          # 중요: 칸 안에 실제 수치(상관계수) 표시
    fmt=".2f",           # 수치 소수점 자리수 설정
    cmap="coolwarm",     # 색상 팔레트 (양의 상관관계는 빨강, 음의 상관관계는 파랑)
    linewidths=0.5,      # 칸 사이의 간격
    cbar=True            # 우측에 색상 막대(Colorbar) 표시
)

# 4. 그래프 꾸미기
plt.title("Tips 데이터셋 수치형 변수 간 상관관계")
plt.show()