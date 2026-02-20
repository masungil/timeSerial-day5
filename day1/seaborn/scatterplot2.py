import seaborn as sns
import pandas as pd
import koreanize_matplotlib # 한글 폰트 설정을 위한 라이브러리입니다. matplotlib에서 한글이 깨지는 문제를 해결해줍니다.
import matplotlib.pyplot as plt

# 1. 데이터 준비
# tips 데이터셋 로드
tips = sns.load_dataset("tips")
tips.to_csv("tips.csv", index=False)  # tips 데이터셋을 CSV 파일로 저장

# 2. 스캐터플롯 실행 (핵심 분석 구간)
plt.figure(figsize=(8, 5))
sns.scatterplot(
    data=tips, 
    x="total_bill",    # x축: 식사 금액
    y="tip",           # y축: 팁 금액
    hue="day",         # 1단계: 요일별 색상 구분
    style="time",      # 2단계: 시간대별 마커 모양 구분    
    size="size",       # 3단계: 인원수에 따른 점 크기 조절
    palette="viridis", # 색상 팔레트
    alpha=0.7          # 투명도 설정 
)

# 3. 부가 설정
plt.title("식사 금액과 팁의 관계 분석 (요일/시간/인원수 포함)")
plt.legend(bbox_to_anchor=(1.01, 1), loc=2) # 범례를 그래프 밖으로 이동
plt.show()

