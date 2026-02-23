# Attention(어텐션) 메커니즘

## 1. Attention(어텐션) 메커니즘 이란?

어텐션 이전에는 주로 **RNN(순환 신경망)** 기반의 모델을 사용했습니다. 하지만 RNN은 문장이 길어질수록 앞부분의 정보를 잊어버리는 **장기 의존성(Long-term dependency)** 문제와, 모든 정보를 고정된 크기의 벡터에 억지로 구겨 넣어야 하는 **정보 손실** 문제가 있었습니다.

어텐션은 이 문제를 해결하기 위해 **"모든 단어를 똑같이 보지 말고, 출력 단어와 관련 있는 입력 단어에 집중(Attention)하자"** 는 아이디어에서 출발했습니다.

쉽게 비유하자면, 우리가 복잡한 그림을 볼 때 전체를 똑같은 강도로 관찰하기보다 **특정 부분(예: 사람의 얼굴이나 움직이는 물체)** 에 시선을 고정하는 것과 같습니다.

---

### 1. Attention의 핵심 개념

어텐션 메커니즘을 이해하려면 세 가지 요소를 꼭 알아야 합니다. 마치 도서관에서 책을 찾는 과정과 비슷합니다.

#### 핵심 원리: Query, Key, Value

어텐션은 보통 세 가지 요소의 관계를 계산합니다:

* **Query (Q):** 현재 찾고자 하는 정보 (질문)
* **Key (K):** 도서관에 있는 책들의 제목 (인덱스/키워드)
* **Value (V):** 책 안에 담긴 실제 내용 (정보)

**작동 순서:**

1. **유사도 계산:** 현재 시점의 `Query`와 모든 `Key`를 비교하여 얼마나 유사한지 점수를 매깁니다.
2. **소프트맥스(Softmax):** 이 점수들을 합이 1이 되도록 확률값(가중치)으로 변환합니다.
3. **가중합 계산:** 구해진 확률값을 각 `Value`에 곱해서 모두 더합니다. 결과적으로 **중요한 정보는 진하게, 불필요한 정보는 연하게** 섞인 하나의 벡터가 나옵니다.

모델은 Query와 모든 Key 사이의 **유사도(Attention Score)** 를 계산합니다. 그 결과에 따라 각 Value에 부여할 가중치를 결정하고, 이들을 모두 합쳐서 최종적인 출력값을 만들어냅니다.

---

### 2. 주요 장점

* **장기 의존성(Long-term Dependency) 해결:** 문장이 아무리 길어져도 특정 단어와 관련 있는 단어를 직접 연결해 정보를 가져오므로 성능 저하가 적습니다.
* **성능 향상:** 모든 데이터를 동일하게 처리하지 않고 필요한 부분만 골라 학습하므로 정확도가 높아집니다.
* **설명 가능성(Interpretability):** 모델이 결과를 낼 때 **어떤 데이터를 참고했는지 시각화** 할 수 있어, AI의 판단 근거를 파악하기 유리합니다.

---

### 3. 어텐션의 종류

어텐션은 적용 방식에 따라 몇 가지 주요 형태로 나뉩니다.

| 종류 | 특징 |
| --- | --- |
| **Dot-Product Attention** | Query와 Key를 내적하여 단순하게 유사도를 구함 (가장 기본) |
| **Bahdanau Attention** | RNN의 은닉 상태를 활용하여 동적으로 가중치를 계산 |
| **Self-Attention** | **자기 자신** 내의 단어들끼리 관계를 파악 (Transformer의 핵심) |
| **Multi-Head Attention** | 여러 개의 어텐션을 병렬로 수행하여 다양한 관점에서 정보를 파악 |

### 4. 구현 시 고려해야 할 점

실제로 어텐션을 활용한 모델을 설계할 때는 다음과 같은 기술적 요소가 포함됩니다.

1. **Scaling (스케일링):** $Key$의 차원이 커지면 내적 값이 너무 커져 학습이 불안정해질 수 있습니다. 이를 방지하기 위해 차원 수($\sqrt{d_k}$)로 나누어 값을 조절합니다.
2. **Masking (마스킹):** 미래의 단어를 미리 보고 답을 베끼지 못하도록, 아직 나오지 않은 정보는 어텐션 점수를 강제로 0으로 만드는 장치를 둡니다.

