import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import locale
# --- 한글 폰트 설정 추가 ---
import platform

# 폰트 설정 (Windows는 'Malgun Gothic', macOS는 'AppleGothic')
if platform.system() == 'Windows':
    plt.rcParams['font.family'] = 'Malgun Gothic'
elif platform.system() == 'Darwin': # macOS
    plt.rcParams['font.family'] = 'AppleGothic'

# 마이너스 기호(-) 깨짐 방지
plt.rcParams['axes.unicode_minus'] = False
# -------------------------

# 2. 날짜 지역 설정 (Locale) 변경
# Windows 환경: "ko_KR" 또는 "Korean"
# macOS/Linux 환경: "ko_KR.UTF-8"
try:
    if platform.system() == 'Windows':
        locale.setlocale(locale.LC_ALL, 'Korean_Korea.949')
    else:
        locale.setlocale(locale.LC_ALL, 'ko_KR.UTF-8')
except locale.Error:
    print("설정하려는 로케일이 시스템에 설치되어 있지 않습니다.")


# 2. CSV 파일 로딩
df = pd.read_csv('./data/samsung_20251001_20260126.csv')

# 2. 날짜 변환 및 인덱스 설정 (컬럼명 확인 필수)
# 'Date' 컬럼이 없다면 '날짜' 등으로 수정
date_col = 'Date' if 'Date' in df.columns else df.columns[0]
df[date_col] = pd.to_datetime(df[date_col])
df.set_index(date_col, inplace=True)

# 3. [핵심] 날짜 기준 오름차순 정렬
# 과거 데이터가 위로, 최신 데이터가 아래로 오게 정렬하여 꼬임을 방지합니다.
df = df.sort_index(ascending=True)

# 4. 시각화
plt.figure(figsize=(12, 5))

# 데이터의 첫 번째 열(주가)을 그립니다.
plt.plot(df.index, df.iloc[:, 0], color='dodgerblue', linewidth=2, label="종가")

# 5. [중요] Y축 범위 명시적 설정
# 기본적으로 matplotlib은 낮은 값이 아래에 오지만, 
plt.gca().invert_yaxis() # 만약 현재 뒤집혀 있다면 이 줄을 삭제하세요.
y_min = float(df.iloc[:, 0].min()) * 0.95
y_max = float(df.iloc[:, 0].max()) * 1.05
plt.gca().set_ylim(y_min, y_max)

# 축 포맷 및 레이블
plt.title("삼성전자 주가 추이", fontsize=14)
plt.ylabel("가격 (원)")
plt.xlabel("날짜")
plt.grid(True, linestyle=':', alpha=1)

# X축 날짜 가독성 높이기
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m월-%d일'))

plt.show()
