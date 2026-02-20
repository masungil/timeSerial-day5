# 단변수 LSTM 모델

단변수(Univariate) LSTM 모델은 과거의 일련의 데이터 흐름(Time Series)을 학습하여 바로 다음 단계의 값을 예측하는 데 매우 강력한 도구입니다.

주로 **주식 가격, 기온 변화, 전력 소모량**처럼 하나의 지표가 시간에 따라 변하는 데이터를 다룰 때 사용합니다.

---

## 1. 단변수 LSTM이 사용되는 상황

단변수 예측은 오직 **'자기 자신의 과거 데이터'** 만을 기반으로 미래를 점칩니다.

* **주가 예측:** 과거 60일간의 종가를 보고 내일의 종가를 예측할 때.
* **센서 데이터 모니터링:** 특정 기계의 온도가 지난 1시간 동안 어떻게 변했는지 보고 5분 뒤 온도를 예측할 때.
* **수요 예측:** 특정 상품의 일일 판매량 추이를 보고 내일의 재고량을 결정할 때.

---

## 2. 데이터 구조의 이해

LSTM에 데이터를 넣기 위해서는 일반적인 리스트 형태를 **'윈도우(Window)'** 형태로 변환해야 합니다. 예를 들어 `[10, 20, 30, 40, 50]`이라는 시계열 데이터가 있고, 3개의 과거 데이터를 본다면 데이터셋은 다음과 같이 구성됩니다.

* **입력(X):** `[10, 20, 30]`, **출력(y):** `40`
* **입력(X):** `[20, 30, 40]`, **출력(y):** `50`

---

## 3. 모델 설계

단변수 LSTM에서 **'모델 설계'** 란, 단순히 코드를 짜는 것을 넘어 **"과거의 데이터를 어떤 시각으로 바라보고, 어떤 구조의 인공지능 뇌를 만들 것인가"** 를 결정하는 과정입니다.

쉽게 비유하자면, 어떤 요리를 할지 결정하고 그에 맞는 주방 도구와 조리 순서를 정하는 것과 같습니다. 모델 설계의 핵심 요소 3가지가 있습니다.

---

### 1. 윈도우 크기(Look-back Window) 결정

가장 먼저 정해야 할 것은 **"과거 몇 개의 데이터를 보고 미래를 예측할 것인가?"** 입니다. 이것을 'Time Steps'라고도 부릅니다.

* **예시 (주가 예측):**
* **설계 A:** "최근 **3일간**의 가격만 볼래." (단기 흐름 강조)
* **설계 B:** "최근 **60일간**의 가격을 볼래." (장기 추세 강조)

* 이 결정에 따라 입력 데이터의 모양(Input Shape)이 결정됩니다.

---

### 2. 레이어 구조(Architecture) 쌓기

LSTM 모델의 '깊이'와 '넓이'를 정하는 단계입니다. 얼마나 복잡한 패턴을 학습할 수 있는지를 결정합니다.

* **은닉 상태 크기 (Units):** LSTM 셀 내부의 메모리 용량입니다. (예: 50개, 100개) 너무 작으면 학습을 못 하고, 너무 크면 과적합(Overfitting)이 발생합니다.
* **층 쌓기 (Stacked LSTM):** 더 복잡한 비선형 관계를 파악하기 위해 LSTM 층을 2단, 3단으로 쌓을 수도 있습니다.
* **출력층 (Dense Layer):** LSTM이 추출한 특징을 모아서 최종적으로 '내일의 가격'이라는 숫자 하나(1)를 내뱉도록 설계합니다.

---

### 3. 컴파일 설정 (학습 전략)

모델이 정답을 틀렸을 때 어떻게 반성하고 고쳐나갈지 규칙을 정하는 것입니다.

* **손실 함수 (Loss Function):** "정답과 예측값이 얼마나 틀렸나?"를 계산하는 척도입니다. 보통 연속된 숫자를 예측하는 단변수 모델에서는 **MSE(평균 제곱 오차)** 를 사용합니다.
* **최적화 함수 (Optimizer):** "오차를 줄이기 위해 모델의 무게(Weight)를 어떻게 수정할까?"를 결정합니다. 가장 대중적으로 성능이 좋은 **Adam**을 주로 선택합니다.

---

## 4. 예 단변수 LSTM 모델 설계 및 구축

'스마트 기기의 2주간 1시간 단위 사용 전력량' 데이터(`power_usage_dataset.csv`)를 바탕으로, **단변수 LSTM 모델을 구축하는 단계별 설계 방법** 입니다.

---

### 0. 사전 작업

작업을 진행하기 전에 power_usage_dataset.csv 파일에 있는 결측치 값 깨끗하게 정리하고 LSTM 모델을 진행하는 것이 좋습니다.
결측치 값 깨끗하게 정리하는 과정은 clean_data.py 파일을 참조하세요.