---

### 5. 요약: 수학적 구조

이를 수식으로 나타내면 다음과 같습니다 (Scales Dot-Product Attention 기준):

$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$

* $QK^T$ : 유사도 측정
* $\sqrt{d_k}$ : 안정적인 학습을 위한 스케일링
* $\text{softmax}$ : 가중치 합을 1로 변환
* $V$ 곱하기 : 최종 정보 추출

---

### 6. 어텐션이 가져온 변화

* **성능 향상:** 긴 문장에서도 문맥을 놓치지 않고 정확한 번역/요약이 가능해졌습니다.
* **시각화 가능:** 모델이 어떤 단어에 집중해서 결과를 내놓았는지 '어텐션 맵'을 통해 확인하며 모델의 판단 근거를 알 수 있습니다.
* **Transformer의 탄생:** 어텐션만으로 모델을 만든 Transformer가 등장하며, 현재 우리가 쓰는 **GPT, BERT** 같은 거대 언어 모델(LLM)의 시대를 열었습니다.

### 7.활용 분야

| 분야 | 활용 사례 |
| --- | --- |
| **기계 번역** | 소스 문장에서 번역할 단어와 가장 연관 깊은 단어를 찾아 번역 (예: Google 번역) |
| **문서 요약** | 전체 본문 중 핵심 문장이나 단어에 집중하여 요약문 생성 |
| **이미지 캡셔닝** | 이미지의 특정 부분을 보고 그에 맞는 설명 글을 생성 |
| **생성형 AI** | GPT와 같은 대규모 언어 모델(LLM)이 맥락에 맞는 다음 단어를 예측할 때 사용 |

---

### 8. 항공기 승객 데이터를 활용한 Attention 메커니즘 예제

딥러닝 모델 개발 5단계 프로세스에 맞춰, **Attention-LSTM 기반 항공객 승객 수 예측 모델**의 전체 과정을 알아보겠습니다.

---

#### 1단계: 데이터 준비 및 전처리 (Data Preparation)

시계열 데이터의 특성을 고려하여 모델이 학습하기 좋은 형태로 가공하는 단계입니다.

* **계절성 차분 (Seasonal Differencing):** 항공객 데이터는 1년 주기의 강한 계절성을 보입니다. 이를 해결하기 위해 현재 시점에서 12개월 전의 데이터를 뺀 '증감량'만을 추출하여 데이터의 변동성을 안정화합니다.
* **정규화 (Normalization):** `MinMaxScaler`를 사용해 데이터를 0~1 사이로 변환하여 신경망의 학습 속도와 안정성을 높입니다.
* **시퀀스 생성:** 과거 12개월(`look_back`)의 데이터를 하나의 묶음으로 만들어 다음 시점의 값을 예측하는 지도 학습 형태로 구조를 변경합니다.

#### 2단계: 모델 설계 (Model Architecture)

LSTM 레이어 위에 **Attention 레이어**를 쌓아 올린 구조입니다.

* **LSTM 레이어:** 시계열 데이터의 장기적인 의존성을 학습합니다. `return_sequences=True` 설정을 통해 모든 시점의 정보를 Attention 레이어로 전달합니다.
* **Attention 메커니즘 적용 (핵심):**
  * **왜 적용했는가?** LSTM은 시퀀스가 길어질수록 과거의 중요한 정보를 잊어버리는 '장기 의존성 문제'가 발생할 수 있습니다. Attention은 **과거 12개월 중 예측하려는 시점과 가장 상관관계가 높은 특정 달(예: 작년 동월)의 정보에 더 집중**하게 만듭니다.
  * **어떻게 작동하는가?** 가중치(`W`)와 편향(`b`)을 통해 각 시점의 중요도(점수)를 계산하고, `Softmax` 함수를 통해 합계가 1이 되는 가중치를 산출합니다. 이 가중치를 원본 데이터에 곱해 '문맥 벡터(Context Vector)'를 생성함으로써 중요한 시점의 정보를 강조합니다.

#### 3단계: 모델 컴파일 및 학습 (Compile & Training)

설계한 모델이 오차를 줄여나갈 수 있도록 설정하고 학습을 진행하는 단계입니다.

