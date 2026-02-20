import seaborn as sns
import koreanize_matplotlib # 한글 폰트 설정을 위한 라이브러리입니다. matplotlib에서 한글이 깨지는 문제를 해결해줍니다.
import matplotlib.pyplot as plt

# **`stripplot()`**은 범주형 데이터의 실제 관측치를 축 위에 점으로 표시하는 그래프입니다. 
# 앞서 배운 `boxplot`이나 `violinplot`이 데이터를 요약해서 보여준다면, 
# `stripplot`은 **데이터 하나하나의 실제 위치**를 그대로 보여주는 것이 특징입니다.
#
# `tips` 데이터셋을 활용한 `stripplot()` 예제
#
# 이 예제에서는 요일별 결제 금액을 점으로 나타내고, 점들이 겹쳐서 안 보이는 것을 방지하기 위해 
# `jitter` 옵션을 사용합니다.
#
#  상세 설명
#
# **`jitter=True`**: `stripplot`의 가장 중요한 옵션입니다. 
#   데이터가 많으면 점들이 일직선상에 겹쳐서 데이터의 양을 가늠하기 어렵습니다. 
#   `jitter`를 주면 가로로 무작위하게 퍼뜨려주어 **데이터의 밀집도**를 훨씬 잘 보여줍니다.

# **`alpha=0.6`**: 점에 투명도를 주면, 점들이 많이 겹치는 구간(데이터 밀도가 높은 곳)은 
#   색이 진하게 나타나 시각적으로 분포를 파악하기 쉬워집니다.
#
# **개별 관측치 확인**: 요약된 통계량이 아니라, 실제 식당에서 결제된 244건의 데이터가 각각 
#   어디에 위치하는지 "날것" 그대로의 데이터를 볼 수 있습니다.

# 1. 데이터 로드
tips = sns.load_dataset("tips")

# 2. stripplot 시각화
plt.figure(figsize=(10, 6))
sns.stripplot(
    data=tips, 
    x="day",             # X축: 요일
    y="total_bill",      # Y축: 결제 금액
    hue="day",           # 색상: 요일별로 구분
    jitter=True,         # 중요: 점들이 겹치지 않게 옆으로 살짝 퍼뜨림
    alpha=0.6,           # 투명도: 점이 겹치는 정도를 확인하기 위함
    size=6,              # 점의 크기
    palette="deep",
    order=["Thur", "Fri", "Sat", "Sun"]
)

# 3. 그래프 꾸미기
plt.title("요일별 결제 금액의 개별 관측치 (Strip Plot)")
plt.xlabel("요일 (Day)")
plt.ylabel("총 결제 금액 ($)")
plt.show()