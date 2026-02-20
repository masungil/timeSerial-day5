import koreanize_matplotlib # 한글 폰트 설정을 위한 라이브러리입니다. matplotlib에서 한글이 깨지는 문제를 해결해줍니다.
import matplotlib.pyplot as plt
import numpy as np

# 1. 데이터 준비
# 시각화를 위해서는 X축과 Y축의 데이터 개수가 반드시 일치해야 합니다.
x = np.arange(1, 11) #1부터 10까지의 정수 배열 생성 (X축 공통)
y_scatter = np.random.randint(1, 30, 10) # 1~30 사이의 랜덤 정수 10개 생성는 모두 10개로 맞춰져 있습니다.

#그래프가 그려질 그림의 크기를 설정합니다. 가로 8인치, 세로 5인치 크기입니다.
plt.figure(figsize=(8, 5))

# 산점도를 그립니다. 두 변수 사이의 상관관계나 분포를 파악할 때 씁니다.
plt.scatter(x, y_scatter, color='green', s=100, alpha=0.7, edgecolors='white')

# 그래프의 제목입니다. 
plt.title('3. 산점도 차트 (상관관계)')

# X축과 Y축이 레이블을 설정합니다
plt.xlabel('변수 X')
plt.ylabel('변수 Y')

# 차트를 출력합니다 
plt.show()