* **손실 함수(Loss) 및 옵티마이저:** 시계열 예측(회귀)이므로 `mse`(평균 제곱 오차)를 사용하며, 효율적인 학습을 위해 `adam` 옵티마이저를 선택했습니다.
* **학습 실행:** 300회의 에포크(Epochs) 동안 데이터를 반복 학습하며 최적의 가중치를 찾아갑니다.
  * 에포크(Epochs) 횟수를 50회 반복하는 것과 비교해보세요.

#### 4단계: 모델 평가 및 검증 (Evaluation)

학습에 사용되지 않은 최근 24개월 데이터를 통해 모델의 성능을 정밀하게 측정합니다.

* **MAPE(평균 절대 백분율 오차) 확인:** 실제값 대비 오차가 몇 %인지 확인합니다. 제공된 최종 결과에 따르면 **MAPE 3.42%** 라는 매우 높은 정확도를 기록했습니다.
* **시각화:** 실제 승객 수 추이와 모델이 예측한 추이를 그래프로 비교하여 패턴이 일치하는지 육안으로 검증합니다.

#### 5단계: 모델 저장 및 활용 (Saving & Inference)

성능이 확인된 모델을 예측에 사용하기 위해 파일로 저장합니다.

* **모델 저장:** 커스텀 레이어인 `AttentionLayer`를 포함하여 전체 모델을 `.h5` 형식으로 저장합니다.
* **스케일러 저장:** 예측 시 데이터를 다시 원래 단위(승객 수)로 복원하기 위해 정규화 규칙이 담긴 스케일러를 `.pkl` 파일로 함께 저장합니다.

---

#### 전체 코드

파일명 : day4/step4/attention-tranining.py

