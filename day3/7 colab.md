# 구글 콜랩(Google Colab)이란?

구글 콜랩(Google Colab, 정식 명칭 Colaboratory)은 브라우저에서 직접 **파이썬(Python) 코드를 작성하고 실행**할 수 있게 해주는 클라우드 기반의 서비스입니다.

쉽게 말해, 내 컴퓨터에 아무것도 설치하지 않고도 웹사이트에 접속만 하면 바로 프로그래밍을 할 수 있는 '온라인 연습장'과 같습니다.

---

## Colab의 주요 특징

### 1. 무료 GPU 지원 (가장 큰 장점!)

딥러닝이나 데이터 분석에는 고성능 그래픽 카드(GPU)가 필요한데, 콜랩은 구글의 강력한 하드웨어(**Nvidia T4, L4 GPU 등**)를 무료로 사용할 수 있게 해줍니다. 비싼 컴퓨터를 살 돈이 없는 학생이나 연구원들에게는 매우 좋은 것입니다.

### 2. 설치가 필요 없는 환경

파이썬을 공부하려면 아나콘다(Anaconda)를 깔거나 환경 설정을 하느라 애를 먹곤 합니다. 콜랩은 구글 계정만 있으면 **웹 브라우저(크롬 등)** 에서 바로 실행됩니다.

* Pandas, NumPy, TensorFlow, PyTorch 등 주요 라이브러리가 이미 설치되어 있습니다.

### 3. 실시간 협업 및 공유

구글 문서(Google Docs)를 공유하듯, 작성한 코드 파일을 링크 하나로 다른 사람과 공유할 수 있습니다. 동료와 동시에 같은 코드를 보며 수정하는 것도 가능합니다.

### 4. 구글 드라이브 연동

작성한 코드는 구글 드라이브에 자동 저장되며, 드라이브에 올려둔 데이터셋을 불러와서 분석하는 것도 매우 간편합니다.

---

## 어떻게 작동하나요?

콜랩은 **Jupyter Notebook**이라는 형식을 기반으로 합니다. 코드만 적는 게 아니라 설명(텍스트), 이미지, 그래프를 한곳에 모아 '문서'처럼 만들 수 있습니다.

* **코드 셀(Code Cell):** 실제 파이썬 코드를 입력하고 실행하는 공간입니다.
* **텍스트 셀(Text Cell):** 마크다운(Markdown)을 사용하여 코드에 대한 설명을 작성하는 공간입니다.

---

> **알아두면 좋은 점:**
> 무료 버전은 일정 시간(약 12시간)이 지나거나 브라우저를 오래 닫아두면 세션이 종료되어 작업 중이던 데이터가 사라질 수 있습니다. 중요한 결과물은 항상 구글 드라이브에 저장하는 습관이 필요합니다!

## 구글 콜랩에서 첫 번째 코드를 실행

### 1단계: 콜랩 접속하기

1. 웹 브라우저에서 [Google Colab](https://colab.research.google.com/)에 접속합니다.
2. 구글 계정으로 로그인합니다.
3. 팝업창이 뜨면 좌측 하단의 **[새 노트]** 버튼을 클릭합니다.

---

### 2단계: 코드 입력하고 실행하기

새 노트가 열리면 화면에 긴 직사각형 박스가 보일 거예요. 이 박스를 **'코드 셀(Code Cell)'** 이라고 부릅니다.

1. 코드 셀에 아래 내용을 복사해서 붙여넣거나 직접 타이핑해 보세요.

```python
name = "Colab"
print(f"Hello, {name}! 첫 번째 코드 실행에 성공했습니다.")

```

2. 셀 왼쪽의 **재생 버튼(▶️)** 을 누르거나, 키보드 단축키 **`Ctrl + Enter`** 를 누릅니다.
3. 셀 바로 아래에 결과 메시지가 출력되는 것을 확인하세요!

---

### 3단계: (선택) 하드웨어 가속기(GPU) 설정하기

딥러닝이나 복잡한 연산을 할 때 필요한 GPU를 활성화하는 방법입니다.

1. 우측 하단에 런타임 옵션을 클리하면 팝업이 뜨는데, 런타임 유형 변경을 클릭합니다.
2. **'하드웨어 가속기'** 메뉴에서 **[T4 GPU]** 를 선택합니다.
3. **[저장]** 버튼을 누르면, 이제부터 여러분의 코드는 구글의 고성능 그래픽 카드에서 돌아가게 됩니다!

---

### 단축키

콜랩을 훨씬 빠르게 사용하는 핵심 단축키 3가지만 기억해 두세요.

| 단축키 | 기능 |
| --- | --- |
| **`Ctrl + Enter`** | 선택한 셀 실행 |
| **`Shift + Enter`** | 셀 실행 후 다음 셀로 이동 (가장 많이 씀!) |
| **`Alt + Enter`** | 셀 실행 후 아래에 새로운 셀 추가 |

---

## 구글 드라이브 연동

구글 드라이브에 있는 CSV 파일을 코랩(Colab)으로 불러와 간단한 그래프를 그리는 방법은 크게 **1) 구글 드라이브 마운트(연결)**, **2) Pandas로 CSV 로딩**, **3) Matplotlib/Seaborn으로 시각화**의 3단계로 나뉩니다.

