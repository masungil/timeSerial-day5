import koreanize_matplotlib # 한글 폰트 설정을 위한 라이브러리입니다. matplotlib에서 한글이 깨지는 문제를 해결해줍니다.
import matplotlib.pyplot as plt
import numpy as np

# 1. 데이터 준비
x = np.arange(1, 11)
y_line = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] # 소수 데이터
y_bar = [5, 7, 3, 8, 4, 6, 9, 2, 5, 8]
y_scatter = np.random.randint(1, 30, 10)

# 2. 그래프 크기 설정 및 서브플롯 생성 (1행 3열)
fig, axes = plt.subplots(1, 3, figsize=(18, 5))


# --- [그래프 1] 라인 차트 (Line Chart) ---
axes[0].plot(x, y_line, color='blue', marker='o', linestyle='--', linewidth=2)
axes[0].set_title('라인차트(경향/추세)')
axes[0].set_xlabel('시간')
axes[0].set_ylabel('값')
axes[0].grid(True, linestyle=':', alpha=0.6)

# --- [그래프 2] 막대 차트 (Bar Chart) ---
axes[1].bar(x, y_bar, color='salmon', edgecolor='black')
axes[1].set_title('막대 차트 (비교/대조)')
axes[1].set_xlabel('종류')
axes[1].set_ylabel('갯수')

# --- [그래프 3] 산점도 (Scatter Plot) ---
axes[2].scatter(x, y_scatter, color='green', s=100, alpha=0.7, edgecolors='white')
axes[2].set_title('산점도 차트 (상관관계)')
axes[2].set_xlabel('변수 X')
axes[2].set_ylabel('변수 Y')

# 전체 레이아웃 조정 및 제목 추가
plt.suptitle('Matplotlib Basic 3-Step Guide', fontsize=20)
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()