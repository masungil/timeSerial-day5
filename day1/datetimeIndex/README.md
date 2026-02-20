# 1️⃣ Index(인덱스)란 무엇인가?

## ✅ Index의 기본 개념

**Index는 데이터의 “기준 축(reference axis)”** 입니다.

* 각 데이터가 **무엇을 기준으로 정렬되고 식별되는지**를 나타냄
* Pandas에서는 **행(Row)을 식별하는 역할**
* 시계열 데이터에서는 **시간(Time)이 Index가 됨**

```text
Index  →  값
시간   →  관측값
```

---

## 일반 데이터 vs 시계열 데이터

### 일반 데이터 (Index = 단순 번호)

| index | value |
| ----- | ----- |
| 0     | 100   |
| 1     | 120   |

→ 순서만 있을 뿐, **시간 의미 없음**

---

### 시계열 데이터 (Index = 시간)

| time       | value |
| ---------- | ----- |
| 2024-01-01 | 100   |
| 2024-01-02 | 120   |

→ **시간의 흐름 자체가 의미**

---

# 2️⃣ 시계열 데이터에서 “시간 인덱스”가 중요한 이유

### 🔑 핵심 이유 5가지

1. **정렬 기준**

   * 시간 순서가 보장됨
2. **슬라이싱**

   * 특정 날짜/시간 구간 조회 가능
3. **리샘플링**

   * 일 → 월, 분 → 시간 변환
4. **시계열 연산**

   * 이동 평균, 누적 합
5. **모델 입력 기준**

   * LSTM, ARIMA는 시간 순서 필수

---

# 3️⃣ Pandas DatetimeIndex란?

## ✅ DatetimeIndex 정의

`DatetimeIndex`는
👉 **날짜/시간을 전문적으로 처리하는 Pandas의 인덱스 타입**

```python
type(ts.index)
# pandas.core.indexes.datetimes.DatetimeIndex
```

---

## 📌 DatetimeIndex가 제공하는 기능

| 기능    | 설명                           |
| ----- | ---------------------------- |
| 날짜 연산 | 하루 더하기, 차이 계산    |
| 시간 추출 | year, month, day, hour       |
| 부분 선택 | '2024-01', '2024-01-15'      |
| 리샘플링  | resample('M'), resample('H') |
| 타임존   | tz_localize, tz_convert      |

---

# 4️⃣ DatetimeIndex 생성 방법 (가장 중요)

---

## 🔹 방법 1: `pd.date_range()` (가장 많이 사용)

```python
import pandas as pd

dates = pd.date_range(
    start="2026-01-01",   # 시작 날짜
    periods=5,            # 생성할 날짜의 개수
    freq="d"              # 간격 (d: 일 단위)
)

print(dates)
```

### 결과

```text
DatetimeIndex(['2024-01-01', '2024-01-02', '2024-01-03',
               '2024-01-04', '2024-01-05'],
              dtype='datetime64[ns]', freq='D')
```
---

freq 인자의 다양한 활용 (핵심 팁)

freq 값만 바꾸면 다양한 주기의 시계열 데이터를 순식간에 만들 수 있습니다.


|설정값|의미|결과 예시 (시작일: 1/1)|
|---|---|---|
|"d"|일 단위 (Day)|"1/1, 1/2, 1/3..."|
|"b"|평일 단위 (Business Day)|토/일 제외하고 생성|
|"h"|시간 단위 (Hour)|"1/1 00:00, 1/1 01:00..."|
|"me"|월말 단위 (Month End)|"1/31, 2/28, 3/31..."|
|"w"|주 단위 (Week)|일요일마다 생성|

---

## 🔹 방법 2: to_datetime() : 문자열 → DatetimeIndex 변환

 
```python
dates = pd.to_datetime([
    "2024-01-01",
    "2024-01-02",
    "2024-01-03"
])
```

---

## 🔹 방법 3: DataFrame에서 변환

```python
df["date"] = pd.to_datetime(df["date"])
df.set_index("date", inplace=True)
```

---

# 5️⃣ DatetimeIndex를 가진 시계열 데이터 생성 예제

## 📊 예제 1: 기본 시계열 데이터

```python
import numpy as np

dates = pd.date_range("2024-01-01", periods=7, freq="D")
values = np.random.randint(10, 50, size=7)

ts = pd.Series(values, index=dates)
print(ts)
```

---

## 📈 시각화

```python
ts.plot(title="Time Series with DatetimeIndex")
```

---

# 6️⃣ DatetimeIndex 핵심 기능 실습 예제

---

## 🔹 1️⃣ 날짜 기반 슬라이싱 (엄청 중요)

```python
# 특정 날짜
ts["2024-01-03"]

# 날짜 범위
ts["2024-01-02":"2024-01-05"]
```

✔ 일반 인덱스에서는 불가능한 기능

---

## 🔹 2️⃣ 연/월/일 정보 추출

```python
ts.index.year
ts.index.month
ts.index.day
```

---

## 🔹 3️⃣ 리샘플링 (시간 단위 변경)

### 일 → 주 평균

```python
weekly_mean = ts.resample("W").mean()
print(weekly_mean)
```

---

## 🔹 4️⃣ 이동 평균 계산

```python
ts.rolling(window=3).mean()
```

---

# 7️⃣ DatetimeIndex 없을 때 vs 있을 때 차이

---

## ❌ DatetimeIndex 없음

```python
df = pd.DataFrame({
    "date": ["2024-01-01", "2024-01-02"],
    "value": [10, 20]
})
```

* 날짜 연산 ❌
* resample ❌
* 시계열 모델 입력 불가

---

## ⭕ DatetimeIndex 있음

```python
df["date"] = pd.to_datetime(df["date"])
df.set_index("date", inplace=True)
```

* 모든 시계열 기능 가능 ✅

---

# 8️⃣ 실무에서 반드시 기억해야 할 핵심 정리

### ✅ 핵심 문장 3개

1. **시계열 데이터에서 Index = 시간이다**
2. **Pandas 시계열 분석의 출발점은 DatetimeIndex**
3. **DatetimeIndex 없이는 resample, rolling, 모델링이 불가능**

---

# 9️⃣ 실무/교육용 한 줄 정의

> **DatetimeIndex는 시계열 데이터에서 “시간을 기준 축으로 삼아 정렬·연산·분석·모델링을 가능하게 하는 Pandas의 핵심 인덱스 구조”이다.**

---
