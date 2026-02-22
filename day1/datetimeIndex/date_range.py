import pandas as pd

# pd.date_range() 함수를 사용하여 시계열 데이터 생성 
dates = pd.date_range(
    start="2026-01-01",   # 시작 날짜
    periods=5,            # 생성할 날짜의 개수
    freq="d"              # 간격 (d: 일 단위)
)

print(dates)

# 문자열 -> 시계열 데이터 변환 
dates = pd.to_datetime([
    "2026-01-01",
    "2026-01-02",
    "2026-01-03"
])

print(dates)



# 1. 날짜가 문자열(str)인 데이터프레임 생성
df = pd.DataFrame({
    "date": ["2024-01-01", "2024-01-02", "2024-01-03"],
    "value": [10, 20, 15]
})
print(df)

# 2. 문자열 날짜 → datetime 타입으로 변환
df["date"] = pd.to_datetime(df["date"])

# 3. date 컬럼을 Index(시간 인덱스)로 설정
df.set_index("date", inplace=True)

# 위 두 라인(2,3)이 실행되면 df는 **시계열 데이터프레임(Time Series DataFrame)**으로 변환됩니다 



# DatetimeIndex 객체를 출력합니다
print(df)

for d in df:
    for v in d:
        print(f"value -> {v}")
    print()
print("end")


for d in df.index:
    print(f"index -> {d}")

for d in df.index:
    print(f"index -> {df.loc[d, 'value']}")