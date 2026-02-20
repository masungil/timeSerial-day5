import seaborn as sns
import koreanize_matplotlib # 한글 폰트 설정을 위한 라이브러리입니다. matplotlib에서 한글이 깨지는 문제를 해결해줍니다.
import matplotlib.pyplot as plt

# `tips` 데이터셋은 요일별, 성별, 흡연 여부 등 **항목별 데이터 개수**가 다르기 때문에 
# `countplot()`의 진면목을 확인하기 훨씬 좋습니다.
#
# `tips` 데이터셋을 활용한 `countplot()` 예제
#
# 아래코드는 식당을 방문한 고객들이 **어떤 요일에 가장 많이 방문했는지** 빈도를 측정합니다.
# `tips` 데이터셋 상세 설명
#
# **`tips` 데이터셋 구조**:
# `total_bill`: 총 결제 금액
# `tip`: 팁 금액
# `sex`: 성별 (Male, Female)
# `day`: 요일 (Thur, Fri, Sat, Sun)
# `time`: 시간대 (Lunch, Dinner) 등
#
# **`x="day"`**: 요일별로 데이터 행(Row)이 몇 개 있는지 세어 막대 높이로 표시합니다. 
# **`hue="sex"`**: 요일별 막대를 다시 '남성'과 '여성'으로 쪼개어 보여줍니다. 
#   이를 통해 "토요일에는 남성 손님이 여성보다 얼마나 더 많이 왔는지" 등을 즉각적으로 비교할 수 있습니다.
# **`order`**: 요일은 시계열 성격이 있으므로 목~일 순서로 보기 좋게 정렬해준 것입니다.
#
# 무엇을 분석할 수 있을까요?
# **최대 빈도 요일**: 보통 토요일(Sat)이나 일요일(Sun)의 막대가 가장 높으므로, 
#   주말에 손님이 가장 많다는 것을 알 수 있습니다.
# **성별 분포**: 특정 요일에 특정 성별의 방문이 두드러지는지 파악하여 타겟 마케팅 전략을 세울 수 있습니다.
# **데이터의 균형**: 목요일과 금요일의 데이터 양이 주말에 비해 적다는 것을 확인하고, 
#   분석 결과가 주말 데이터에 편향될 수 있음을 인지할 수 있습니다.


# 1. 데이터 로드 (tips 데이터셋)
tips = sns.load_dataset("tips")

# 2. countplot 시각화
plt.figure(figsize=(10, 6))
sns.countplot(
    data=tips, 
    x="day",             # X축: 요일 (Thur, Fri, Sat, Sun)
    hue="sex",           # 색상: 성별로 나누어 빈도 계산
    palette="pastel",    # 부드러운 색상 팔레트
    order=["Thur", "Fri", "Sat", "Sun"] # 요일 순서 지정
)

# 3. 그래프 꾸미기
plt.title("요일별 방문 고객 수 (성별 구분)")
plt.xlabel("요일 (Day)")
plt.ylabel("방문 횟수 (Count)")
plt.show()