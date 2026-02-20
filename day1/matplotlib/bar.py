import koreanize_matplotlib # 한글 폰트 설정을 위한 라이브러리입니다. matplotlib에서 한글이 깨지는 문제를 해결해줍니다.
import matplotlib.pyplot as plt
import numpy as np

# 데이터 준비
# 시각화를 위해서는 X축과 Y축의 데이터 개수가 반드시 일치해야 합니다.
x = np.arange(1, 11) #1부터 10까지의 정수 배열 생성 (X축 공통)
y_bar = [5, 7, 3, 8, 4, 6, 9, 2, 5, 8] # 막대용 임의 데이터

#그래프가 그려질 그림의 크기를 설정합니다. 가로 8인치, 세로 5인치 크기입니다.
plt.figure(figsize=(8, 5))

# 막대 차트를 그립니다. 항목 간의 수량을 비교할 때 가장 효과적입니다.
plt.bar(x, y_bar, color='salmon', edgecolor='black')

#그래프의 제목입니다.
plt.title('2. 막대 차트 (비교/대조)')

# X축과 Y축이 레이블을 설정합니다
plt.xlabel('종류')
plt.ylabel('갯수')

# 차트를 출력합니다 
plt.show()

