import pandas as pd

# 1. 데이터 생성 (날짜 문자열 리스트)
dates = ['2025-01-01', '2025-01-02', '2025-01-03', '2025-01-07']
data = [100, 150, 120, 200]

# 2. DatetimeIndex로 변환하며 데이터프레임 생성
df = pd.DataFrame(data, index=pd.to_datetime(dates), columns=['Price'])

print("--- 생성된 데이터프레임 ---")
print(df)

# 3. DatetimeIndex의 강력한 기능들
print(f"\n인덱스의 연도 정보: {df.index.year.tolist()}")
print(f"인덱스의 요일 정보: {df.index.day_name().tolist()}")

# 4. 특정 기간 슬라이싱 (1월 1일부터 2일까지)
print("\n--- 1월 2일까지의 데이터 ---")
print(df.loc['2025-01-01':'2025-01-02'])
