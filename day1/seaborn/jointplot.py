import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt

# `jointplot()`은 두 수치형 변수 사이의 관계(산점도)와 각 변수별 분포(히스토그램/KDE)를 한 화면에 동시에 
# 보여주는 매우 효율적인 도구입니다.
#
# `pairplot()`이 전체적인 관계를 훑는 용도라면, `jointplot()`은 특정 두 변수의 관계를 집중적으로 
# 파악할 때 사용합니다.
#
# 이 코드는 총 결제 금액(`total_bill`)과 팁(`tip`) 사이의 관계를 시각화합니다.
#
# 결과 분석 설명
#
# 중앙 그래프 (Joint Plot): 두 변수(`total_bill`, `tip`)의 산점도를 보여줍니다. 
#    결제 금액이 커질수록 팁이 늘어나는 경향을 확인할 수 있습니다.
# 상단/우측 그래프 (Marginal Plot): 각 축에 해당하는 변수의 분포를 보여줍니다. 
#    `total_bill`이 어떤 범위에 많이 몰려 있는지, `tip`의 분포는 어떠한지 개별적으로도 파악이 가능합니다.
# `kind` 파라미터 활용:
# `kind="reg"`: 선형 회귀선과 신뢰구간을 추가합니다.
# `kind="kde"`: 점 대신 등고선 형태의 밀도 그래프를 그립니다.
# `kind="hex"`: 데이터가 너무 많을 때 육각형 벌집 모양으로 밀도를 표현합니다.


# 1. 데이터 로드
tips = sns.load_dataset("tips")

# 2. jointplot 시각화
# kind="reg"를 사용하면 산점도 위에 회귀선(Regression line)을 그려줍니다.
g = sns.jointplot(
    data=tips, 
    x="total_bill", 
    y="tip", 
    hue="time",          # 시간대(Lunch/Dinner)별 색상 구분
    kind="scatter",      # 기본 산점도 형식 (reg, kde, hex 등으로 변경 가능)
    palette="viridis",
    marginal_kws=dict(fill=True) # 주변부 그래프(marginal)를 채우기 설정
)

# 3. 제목 설정 및 여백 조정 (핵심!)
# jointplot은 JointGrid 객체이므로 g.fig.suptitle을 사용합니다.
g.figure.suptitle("총 결제 금액과 팁의 상관관계 분석 (Joint Plot)")

# 제목이 잘리지 않도록 상단 여백 확보
plt.subplots_adjust(top=0.9) 

plt.show()