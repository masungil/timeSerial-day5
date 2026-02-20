import pandas as pd
import numpy as np

# [1] 원본 데이터 로딩
# - 데이터 소스: UCI Machine Learning Repository의 가계 전력 소비 데이터
# - sep=';': 데이터가 세미콜론(;)으로 구분되어 있음
# - low_memory=False: 대용량 데이터 처리 시 데이터 타입 추론으로 인한 메모리 경고 방지
# - na_values=['?']: 원본 데이터에서 결측치가 '?'로 표시되어 있으므로 이를 NaN으로 처리
file_path = './data/household_power_consumption.txt'

print("데이터를 로딩 중입니다... 잠시만 기다려주세요.")

df = pd.read_csv(file_path, sep=';', 
                 low_memory=False, 
                 na_values=['?'])

# [2] 날짜 및 시간 데이터 통합
# - 'Date'와 'Time' 문자열 컬럼을 합쳐서 하나의 datetime 객체로 변환
# - dayfirst=True: 데이터 형식이 일/월/년 순서인 경우를 처리 (예: 16/12/2006)
df['dt'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], dayfirst=True)

# [3] 인덱스 설정 및 불필요한 컬럼 제거
# - 시간 기반 분석을 위해 통합된 'dt' 컬럼을 인덱스로 설정
df.set_index('dt', inplace=True)
# - 이미 인덱스로 사용된 Date와 Time 컬럼은 메모리 절약을 위해 삭제
df.drop(['Date', 'Time'], axis=1, inplace=True)

# [4] 결측치 처리 및 데이터 타입 변환
# - ffill(): Forward Fill 방식으로, 결측치가 발생하면 바로 이전 시점의 값으로 채움 (시계열 데이터에서 흔히 사용)
# - astype(float): 모든 수치형 데이터를 계산 가능한 float 타입으로 변환
df = df.ffill().astype(float)

# [5] 데이터 재샘플링 (Resampling)
# - 원본은 1분 단위 데이터이지만, 분석의 효율성과 노이즈 제거를 위해 '일(Day)' 단위로 집계
# - .sum(): 하루 동안의 총 전력 사용량 합계를 계산
df_daily = df.resample('D').sum()

# [6] 결과 확인 및 저장
print("\n--- 일일 단위 재샘플링 완료 ---")
print(df_daily.head())
print(f"\n데이터 크기 변환: {df.shape[0]} 행 (분 단위) -> {df_daily.shape[0]} 행 (일 단위)")

# - 전처리가 완료된 데이터를 CSV 형식으로 저장하여 이후 단계에서 활용
df_daily.to_csv('./data/household_daily_usage.csv')