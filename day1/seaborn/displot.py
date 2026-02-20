import seaborn as sns
import koreanize_matplotlib # 한글 폰트 설정을 위한 라이브러리입니다. matplotlib에서 한글이 깨지는 문제를 해결해줍니다.
import matplotlib.pyplot as plt

#displot()**은 histplot, kdeplot, rugplot 등을 하나로 통합하여 관리하는 
# **상위 인터페이스(Figure-level function)**입니다. 
# relplot이 관계형 그래프를 통합하듯, displot은 분포형 그래프를 통합하며 
# **여러 개의 서브플롯(격자)**을 한꺼번에 그리는 데 매우 강력합니다.


#  `displot()`의 특징 설명
#
# ① 통합 제어 기능
#
#  `displot()`은 한 번의 실행으로 히스토그램(`hist`)과 밀도 곡선(`kde`), 
# 그리고 눈금 표시(`rug`)를 모두 제어할 수 있습니다.
#  코드에서는 `kind="hist"`와 `kde=True`를 조합하여 **"막대 데이터"**와 
# **"흐름 곡선"**을 동시에 보여줍니다.
#
# ② `col` 파라미터를 통한 연도별 분리
#
#  `histplot`에서 `hue="year"`를 썼을 때는 모든 연도가 한 그래프에 겹쳐 보여 복잡했습니다.
#  `displot`에서 **`col="year"`**를 쓰면, 연도마다 개별 그래프가 생성되어 
# **시간이 흐름에 따라 분포(데이터 뭉치)가 오른쪽으로 이동하는 모습**을 영화 
# 프레임처럼 확인할 수 있습니다.
#
# ③ 분포(밀도) 확인의 시각화
#
# 각 서브플롯 내에서 데이터가 몰려 있는 구간(가장 높은 막대)을 확인하여 해당 
# 연도의 평균적인 승객 규모를 파악합니다.
# 오른쪽으로 갈수록(최근 연도일수록) 그래프의 가로축 범위가 넓어지는 것을 통해 
# **성장성**과 **변동성**을 동시에 읽어낼 수 있습니다.


# 1. 데이터 로드
flights = sns.load_dataset("flights")

# 2. displot 실행
# kind="hist"(기본값)를 사용하면서 kde=True를 설정하여 통합 분석
g = sns.displot(
    data=flights,
    x="passengers",
    hue="year",       # 연도별 색상 구분
    col="year",       # 연도별로 그래프를 옆으로 나눔 (서브플롯 생성)
    col_wrap=4,       # 한 줄에 4개씩 배치
    kind="hist",      # 히스토그램 형태
    kde=True,         # 밀도 곡선 추가
    palette="viridis",
    height=3,         # 개별 그래프의 높이
    aspect=1.2        # 개별 그래프의 가로세로 비율
)

# 3. 그래프 꾸미기
g.figure.suptitle("연도별 항공 탑승객 분포 변화 (displot)", y=1.05)
g.set_axis_labels("탑승객 수", "빈도")
plt.show()