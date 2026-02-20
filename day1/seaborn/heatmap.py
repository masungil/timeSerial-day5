import seaborn as sns
import koreanize_matplotlib # 한글 폰트 설정을 위한 라이브러리입니다. matplotlib에서 한글이 깨지는 문제를 해결해줍니다.
import matplotlib.pyplot as plt

# `heatmap()`은 데이터의 수치 크기를 색상의 명도와 채도로 변환하여 시각화하는 그래프입니다. 
# 주로 변수 간의 상관관계(Correlation) 분석이나 시계열 데이터의 월별/연도별 변화를 한눈에 파악할 때 사용됩니다.
# 
# `tips` 데이터셋을 활용하여 수치형 변수들 간의 상관계수를 시각화하는 예제
#
# 1. `tips` 데이터셋 변수 간 상관관계 히트맵
#
# 이 예제는 식사 비용, 팁, 인원수 사이의 밀접한 관계를 수치와 색상으로 보여줍니다.
#
# 2. 상세 설명
#
# `corr()`: 데이터프레임 내 변수들 사이의 상관계수를 계산합니다. 
#    1에 가까울수록 강한 양의 상관관계를 의미합니다.
#
# `annot=True`: 히트맵은 색상만으로도 직관적이지만, 실제 수치를 함께 적어주면 훨씬 
#    정확한 분석이 가능합니다.
#
# `cmap="coolwarm"`: 시각화 목적에 맞는 색상 선택이 중요합니다. 
#    상관계수 분석에는 보통 중간값(0)을 기준으로 색이 변하는 `coolwarm`이나 `RdBu` 
#    팔레트를 선호합니다.
#
# 데이터 재구조화 필요성: `heatmap()`은 기본적으로 행렬 형태의 데이터를 요구합니다. 
#    따라서 단순 데이터프레임을 넣기보다 위 예제처럼 `corr()`을 사용하거나 
#    `pivot_table()`을 이용해 데이터를 가공한 뒤 그려야 합니다.
#
# 3. 히트맵 분석 인사이트
#
# Total Bill vs Tip: 보통 이 두 변수 사이의 상관계수가 높게 나타납니다. 
#    즉, "결제 금액이 클수록 팁도 많이 준다"는 가설을 데이터로 증명할 수 있습니다.
#
# 색상의 농도: 가장 짙은 빨간색 칸을 찾아 어떤 변수들이 서로 가장 큰 영향을 
#   주고받는지 즉시 파악할 수 있습니다.

# 1. 데이터 로드
tips = sns.load_dataset("tips")

# 2. 수치형 데이터만 선택하여 상관계수 행렬 계산
# numeric_only=True는 최신 pandas 버전에서 수치형 데이터만 골라내기 위해 사용합니다.
corr = tips.corr(numeric_only=True)

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