아래의 순서대로 코드를 실행해 보세요.

---

### 1단계: 구글 드라이브와 코랩 연결하기 (Mount)

가장 먼저 코랩이 내 구글 드라이브의 파일에 접근할 수 있도록 허용해야 합니다.

```python
from google.colab import drive
drive.mount('/content/drive')

```

* 위 코드를 실행하면 팝업창이 뜹니다. 드라이브 접근 권한을 **[허용]** 해 주세요.
* 완료되면 코랩 왼쪽의 폴더 아이콘을 눌렀을 때 `drive`라는 폴더가 보입니다.

---

### 2단계: CSV 파일 경로 복사 및 로딩

1. 왼쪽 폴더 메뉴에서 `drive` > `MyDrive` 폴더로 들어가 step7/data/power_usage_dataset.csv 파일을 업로드 합니다.
2. 파일 이름 오른쪽 옆의 **점 세 개(⋮)** 버튼을 누르고 **[경로 복사]** 를 클릭합니다.
3. 아래 코드의 `파일경로` 부분에 붙여넣기 하여 파일을 읽어옵니다.

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Input

# 1. 데이터 로드 및 정렬
df = pd.read_csv('/content/drive/MyDrive/power_usage_dataset.csv')
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
history = model.fit(X_train, y_train, epochs=50, batch_size=16, validation_split=0.1, verbose=1)

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

### 3단계: 간단한 그래프 그리기 (시각화)

![alt text](image-9.png)

---

### 4단계: GPU로 변경하고 실행 시간을 확인합니다 

---

## colab에서 사용하는 T4 gpu 사양

코랩(Colab)에서 무료 티어 사용자에게 주로 할당되는 **NVIDIA Tesla T4**는 딥러닝 입문과 중급 수준의 프로젝트에 최적화된 가성비 높은 GPU입니다.

"**학습 속도는 일반 PC의 보급형~중급 그래픽카드 수준이지만, 넉넉한 메모리 덕분에 더 큰 인공지능 모델을 돌릴 수 있다**" 고 요약할 수 있습니다.

---

### T4 GPU 주요 사양 요약

| 사양 | 상세 내용 | 비고 |
| --- | --- | --- |
| **아키텍처** | Turing (튜링) | RTX 20 시리즈와 같은 세대 |
| **비디오 메모리(VRAM)** | **16 GB** (GDDR6) | 대규모 데이터 처리에 유리 |
| **CUDA 코어** | 2,560개 | 연산 병렬 처리를 담당 |
| **텐서 코어(Tensor Cores)** | 320개 | AI 연산 가속 전용 코어 |
| **연산 성능 (FP16)** | 약 65 TFLOPS | 혼합 정밀도 연산 시 매우 빠름 |

---

### 다른 GPU와의 체감 성능 비교

실제 사용자들이 느끼는 T4의 성능은 우리가 흔히 쓰는 PC용 그래픽카드와 비교하면 다음과 같습니다.

1. **RTX 3060 ~ 3070 사이:** 순수한 연산 속도만 놓고 보면 데스크탑용 **RTX 3060**과 비슷하거나 상황에 따라 약간 느린 수준입니다. 하지만 전력 효율에 최적화된 모델이라 일반 게임용 카드보다는 절대적인 처리 속도가 낮을 수 있습니다.
2. **메모리의 강점:** 게임용 그래픽카드(보통 8GB~12GB)보다 많은 **16GB의 VRAM**을 가지고 있습니다. 덕분에 최신 LLM(거대언어모델)이나 고해상도 이미지 생성 AI(Stable Diffusion 등)를 실행할 때 메모리 부족(Out of Memory) 오류가 훨씬 적게 발생합니다.
3. **학습(Training) vs 추론(Inference):** T4는 원래 '추론(이미 만든 AI를 실행하는 것)'에 특화되어 설계되었습니다. 하지만 코랩 환경에서는 웬만한 딥러닝 모델의 '학습'에도 충분히 훌륭한 성능을 보여줍니다.

---

### T4 GPU로 할 수 있는 것들

* **컴퓨터 비전:** YOLO 등을 활용한 객체 탐지 모델 학습
* **자연어 처리(NLP):** BERT, GPT-2 급의 모델 파인튜닝(Fine-tuning)
* **이미지 생성:** Stable Diffusion을 이용한 이미지 생성 및 간단한 LoRA 학습
* **LLM 실습:** Llama-3 (8B) 같은 모델을 양자화(4-bit)하여 구동하기

> "내 컴퓨터가 맥북 에어이거나 그래픽카드가 없는 사무용 노트북이라도, T4를 연결하는 순간 **수백만 원대 워크스테이션급의 AI 개발 환경**을 무료로 갖게 되는 셈입니다."

더 강력한 성능이 필요하시다면 코랩 유료 버전(Pro/Pro+)에서 제공하는 **L4**나 **A100** GPU를 고려해 볼 수 있습니다.