```python
import numpy as np
import pandas as pd
import koreanize_matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf
from tensorflow.keras import layers, Model
from sklearn.preprocessing import MinMaxScaler
import os
import joblib  # 스케일러(MinMaxScaler) 저장을 위한 라이브러리

# 1. 데이터 로드 및 전처리
# flights.csv 데이터를 읽어와서 승객 수(Passengers) 데이터만 추출합니다.
data_df = pd.read_csv('./data/flights.csv')
passengers = data_df['Passengers'].values.astype(float)

# 계절성 차분 (Seasonal Differencing)
# 시계열 데이터의 계절적 패턴을 제거하여 정상성(Stationarity)을 확보합니다.
# 12개월 전의 데이터와 현재 데이터의 차이를 계산합니다.
seasonal_period = 12
diff_passengers = passengers[seasonal_period:] - passengers[:-seasonal_period]
diff_passengers = diff_passengers.reshape(-1, 1)

# 데이터 정규화 (Normalization)
# 신경망 학습의 안정성과 속도를 위해 데이터를 0~1 사이 값으로 변환합니다.
scaler = MinMaxScaler()
data_scaled = scaler.fit_transform(diff_passengers)

# [중요] 스케일러 파일 저장
# 추후 예측 단계(Inference)에서 예측된 값을 다시 원래 단위로 복원(Inverse Transform)하기 위해 저장합니다.
scaler_filename = "./model/air_passengers_scaler.pkl"
if not os.path.exists('./model'):
    os.makedirs('./model')
joblib.dump(scaler, scaler_filename)
print(f"✅ 스케일러 저장 완료: {scaler_filename}")

# 시퀀스 생성 함수
# 과거의 데이터(look_back 기간)를 기반으로 다음 시점의 값을 예측하기 위한 데이터셋을 만듭니다.
def create_dataset(dataset, look_back=12):
    X, y = [], []
    for i in range(len(dataset) - look_back):
        X.append(dataset[i:(i + look_back), 0]) # 과거 12개월 데이터
        y.append(dataset[i + look_back, 0])      # 정답(13개월째 데이터)
    return np.array(X), np.array(y)

look_back = 12
X, y = create_dataset(data_scaled, look_back)

# LSTM 입력을 위한 3차원 변환: (샘플 수, 타임스텝, 특성 수)
X = X.reshape((X.shape[0], X.shape[1], 1))

# 학습/테스트 데이터 분리 (최근 24개월 데이터를 테스트용으로 사용)
train_size = len(X) - 24
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

# 2. Attention 레이어 정의
# LSTM의 모든 시점 출력 중 중요한 부분에 가중치를 부여하는 메커니즘입니다.
@tf.keras.utils.register_keras_serializable() # 모델 저장/로드 시 커스텀 레이어 인식을 위해 등록
class AttentionLayer(layers.Layer):
    def __init__(self, **kwargs):
        super(AttentionLayer, self).__init__(**kwargs)

    def build(self, input_shape):
        # 학습 가능한 가중치(Weight)와 편향(Bias) 정의
        self.W = self.add_weight(name="att_weight", shape=(input_shape[-1], 1), initializer="normal")
        self.b = self.add_weight(name="att_bias", shape=(input_shape[1], 1), initializer="zeros")
        super(AttentionLayer, self).build(input_shape)

    def call(self, inputs):
        # Attention 점수 계산 (Tanh 활성화 함수 사용)
        et = tf.nn.tanh(tf.matmul(inputs, self.W) + self.b)
        # Softmax를 통해 각 시점의 가중치(합계 1) 산출
        at = tf.nn.softmax(et, axis=1)
        # 원본 입력에 가중치를 곱하여 문맥 벡터(Context Vector) 생성
        context = inputs * at
        # 가중치가 적용된 벡터들을 합산하여 최종 출력
        return tf.reduce_sum(context, axis=1), at

    def get_config(self):
        # 모델의 설정을 반환 (저장된 모델을 불러올 때 필요)
        config = super(AttentionLayer, self).get_config()
        return config

# 3. 모델 구축 및 학습
inputs = layers.Input(shape=(look_back, 1))
# return_sequences=True는 모든 시점의 출력을 Attention 레이어로 전달하기 위함입니다.
lstm_out = layers.LSTM(128, return_sequences=True)(inputs)
# Attention 적용: 시계열 데이터 내에서 중요한 패턴이 있는 시점을 강조합니다.
attention_out, _ = AttentionLayer()(lstm_out)
# 최종 예측 값을 위한 Dense 레이어
prediction = layers.Dense(1)(attention_out)

model = Model(inputs=inputs, outputs=prediction)
model.compile(optimizer='adam', loss='mse')

print("🚀 고성능 Attention-LSTM 모델 학습 중...")
# 에포크 300회 학습
model.fit(X_train, y_train, epochs=300, batch_size=16, verbose=0)

# [중요] 학습된 모델 저장
# .h5 형식으로 저장하여 추후 추론 파일에서 불러와 사용할 수 있게 합니다.
model_filename = "./model/air_passengers_best_model.h5"
model.save(model_filename)
print(f"✅ 모델 저장 완료: {model_filename}")

# 4. 성능 검증 (MAPE 확인)
# 테스트 데이터에 대해 예측 수행
y_pred_diff_scaled = model.predict(X_test)
# 정규화된 값을 원래의 차분값 스케일로 복원
y_pred_diff = scaler.inverse_transform(y_pred_diff_scaled).flatten()

# 차분된 값을 원래의 승객 수 단위로 복원 (이전 해의 같은 달 값에 더함)
actual_start_idx = len(passengers) - 24
y_pred_final = []
for i in range(24):
    prev_year_val = passengers[actual_start_idx - seasonal_period + i]
    y_pred_final.append(prev_year_val + y_pred_diff[i])

y_pred_final = np.array(y_pred_final)
y_actual_final = passengers[actual_start_idx:]

# MAPE(Mean Absolute Percentage Error): 평균 절대 백분율 오차
# 실제값 대비 오차가 몇 %인지 나타내는 지표입니다.
mape = np.mean(np.abs((y_actual_final - y_pred_final) / y_actual_final)) * 100
print(f"📊 최종 모델의 MAPE: {mape:.2f} %")

# 5. 시각화
plt.figure(figsize=(12, 5))
plt.plot(y_actual_final, label='실제값 (Actual)', marker='o')
plt.plot(y_pred_final, label=f'예측값 (Predicted, MAPE: {mape:.2f}%)', marker='x', color='red')
plt.title('항공기 승객 수 예측 결과 (Attention 기반 LSTM)')
plt.xlabel('시간 (최근 24개월)')
plt.ylabel('승객 수')
plt.legend()
plt.grid(True)
plt.show()

```

#### 실행 결과

![alt text](image-9.png)

---

### 9. 학습한 모델을 이용하여 1961년 항공기 승객 예측하기

