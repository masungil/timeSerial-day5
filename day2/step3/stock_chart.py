import pandas as pd
import koreanize_matplotlib # 한글 폰트 설정을 위한 라이브러리입니다. matplotlib에서 한글이 깨지는 문제를 해결해줍니다.
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import locale
import platform


#  날짜 지역 설정 (Locale) 변경
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
date_col = '날짜'
df[date_col] = pd.to_datetime(df[date_col])
df.set_index(date_col, inplace=True)

# 3. [핵심] 날짜 기준 오름차순 정렬
# 과거 데이터가 위로, 최신 데이터가 아래로 오게 정렬하여 꼬임을 방지합니다.
df = df.sort_index(ascending=True)

# 4. 시각화
plt.figure(figsize=(12, 5))

# 데이터의 첫 번째 열(주가)을 그립니다.
plt.plot(df.index, df.iloc[:, 0], color='dodgerblue', linewidth=2, label="종가")

# 축 포맷 및 레이블
plt.title("삼성전자 주가 추이", fontsize=14)
plt.ylabel("가격 (원)")
plt.xlabel("날짜")
plt.grid(True, linestyle=':', alpha=1)

# X축 날짜 가독성 높이기
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m월-%d일'))

plt.show()