---

### 1. 모델 설계 5단계 (Architecture Design)

단변수 LSTM 설계는 단순히 층을 쌓는 것이 아니라, **데이터의 시간적 맥락**을 어떻게 모델에 주입할지 결정하는 과정입니다.

#### ① 데이터 프레이밍 (Window Size 결정)

* **설계 내용:** "몇 시간의 데이터를 보고 다음 1시간을 예측할 것인가?"를 정합니다.
* **제안:** 24시간 주기가 뚜렷한 전력 데이터 특성상, **과거 24시간(`n_steps = 24`)**의 데이터를 입력으로 설정하는 것이 합리적입니다.

#### ② 데이터 정규화 (Scaling)

* **이유:** LSTM은 활성화 함수로 `tanh`나 `sigmoid`를 사용하므로, 입력값이 크면 학습이 매우 늦어집니다.
* **방법:** `MinMaxScaler`를 사용하여 전력량 데이터를 0과 1 사이로 변환합니다.

#### ③ 신경망 구조 설계 (Layer Design)

* **LSTM 층:** 전력량의 패턴(피크 시간대 등)을 기억하기 위해 50~100개의 유닛을 가진 LSTM 층을 배치합니다.
* **Dense 층:** 마지막에 하나의 숫자(예측 전력량)를 출력해야 하므로 유닛이 1개인 Dense 층을 연결합니다.

#### ④ 컴파일 및 손실 함수 선택

* **Loss:** 수치 예측(회귀)이므로 정답과의 차이의 제곱인 **MSE(Mean Squared Error)** 를 사용합니다.
* **Optimizer:** 학습 속도를 자동으로 조절해주는 **Adam** 이 가장 무난합니다.

#### ⑤ 검증 전략 (Train/Test Split)

* 시계열 데이터는 순서가 중요하므로 무작위로 섞지 않고, **앞의 10일치 데이터를 학습용, 뒤의 4일치 데이터를 테스트용**으로 순차 분리합니다.

---

### 2. 실전 파이썬 코드

아래 코드는 data 폴더에 있는 파일을 읽어 전처리부터 예측까지 수행합니다.

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Input

# 1. 데이터 로드 및 정렬
df = pd.read_csv('./data/clean_power_usage_dataset.csv')
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values('Date')

# 2. 결측치 처리 (시간축 생성 및 선형 보간)
df = df.set_index('Date').resample('h').asfreq()
df['Usage'] = df['Usage'].interpolate(method='linear')
df = df.reset_index()

# 3. 정규화 (Min-Max Scaling)
scaler = MinMaxScaler()
# 학습 시 2차원 배열을 사용했음을 기억하세요.
df['Usage_scaled'] = scaler.fit_transform(df[['Usage']])

# 4. 지도 학습 데이터셋 생성 (Sliding Window)
window_size = 24
X, y = [], []
scaled_data = df['Usage_scaled'].values

for i in range(window_size, len(scaled_data)):
    X.append(scaled_data[i-window_size:i]) # 과거 24시간
    y.append(scaled_data[i])               # 현재 시점 (정답)

X = np.array(X)
y = np.array(y)

# LSTM 입력을 위해 3차원 변환: (샘플 수, 타임스텝, 특성 수)
X = X.reshape((X.shape[0], X.shape[1], 1))

# 학습/테스트 데이터 분할 (8:2)
train_size = int(len(X) * 0.8)
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

print(f"학습 데이터 크기: {X_train.shape}")
print(f"테스트 데이터 크기: {X_test.shape}")

# 5. LSTM 모델 설계 (최신 Keras 방식 적용)
model = Sequential([
    Input(shape=(window_size, 1)), 
    LSTM(64, activation='relu'),
    Dense(32, activation='relu'),
    Dense(1)
])

model.compile(optimizer='adam', loss='mse')

# 6. 모델 학습
print("모델 학습 시작...")
history = model.fit(X_train, y_train, epochs=50, batch_size=32, validation_split=0.1, verbose=1)

# 7. 결과 예측 및 차원 오류 수정
predictions_scaled = model.predict(X_test)

# inverse_transform에는 반드시 2D 배열이 들어가야 함
predictions = scaler.inverse_transform(predictions_scaled)

# y_test는 (N,) 형태의 1차원이므로 .reshape(-1, 1)로 2차원 변환 후 복원
y_test_unscaled = scaler.inverse_transform(y_test.reshape(-1, 1))

# 8. 시각화
plt.figure(figsize=(12, 6))
plt.plot(y_test_unscaled, label='Actual Usage', color='blue')
plt.plot(predictions, label='Predicted Usage', color='red', linestyle='--')
plt.title('Smart Device Power Usage Prediction')
plt.xlabel('Time (Hours)')
plt.ylabel('Usage')
plt.legend()
plt.grid(True)
plt.show()

