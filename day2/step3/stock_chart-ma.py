import pandas as pd
import koreanize_matplotlib # 한글 폰트 설정을 위한 라이브러리입니다. matplotlib에서 한글이 깨지는 문제를 해결해줍니다.
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import locale
import platform

# 날짜 지역 설정 (Locale) 변경
# Windows 환경: "ko_KR" 또는 "Korean"
# macOS/Linux 환경: "ko_KR.UTF-8"
try:
    if platform.system() == 'Windows':
        locale.setlocale(locale.LC_ALL, 'Korean_Korea.949')
    else:
        locale.setlocale(locale.LC_ALL, 'ko_KR.UTF-8')
except locale.Error:
    print("설정하려는 로케일이 시스템에 설치되어 있지 않습니다.")


# 1. 삼성전자 주가 CSV 파일 로딩
file_path = './data/samsung_20251001_20260126.csv'
df = pd.read_csv(file_path)

# 2. 데이터 전처리 (필수 단계)
# 날짜를 datetime 객체로 변환
df['날짜'] = pd.to_datetime(df['날짜'])

# 계산을 위해 날짜를 과거순(오름차순)으로 정렬
df = df.sort_values(by='날짜').reset_index(drop=True)

# 3. 이동평균 계산 (5일, 10일 예시)
df['MA5'] = df['종가'].rolling(window=5).mean()
df['MA20'] = df['종가'].rolling(window=20).mean()

# 4. 결과 시각화
plt.figure(figsize=(12, 6))
plt.plot(df['날짜'], df['종가'], label='종가', color='black', alpha=0.3)
plt.plot(df['날짜'], df['MA5'], label='5일 이동평균', color='blue')
plt.plot(df['날짜'], df['MA20'], label='20일 이동평균', color='red')

plt.title('삼성전자 주가 추이 (5일, 20일 이동평균)')
plt.ylabel("가격 (원)")
plt.xlabel("날짜")
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()

# 최종 가공된 데이터 확인
print(df[['날짜', '종가', 'MA5', 'MA20']].tail())
