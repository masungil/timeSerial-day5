import seaborn as sns
import koreanize_matplotlib # 한글 폰트 설정을 위한 라이브러리입니다. matplotlib에서 한글이 깨지는 문제를 해결해줍니다.
import matplotlib.pyplot as plt


# `swarmplot()`은 앞서 보신 `stripplot()`과 유사하지만, 가장 큰 차이점은 데이터 포인트(점)들이 
# 서로 겹치지 않도록 옆으로 펼쳐준다는 것입니다.
#
# 이로 인해 데이터의 실제 개수와 밀도 분포를 벌집 모양처럼 시각적으로 가장 정확하게 
# 파악할 수 있는 범주형 그래프입니다.
#
# `tips` 데이터셋을 활용한 `swarmplot()` 예제
# 이 예제에서는 요일별 결제 금액을 시각화하며, 성별(`sex`)에 따라 점의 색상을 
# 나누어 분포 차이를 분석합니다.
#
# 2. 코드 및 기능 상세 설명
#
# 데이터의 입체적 분포: `stripplot`은 무작위로 점을 뿌리지만, 
#    `swarmplot`은 점들을 알고리즘에 따라 정렬하여 쌓습니다. 점들이 옆으로 많이 퍼진 
#    구간일수록 데이터가 많이 몰려 있는 최빈값 구간임을 직관적으로 알 수 있습니다.
#
# `size` 파라미터의 중요성: `swarmplot`은 점들이 겹치지 않게 배치하기 때문에, 
#    데이터 양에 비해 점의 크기가 너무 크면 그래프 옆으로 점들이 튀어나가거나 
#    "Points have been overlapped"라는 경고 메시지가 뜹니다. 
#    데이터가 많을수록 `size`를 작게 조절해야 합니다.
#
# `hue` 활용: 색상을 구분하면 특정 요일, 특정 금액대에서 남성과 여성 중 누가 더 
#    많이 분포하는지 아주 세밀하게 비교할 수 있습니다.
#
# 3. `stripplot` vs `swarmplot` 비교
#
#|     특 징     |      stripplot()       |      swarmplot()`            |
#| --------------| ---------------------- | -------------------------    |
#| 배치 방식     | 무작위 (Jitter)        | 규칙적 (알고리즘 기반)       |
#| 중복 방지     | 점들이 겹칠 수 있음    | 점들이 절대 겹치지 않음      |
#| 권장 데이터량 | 대용량 데이터에도 적합 | 중소규모 데이터에 적합       |
#|               |                          (너무 많으면 계산 오래 걸림) |
#| 분포 시각화   | 대략적인 밀도 확인     | 정확한 밀도 모양             |   
#|               |                        |    (바이올린 형태) 확인      |


# 1. 데이터 로드
tips = sns.load_dataset("tips")

# 2. swarmplot 시각화
plt.figure(figsize=(10, 6))
sns.swarmplot(
    data=tips, 
    x="day",             # X축: 요일
    y="total_bill",      # Y축: 결제 금액
    hue="sex",           # 색상: 성별로 구분
    palette="Set1",      # 선명한 색상 팔레트
    size=5,              # 점의 크기 (데이터가 많으면 크기를 줄여야 안 겹침)
    order=["Thur", "Fri", "Sat", "Sun"]
)

# 3. 그래프 꾸미기
plt.title("요일 및 성별에 따른 결제 금액 밀집도 (Swarm Plot)")
plt.xlabel("요일 (Day)")
plt.ylabel("총 결제 금액 ($)")
plt.legend(title="성별", loc='upper right')
plt.show()