```

---

### 3. 코드 상세 설명

* **`input_shape=(24, 1)`:** LSTM의 핵심 설계입니다. 24시간(Time Steps)이라는 시간 축과 1개(Feature, 사용량)의 변수를 보겠다는 뜻입니다.
* **`return_sequences=False`:** LSTM 층을 하나만 사용할 때 설정합니다. 만약 LSTM을 2층으로 쌓고 싶다면 첫 번째 LSTM에는 이 값을 `True`로 주어야 합니다.
* **`inverse_transform`:** 모델은 0~1 사이의 숫자로 예측값을 내놓습니다. 이를 우리가 이해할 수 있는 실제 전력량(kWh 등) 단위로 되돌리는 꼭 필요한 단계입니다.

`model.fit()`은 설계된 신경망 모델에게 **"데이터를 줄 테니 스스로 규칙을 찾아내서 공부해라"**라고 명령하는 실제 **학습(Training)** 명령어입니다.

단순히 실행하는 것을 넘어, 내부에서 어떤 일이 벌어지는지 핵심 파라미터와 함께 자세히 설명해 드릴게요.

---

### 4. `model.fit()`의 핵심 역할

이 함수가 실행되면 컴퓨터 내부에서는 다음의 **학습 사이클**이 반복됩니다:

1. **순전파(Forward Pass):** 입력 데이터를 넣고 현재 가중치로 예측값을 계산합니다.
2. **손실 계산(Loss Calculation):** 예측값과 실제 정답 사이의 오차를 구합니다.
3. **역전파(Backward Pass):** 오차를 줄이기 위해 가중치를 어느 방향으로 얼마나 수정할지 결정합니다.
4. **업데이트(Optimizer):** 가중치를 실제로 수정합니다.

---

### 5. 주요 파라미터 상세 분석

```python
history = model.fit(
    X_train, y_train,           # 1. 학습 데이터와 정답
    epochs=50,                  # 2. 전체 데이터 반복 횟수
    batch_size=16,              # 3. 한 번에 학습할 묶음 크기
    validation_split=0.1,       # 4. 검증용 데이터 비율
    verbose=1                   # 6. 출력 모드
)

```

#### ① 데이터 관련 (`X_train`, `y_train`)

* **X**: 모델이 공부할 '문제' (입력 특성)
* **y**: 모델이 맞춰야 할 '정답' (타겟 레이블)

#### ② `epochs`

* 전체 데이터를 50번 돌려가며 학습합니다.

#### ③ `batch_size`

* 가중치를 한 번 업데이트하기 위해 사용하는 데이터의 양입니다.
* **작으면(예: 8, 16):** 가중치 업데이트가 빈번해 학습이 세밀하지만 속도가 느립니다.
* **크면(예: 128, 256):** 한 번에 많이 계산하여 GPU/CPU 병렬 효율이 좋고 속도가 빠릅니다.

#### ④ `validation_split` (또는 `validation_data`)

* 학습 도중 모델이 처음 보는 데이터로 **자체 시험**을 치르게 합니다.
* `0.1`로 설정하면 전체 학습 데이터의 10%는 공부에 쓰지 않고, 매 에포크 끝에 성능 측정용으로만 사용합니다. 이를 통해 **과적합(Overfitting)** 여부를 실시간으로 감시합니다.

#### ⑤ `verbose`

* 학습 진행 상황을 화면에 어떻게 보여줄지 결정합니다. (0: 무표시, 1: 진행 표시줄 포함, 2: 에포크당 한 줄 출력)

---

### 6. 반환값: `history` 객체

`model.fit()`은 학습이 끝나면 그냥 종료되는 것이 아니라, 학습 과정의 모든 기록(에포크별 오차 등)을 담은 **`history` 객체**를 돌려줍니다.

```python
# 학습이 끝난 후 오차 변화를 그래프로 그릴 수 있습니다.
import matplotlib.pyplot as plt

plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.legend()
plt.show()

