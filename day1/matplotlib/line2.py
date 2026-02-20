import koreanize_matplotlib # 한글 폰트 설정을 위한 라이브러리입니다. matplotlib에서 한글이 깨지는 문제를 해결해줍니다.
import matplotlib.pyplot as plt
import numpy as np

# 데이터 준비
# 시각화를 위해서는 X축과 Y축의 데이터 개수가 반드시 일치해야 합니다.
x = np.arange(1, 11) #1부터 10까지의 정수 배열 생성 (X축 공통)
y_line = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] # 소수(Prime Number) 리스트

#그래프가 그려질 그림의 크기를 설정합니다. 가로 8인치, 세로 5인치 크기입니다.
plt.figure(figsize=(8, 5))

#라인 차트를 그립니다. 시계열 데이터나 연속적인 수치 변화를 표현할 때 씁니다
plt.plot(x, y_line, color='blue', marker='o', linestyle='--', linewidth=2)

# 그래프의 제목입니다. 
plt.title('1. 라인차트(경향/추세)')

# X축과 Y축이 레이블을 설정합니다
plt.xlabel('시간')
plt.ylabel('값')

# 배경에 눈금선을 그려줍니다. 투명도는 0.6
plt.grid(True, linestyle=':', alpha=0.6)

# 차트를 출력합니다 
plt.show()