import pandas as pd
import numpy as np

dates = pd.date_range(
    "2026-01-01",    # 시작 날짜: 2026년 1월 1일부터 시작
    periods=7,       # 생성 개수: 총 7개의 날짜를 생성
    freq="D"         # 주기(Frequency): 'D'는 일(Day) 단위를 의미 (매일매일)
)
# 결과: 2026-01-01, 2026-01-02, ..., 2026-01-07 까지의 인덱스 생성

# 2. 실제 데이터(수치) 생성
# np.random.randint는 정해진 범위 내에서 무작위 정수를 생성합니다.
values = np.random.randint(
    10,              # 최소값: 10부터 시작 (포함)
    50,              # 최대값: 50 직전까지 (49까지 포함)
    size=7           # 개수: 위에서 만든 날짜 개수와 동일하게 7개 생성
)
# 결과: [24, 45, 12, 38, ...] 같은 형태의 7개 정수 배열 생성

# 3. Pandas Series 객체 생성
# 데이터(values)와 인덱스(index)를 합쳐서 하나의 시계열 데이터를 완성합니다.
ts = pd.Series(
    values,          # Series의 본체 데이터 (무작위 정수 7개)
    index=dates      # 각 데이터에 대응하는 날짜 인덱스 부여
)

# 생성된 시계열 데이터 확인
print(ts)


# 날짜 기반 슬라이싱
# 특정 날짜
value = ts['2026-01-03']
print(f"\n2026-01-03의 값은 == {value}\n")
print(f"일반 색인으로 값 얻기 == {ts.iloc[2]}\n")
print(f"날짜 색인으로 값 얻기 == {ts.loc['2026-01-03']}\n")

# 날짜 범위
# --- 1. 특정 기간 데이터 추출 (Slicing) ---
# Pandas Series에서는 날짜 문자열을 사용하여 시작:끝 범위를 지정할 수 있습니다.
# "2026-01-02"부터 "2026-01-05"까지의 데이터를 잘라냅니다. (시작과 끝 날짜 모두 포함)
print(ts["2026-01-02":"2026-01-05"])

# --- 2. 추출된 데이터의 인덱스를 활용한 반복문 (Looping) ---
# ts["2026-01-02":"2026-01-05"].index는 추출된 범위의 '날짜(DatetimeIndex)'들만 모아둔 것입니다.
for d in ts["2026-01-02":"2026-01-05"].index:
    # d는 현재 순회 중인 '날짜 객체(Timestamp)'입니다.
    # ts[d]는 원본 Series에서 해당 날짜(d)에 매칭되는 '값(Value)'을 가져옵니다.
    print(f"{d} -> {ts[d]}")
    print('-' * 30)


# 1. 인덱스에서 '연도(Year)' 정보만 추출
# ts.index가 DatetimeIndex일 때만 사용 가능합니다.
# 모든 행의 연도 데이터를 정수(int) 형태의 배열로 반환합니다.
print(ts.index.year) 
# 결과 예시: Int64Index([2026, 2026, ..., 2026], dtype='int64')

# 2. 인덱스에서 '월(Month)' 정보만 추출
# 1월은 1, 12월은 12로 표시되는 정수 데이터를 반환합니다.
print(ts.index.month)
# 결과 예시: Int64Index([1, 1, ..., 1], dtype='int64') (모두 1월이므로)

# 3. 인덱스에서 '일(Day)' 정보만 추출
# 해당 날짜의 일자 데이터를 정수 형태로 반환합니다.
print(ts.index.day)
# 결과 예시: Int64Index([1, 2, 3, 4, 5, 6, 7], dtype='int64')

# 4. 인덱스에서 '요일(Weekday)' 정보만 추출
# --- 시계열 리샘플링 및 주간 평균 계산 ---

# 1. ts.resample("W"): 데이터를 '주(Weekly)' 단위로 그룹화합니다.
# "W"는 일요일을 기준으로 한 주를 묶는 옵션입니다.
# 이 단계까지만 실행하면 그룹화된 상태(Resampler 객체)이며, 실제 값은 계산되지 않습니다.
resampled_data = ts.resample("W")

# 2. .mean(): 그룹화된 각 주차 데이터들의 '산술 평균'을 계산합니다.
# 예를 들어, 한 주에 포함된 7일치 데이터의 합을 7로 나눈 값이 해당 주의 대표값이 됩니다.
weekly_mean = resampled_data.mean()

# 3. 결과 출력
# 인덱스는 각 주의 마지막 날(보통 일요일)로 표시되며, 값은 그 주의 평균값이 출력됩니다.
for d in weekly_mean.index:
    print(f"{d} -> {weekly_mean[d]}")
    print('-' * 30)
print(weekly_mean)


# --- 3일 이동 평균(Rolling Mean) 계산 ---

# 1. ts.rolling(window=3): 
# 현재 데이터를 기준으로 '윈도우(창문)'라는 크기 3의 구간을 설정합니다.
# 즉, [현재 행, 바로 직전 행, 그 전 행] 이렇게 3개씩 묶어서 볼 준비를 합니다.
rolling_obj = ts.rolling(window=3)

# 2. .mean():
# 위에서 설정한 윈도우(3개 데이터) 안에 들어온 값들의 '평균'을 계산합니다.
# 이 과정을 한 칸씩 아래로 내려가며 반복하기 때문에 '이동' 평균이라고 부릅니다.
rolling_avg = rolling_obj.mean()

# 3. 결과 출력
print(rolling_avg)