**인퍼런스(추론) 프로세스 개발 4단계**에 맞춰 각 과정과 **Attention 메커니즘의 활용 방식**을 알아보겠습니다.

---

#### 1단계: 모델 및 환경 로드 (Model & Environment Loading)

학습이 완료된 모델과 전처리 도구를 다시 불러와 예측 준비를 하는 단계입니다.

* **커스텀 레이어 등록:** `load_model` 시 에러를 방지하기 위해 학습 때 정의한 `AttentionLayer` 클래스를 동일하게 선언하고, `Custom` 패키지로 등록합니다.
* **파일 로드:** `tf.keras.models.load_model`을 사용해 학습된 모델(`.h5`)을 불러오고, `joblib`으로 정규화 규칙이 담긴 스케일러(`.pkl`)를 로드합니다.
* **컴파일 옵션 제외:** 예측 전용이므로 `compile=False`를 설정하여 불필요한 학습 설정 로드 시 발생할 수 있는 오류를 차단합니다.

#### 2단계: 입력 데이터 준비 (Data Preparation)

미래를 예측하기 위한 기준점이 되는 데이터를 정규화하고 시퀀스 형태로 가공하는 단계입니다.

* **계절성 차분 적용:** 모델이 학습한 방식대로 현재 승객 수 데이터에서 12개월 전 데이터를 뺀 '증감량'을 계산합니다.
* **스케일링:** 로드된 `scaler`를 사용하여 증감량 데이터를 모델이 인식할 수 있는 0~1 사이의 값으로 변환합니다.
* **마지막 시퀀스 추출:** 1961년을 예측하기 위해 1960년의 마지막 12개월분 데이터를 추출하여 3차원 배열(`1, 12, 1`)로 변환합니다.

#### 3단계: 재귀적 예측 및 Attention 활용 (Recursive Prediction & Attention)

가장 핵심적인 단계로, 모델이 과거 데이터를 분석해 미래를 예측합니다.

* **Attention 메커니즘의 활용:**
  * **핵심 단서 포착:** 모델 내부의 `AttentionLayer`는 입력된 12개월 데이터 중 **현재 예측하려는 시점과 가장 연관성이 높은 과거 시점(예: 작년 동월의 증감 패턴)** 에 더 높은 가중치를 부여합니다.
  * **문맥 벡터(Context Vector) 생성:** `tanh` 함수로 계산된 점수를 `softmax`로 확률화하여, 중요한 정보는 강조하고 불필요한 노이즈는 걸러낸 '압축된 정보'를 예측 레이어에 전달합니다.

* **재귀적 업데이트:** 모델이 예측한 1월의 값을 다시 입력 데이터의 끝에 넣고, 가장 오래된 값을 빼는 '윈도우 슬라이딩' 방식을 통해 12월까지 순차적으로 예측을 진행합니다.

#### 4단계: 결과 복원 및 시각화 (Post-processing & Visualization)

모델의 출력값(정규화된 증감량)을 사람이 이해할 수 있는 실제 값으로 바꾸는 단계입니다.

* **역변환(Inverse Transform):** `scaler`를 통해 0~1 사이의 예측값을 다시 실제 '증감량' 수치로 되돌립니다.
* **차분 복원:** 예측된 증감량을 1960년의 실제 값에 더하여 **최종적인 1961년 승객 수** 를 산출합니다.
* **결과 출력:** `matplotlib`을 통해 과거 데이터와 연결된 미래 예측 그래프를 그리고, 월별 예상 승객 수를 텍스트로 출력합니다.

---

#### 💡 인퍼런스에서 Attention이 중요한 이유

학습 때와 마찬가지로 인퍼런스에서도 **Attention**은 모델이 **"과거 12개월 중 어디를 중요하게 봐야 하는가"** 를 계속해서 가이드합니다. 특히 재귀적 예측은 뒤로 갈수록 오차가 누적될 위험이 있는데, Attention 메커니즘이 **고정된 주기의 핵심 패턴에 집중**하게 함으로써 1961년 예측에서도 일관성 있는 계절적 흐름을 유지할 수 있게 해줍니다.

#### 전체 코드

파일명 : day4/step4/attention-inference.py

