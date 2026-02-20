import seaborn as sns
import koreanize_matplotlib # 한글 폰트 설정을 위한 라이브러리입니다. matplotlib에서 한글이 깨지는 문제를 해결해줍니다.
import matplotlib.pyplot as plt

#  `clustermap()`은 앞서 배운 `heatmap()`에 계층적 클러스터링(Hierarchical Clustering) 기능을
#  더한 고성능 시각화 도구입니다.
#
# 단순히 수치를 색상으로 보여주는 것에 그치지 않고, 비슷한 패턴을 가진 행(Row)과 열(Column)을 
# 유사도에 따라 자동으로 묶어(Clustering) 데이터 내의 숨겨진 구조를 찾아내 줍니다.
#
# 1. `tips` 데이터셋을 활용한 `clustermap()` 예제 
#
# `tips` 데이터셋의 수치형 변수(결제 금액, 팁, 인원수) 사이의 관계를 클러스터링하여 
# 시각화해 한 예제입니다
#
# 2. `clustermap()`의 핵심 구성 요소
#
# 이 그래프가 일반 히트맵과 다른 가장 큰 특징은 그래프 외곽에 그려진 선(Dendrogram)입니다.
#
# 덴드로그램 (Dendrogram): 그래프 위쪽과 왼쪽에 그려진 나뭇가지 모양의 선입니다. 
#    선이 연결된 지점이 낮을수록 두 변수(혹은 행)가 매우 유사한 패턴을 보인다는 뜻입니다.
#
# 자동 재정렬: 유사한 변수들끼리 이웃하도록 행과 열의 순서를 자동으로 바꿉니다. 
#    일반 히트맵에서는 변수 순서가 고정되어 있지만, `clustermap`에서는 데이터의 성격에 
#    따라 순서가 재배치됩니다.
#
# 패턴 발견: 어떤 변수 그룹이 서로 묶여 있는지 확인하여, 데이터 내에 존재하는 하위 그룹이나 
#    특징적인 군집을 찾아낼 수 있습니다.


# 1. 데이터 로드
tips = sns.load_dataset("tips")

# 2. 수치형 데이터 간의 상관계수 행렬 계산
corr = tips.corr(numeric_only=True)

# 3. clustermap 실행
# standard_scale=1 옵션을 주면 데이터를 0~1 사이로 정규화하여 비교가 쉬워집니다.
g = sns.clustermap(
    data=corr, 
    annot=True,          # 수치 표시
    fmt=".2f",           # 소수점 자리수
    cmap="mako",         # 색상 팔레트
    figsize=(10, 8),      # 그래프 크기
    linewidths=0.3,      # 칸 사이 간격
    dendrogram_ratio=(0.1, 0.1), # 덴드로그램(가지 모양 선)이 차지하는 비중
    cbar_pos=(0.02, 0.8, 0.03, 0.15) # 컬러바 위치를 살짝 옮겨 공간 확보
)

# 4. 제목 설정 (clustermap은 객체 구조가 달라 제목 설정 방식이 조금 다릅니다)
g.figure.suptitle("Tips 데이터 변수 간 계층적 클러스터링 히트맵")
# 상단 여백을 강제로 만들어 제목이 잘리지 않게 합니다.
plt.subplots_adjust(top=0.92)
plt.show()