import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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


# 데이터 생성 코드 시작 
# 재현 가능성을 위해 시드 고정
np.random.seed(42)

# 날짜 생성 (영업일 기준)
dates = pd.date_range(start="2026-01-01", periods=100, freq="B")

# 주가 변동 (랜덤 워크)
price_changes = np.random.normal(loc=0.2, scale=1.5, size=len(dates))
stock_price = 100 + np.cumsum(price_changes)

stock_ts = pd.Series(stock_price, index=dates, name="주식 가격")
# 데이터 생성 코드 끝 
 
# 시각화
stock_ts.plot(figsize=(10, 4), title="주식가격 시계열")
plt.ylabel("가격")
plt.show()