```python
import numpy as np
import pandas as pd
import koreanize_matplotlib
import matplotlib.pyplot as plt
import tensorflow as tf
import joblib
import os

# 1. Attention 레이어 클래스 정의 (로드 시 필수)
# @tf.keras.utils.register_keras_serializable()는 학습 시 등록된 이름을 찾기 위해 필요할 수 있습니다.
@tf.keras.utils.register_keras_serializable(package="Custom")
class AttentionLayer(tf.keras.layers.Layer):
    def __init__(self, **kwargs):
        super(AttentionLayer, self).__init__(**kwargs)

    def build(self, input_shape):
        self.W = self.add_weight(name="att_weight", shape=(input_shape[-1], 1), initializer="normal")
        self.b = self.add_weight(name="att_bias", shape=(input_shape[1], 1), initializer="zeros")
        super(AttentionLayer, self).build(input_shape)

    def call(self, inputs):
        et = tf.nn.tanh(tf.matmul(inputs, self.W) + self.b)
        at = tf.nn.softmax(et, axis=1)
        context = inputs * at
        return tf.reduce_sum(context, axis=1), at

    def get_config(self):
        return super(AttentionLayer, self).get_config()

# 2. 파일 경로 설정
model_path = './model/air_passengers_best_model.h5'
scaler_path = './model/air_passengers_scaler.pkl'
data_path = './data/flights.csv'

# 파일 존재 확인
if not all(os.path.exists(f) for f in [model_path, scaler_path, data_path]):
    print("❌ 필요한 파일(모델, 스케일러, 데이터)이 없습니다. 경로를 확인해주세요.")
else:
    # 3. 모델 및 스케일러 로드
    # 'Custom>AttentionLayer' 에러를 방지하기 위해 custom_object_scope를 사용합니다.
    custom_objects = {'AttentionLayer': AttentionLayer}
    
    with tf.keras.utils.custom_object_scope(custom_objects):
        model = tf.keras.models.load_model(model_path, compile=False)
    
    scaler = joblib.load(scaler_path)
    print("✅ 모델 및 스케일러 로드 완료")

    # 4. 원본 데이터 로드 (미래 예측의 기준점)
    data_df = pd.read_csv(data_path)
    col_name = 'passengers' if 'passengers' in data_df.columns else 'Passengers'
    passengers = data_df[col_name].values.astype(float)

    # 5. 미래 예측 (1961년 12개월)
    # 마지막 12개월의 차분 데이터 준비
    seasonal_period = 12
    diff_passengers = passengers[seasonal_period:] - passengers[:-seasonal_period]
    diff_scaled = scaler.transform(diff_passengers.reshape(-1, 1))
    
    # 마지막 시퀀스 (1960년 패턴)
    current_batch = diff_scaled[-12:].reshape(1, 12, 1)
    
    future_diff_preds = []
    print("🔮 1961년 미래 예측 진행 중...")
    
    for i in range(12):
        pred_scaled = model.predict(current_batch, verbose=0)
        future_diff_preds.append(pred_scaled[0, 0])
        
        # 윈도우 슬라이딩 업데이트
        new_val = pred_scaled.reshape(1, 1, 1)
        current_batch = np.append(current_batch[:, 1:, :], new_val, axis=1)

    # 6. 역변환 및 복원
    future_diff_unscaled = scaler.inverse_transform(np.array(future_diff_preds).reshape(-1, 1)).flatten()
    
    # 1961년 최종값 = 1960년 실제값 + 예측된 증감량
    last_year_1960 = passengers[-12:]
    forecast_1961 = last_year_1960 + future_diff_unscaled

    # 7. 시각화 및 출력
    future_months = pd.date_range(start='1961-01-01', periods=12, freq='MS')
    forecast_series = pd.Series(forecast_1961, index=future_months)

    plt.figure(figsize=(12, 6))
    plt.plot(pd.to_datetime(data_df['Month'])[-24:], passengers[-24:], label='실제값 (1959-1960)', marker='o')
    plt.plot(forecast_series, label='예측값 (1961)', marker='x', color='red', linestyle='--')
    plt.title('항공기 승객 수 미래 예측 (1961년)')
    plt.ylabel('승객 수')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

    print("\n--- 1961년 예측 결과 ---")
    for month, val in zip(future_months, forecast_1961):
        print(f"{month.strftime('%Y-%m')}: {int(val)}명")
```

#### 실행 결과

![alt text](image-10.png)

---