```

---

### 7. model.fit() 함수 정리

`model.fit()`은 단순한 실행 함수가 아니라, **데이터 공급 전략(`batch_size`)**, **인내심(`epochs`)**, **성능 검증(`validation`)**, **안전장치(`callbacks`)**를 모두 아우르는 지휘소와 같습니다.

### 8. Epoch(에포크), Batch Size(배치 사이즈), Iteration(이터레이션) 개념

이 개념들은 마치 **"두꺼운 문제집 한 권을 공부하는 전략"**과 같습니다.

---

#### 1. Epoch (에포크): "문제집을 몇 번 반복회서 읽어 볼 것인가?"

**Epoch**는 전체 데이터셋이 신경망을 한 번 통과(순전파 + 역전파)한 상태를 의미합니다.

* **정의:** 모델이 준비된 모든 학습 데이터를 정확히 한 번 다 훑었을 때 "1 Epoch가 지났다"고 합니다.
* **필요성:** 신경망은 한 번만 봐서는 데이터의 복잡한 패턴을 모두 이해하지 못합니다. 여러 번 반복해서 보아야 가중치($W$)가 최적의 값으로 수렴합니다.
* **주의점:** * 너무 적으면 **과소적합(Underfitting)**: 공부를 덜 해서 성적이 안 나오는 상태.
* 너무 많으면 **과적합(Overfitting)**: 문제 자체를 달달 외워서 새로운 유형(테스트 데이터)이 나오면 틀리는 상태.

---

#### 2. Batch Size (배치 사이즈): "한 번에 몇 문제를 풀 것인가?"

데이터 전체를 한꺼번에 CPU 또는 GPU 메모리에 올리기에는 데이터가 너무 크고 무겁습니다. 그래서 데이터를 작은 덩어리로 나누는데, 이 **덩어리의 크기**가 **Batch Size**입니다.

* **정의:** 가중치를 한 번 업데이트하기 위해 모델에 투입되는 데이터 샘플의 묶음 단위입니다.
* **작동 방식:** 만약 1,000개의 데이터가 있고 배치를 100으로 잡았다면, 100개 풀고 정답 확인(가중치 업데이트)하고, 다음 100개 풀고 확인하는 과정을 반복합니다.
* **선택의 기준:**
* **큰 배치 사이즈:** 학습 속도가 빠르고 안정적이지만, GPU 메모리(VRAM)를 많이 소모합니다.
* **작은 배치 사이즈:** 학습 속도는 느려질 수 있지만, 모델이 더 세밀하게 학습되어 일반화 능력이 좋아지는 경우가 많습니다.

---

#### 3. Iteration (이터레이션): "한 에포크를 위해 몇 번 반복하는가?"

**Iteration**은 1 Epoch를 완료하기 위해 필요한 **가중치 업데이트 횟수**입니다.

* **계산식:** $Iteration = \frac{전체 데이터 수}{Batch Size}$
* **예시:** * 전체 데이터: 2,000개
* Batch Size: 500개
* 결과: **1 Epoch**를 위해 **4 Iteration**이 필요함 (즉, 한 에포크 동안 총 4번 가중치를 수정함).

---

#### 4. loss (훈련 손실)

* 의미: 모델이 학습 데이터(X_train)를 풀면서 낸 오차입니다.
* 역할: 모델은 이 loss를 줄이기 위해 가중치를 수정하며 공부합니다.
* 특징: 학습이 진행될수록(에포크가 쌓일수록) loss는 보통 계속해서 떨어집니다. 같은 문제를 반복해서 푸는 것이니 당연히 오차는 줄어들게 됩니다.

---

#### 5. Val_loss (검증 손실)

* 의미: 모델이 학습에 한 번도 사용하지 않은 데이터(validation_split으로 떼어놓은 10%의 데이터)를 풀었을 때 낸 오차입니다.
* 역할: 모델의 **진짜 실력(일반화 능력)** 을 검증합니다. 공부한 내용을 토대로  처음 보는 문제도 잘 맞추는지 확인하는 것입니다.
* 특징: 이 수치가 낮을수록 모델이 실전에 강하다는 뜻입니다.

---

### 9. 데이터 학습 프로세스

실제 모델이 일하는 순서는 다음과 같습니다.

1. **데이터 셔플(Shuffle):** 문제 순서를 외우지 못하게 데이터를 무작위로 섞습니다.
2. **배치 분할:** 설정한 **Batch Size**만큼 데이터를 쪼개서 모델에 넣습니다.
3. **순전파(Forward):** 모델이 예측값을 내놓습니다.
4. **역전파(Backward):** 정답과 비교하여 틀린 만큼 가중치를 수정합니다 (**1 Iteration 완료**).
5. **반복:** 모든 데이터를 다 쓸 때까지 2~4 과정을 반복합니다.
6. **에포크 완료:** 데이터 100%를 다 봤다면 **1 Epoch**가 종료됩니다.
7. **재시작:** 설정한 Epoch 횟수만큼 다시 1번부터 시작합니다.

---

### 10. 실행 결과 분석

| 항목 | 건수 | 비고 |
|---|---|---|
| 전체 건수 | 2928 | - |
| 학습건수  | 2208 | 2928 * 0.8 (80%) |
| 배치 사이즈 | 32 | - |
| window_size | 168 | - |
| Iteration | 63 | (2208 - 168) / 32 = 63 |
| 에포크 | 50 | - |

24 시간 * 7일 = 168, 즉 1주일을 의미함

---
