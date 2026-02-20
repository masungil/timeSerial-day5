# 5. Human Activity Recognition(행동 인식)

## 1. Human Activity Recognition(행동 인식) 란?

**Human Activity Recognition (HAR)**, 즉 **행동 인식**은 인공지능과 센서 기술을 활용하여 사람이 어떤 행동을 하고 있는지(예: 걷기, 달리기, 수면, 요리 등)를 자동으로 식별하고 분석하는 기술입니다.

단순히 "움직임이 있다"를 넘어, "어떤 의도의 움직임인가"를 파악하는 것이 핵심입니다.

---

### 1. 행동 인식의 작동 원리 (Process)

HAR 시스템은 일반적으로 다음과 같은 파이프라인을 거쳐 작동합니다.

1. **데이터 수집 (Data Acquisition):** 센서나 카메라를 통해 원시 데이터를 수집합니다.
2. **전처리 (Pre-processing):** 노이즈를 제거하고 데이터를 정규화합니다.
3. **특징 추출 (Feature Extraction):** 데이터에서 행동을 구분할 수 있는 핵심 특징(가속도 변화량, 관절의 각도 등)을 뽑아냅니다.
4. **모델 학습 및 분류 (Classification):** 머신러닝/딥러닝 알고리즘이 특징을 분석해 "달리기" 또는 "앉기" 등으로 최종 판정을 내립니다.

---

### 2. 주요 데이터 소스 (방법론)

어떤 도구를 사용하느냐에 따라 크게 두 가지로 나뉩니다.

#### ① 센서 기반 (Sensor-based)

스마트폰, 스마트워치, 또는 몸에 부착하는 웨어러블 기기를 이용합니다.

* **사용 센서:** 가속도계(Accelerometer), 자이로스코프(Gyroscope), 심박수 센서 등.
* **장점:** 장소 제약이 적고 프라이버시 침해 우려가 낮습니다.
* **예시:** 애플워치의 낙상 감지 기능, 스마트폰의 걸음 수 측정.

#### ② 비전 기반 (Vision-based)

카메라나 CCTV 영상을 분석하여 행동을 인식합니다.

* **기술:** 포즈 추정(Pose Estimation), 객체 추적(Object Tracking).
* **장점:** 복잡한 상호작용(예: 물건을 주고받는 행동)을 파악하기 유리합니다.
* **예시:** 홈 트레이닝 앱의 자세 교정, 무인 매장의 이상 행동 감지.

---

### 3. 주요 활용 분야

행동 인식 기술은 현재 우리 삶의 다양한 영역에서 쓰이고 있습니다.

* **헬스케어:** 고독사 방지를 위한 노인 활동 모니터링, 수면 패턴 분석.
* **스포츠:** 선수의 폼(Form) 분석 및 부상 방지, 자동 기록 측정.
* **보안 및 안전:** 공공장소에서의 폭행/배회 감지, 산업 현장에서의 위험 행동 알람.
* **스마트 홈:** 사용자의 행동에 맞춰 조명이나 가전을 조절하는 자동화 시스템.

---

### 4. 핵심 기술 (Deep Learning)

최근에는 수작업으로 특징을 뽑지 않고, **Deep Learning** 모델이 스스로 학습하는 방식이 주류입니다.

* **CNN (Convolutional Neural Networks):** 이미지나 센서 데이터의 공간적 패턴 인식에 탁월합니다.
* **RNN / LSTM:** 시간의 흐름(시계열 데이터)이 중요한 행동 분석에 사용됩니다.
* **Transformer:** 최근 비전 분야에서도 각광받으며 복잡한 맥락 파악에 사용됩니다.

> **참고:** 행동 인식에서 가장 까다로운 점은 사람마다 체격이나 행동 습관이 다르기 때문에, 이를 일반화하여 정확도를 높이는 것입니다.

---

## 2. 행동 인식(HAR) 모델을 개발 위해 필요한 데이터 수집

행동 인식(HAR) 모델을 개발하거나 학습시키기 위해서는 잘 정제된 데이터셋이 필수적입니다. HAR 데이터셋은 크게 **센서 기반**과 **비전 기반**으로 나뉩니다.

---

### 1. 센서 기반 데이터셋 (Sensor-based)

스마트폰이나 웨어러블 기기에서 추출한 가속도, 자이로스코프 데이터를 포함합니다.

* **UCI HAR Dataset:** 가장 고전적이고 유명한 데이터셋입니다. 30명의 피실험자가 스마트폰을 허리에 차고 수행한 6가지 활동(걷기, 계단 오르기/내려오기, 앉기, 서기, 눕기) 데이터를 제공합니다.
* **WISDM (Wireless Sensor Data Mining):** 스마트폰을 주머니에 넣은 상태에서 수집된 데이터로, 일상적인 활동 인식 연구에 자주 쓰입니다.
* **PAMAP2:** 심박수 데이터와 여러 신체 부위(가슴, 팔, 발목)에 부착된 센서 데이터를 포함하여, 가벼운 운동부터 격렬한 운동까지 폭넓게 다룹니다.

---

### 2. 비전 기반 데이터셋 (Vision-based / Video)

카메라 영상이나 비디오 클립을 통해 행동을 분류하기 위한 데이터셋입니다.

* **UCF101:** 유튜브에서 수집한 101가지 카테고리의 행동 영상입니다. 스포츠, 악기 연주 등 역동적인 동작이 많아 비디오 분류 모델의 벤치마크로 쓰입니다.
* **HMDB51:** 영화나 유튜브 영상에서 추출한 51가지 행동 데이터를 포함하며, 조명이나 각도가 다양해 난이도가 높은 편입니다.
* **Kinetics (400/600/700):** 구글(DeepMind)에서 배포한 대규모 데이터셋입니다. 수십만 개의 짧은 유튜브 영상 클립으로 구성되어 있어, 최신 딥러닝 모델(예: Video Transformer) 학습에 필수적입니다.

---

### 3. 포즈 추정 기반 데이터셋 (Pose/Skeleton)

영상에서 관절 위치(Skeleton)만을 추출하여 행동을 분석할 때 쓰입니다.

* **NTU RGB+D:** MS Kinect 센서를 이용해 수집한 대규모 데이터셋으로, RGB 영상뿐만 아니라 3D 골격 정보(Skeleton)를 제공합니다. 사람 간의 상호작용(악수하기, 밀치기 등) 연구에 최적화되어 있습니다.

---

### 데이터셋 선택 가이드

| 용도 | 추천 데이터셋 | 특징 |
| --- | --- | --- |
| **입문용 / 모바일 앱** | UCI HAR | 데이터 크기가 적당하고 구조가 단순함 |
| **정밀 운동 분석** | PAMAP2 | 여러 부위의 센서와 심박수 포함 |
| **CCTV / 영상 보안** | Kinetics | 데이터 양이 방대하여 높은 일반화 성능 가능 |
| **상호작용 / 포즈 분석** | NTU RGB+D | 3D 관절 좌표 데이터 제공 |

---

## 3. UCI HAR 데이터셋

UCI 머신러닝 저장소(UCI Machine Learning Repository)의 공식 주소와 행동 인식 데이터셋의 직접 링크는 다음과 같습니다.

### 1. 공식 웹사이트 주소

* **메인 페이지:** [https://archive.ics.uci.edu/](https://archive.ics.uci.edu/)
* **데이터셋 검색 페이지:** [https://archive.ics.uci.edu/datasets](https://archive.ics.uci.edu/datasets)

### 2. UCI HAR 데이터셋 직접 링크

행동 인식 예제에서 사용되는 데이터셋의 상세 페이지입니다.

* **데이터셋 정보:** [Human Activity Recognition Using Smartphones](https://archive.ics.uci.edu/dataset/240/human+activity+recognition+using+smartphones)
* **데이터 직접 다운로드:** 해당 페이지 우측 상단의 **[Download]** 버튼을 누르면 `UCI HAR Dataset.zip` 파일을 받으실 수 있습니다.

---

### Python 코드로 직접 다운로드하기

수동으로 다운로드하기 번거롭다면, 파이썬의 `requests` 라이브러리를 이용해 코드로 바로 내려받고 압축을 풀 수도 있습니다.

파일명 : day5/step4/data_download.py

```python
import requests
import zipfile
import os

# 데이터셋 URL
url = "https://archive.ics.uci.edu/static/public/240/human+activity+recognition+using+smartphones.zip"
zip_name = "./data/uci_har_dataset.zip"
zip_dataset_name = "./data/UCI HAR Dataset.zip"

# 1. 폴더 경로 설정
base_dir = "./data"
dataset_dir = "./data/dataset"

# 폴더 생성 (exist_ok=True는 폴더가 이미 있으면 생성하지 않고 넘어감)
os.makedirs(dataset_dir, exist_ok=True)
print(f"폴더 생성 완료: {dataset_dir}")

# 2. 다운로드
print("데이터셋 다운로드 중...")
response = requests.get(url)
with open(zip_name, "wb") as f:
    f.write(response.content)

# 3. 압축 해제
print("압축 해제 중...")
with zipfile.ZipFile(zip_name, 'r') as zip_ref:
    zip_ref.extractall("./data")

with zipfile.ZipFile(zip_dataset_name, 'r') as zip_ref:
    zip_ref.extractall("./data/dataset")

print("준비 완료! './data' 폴더가 생성되었습니다.")

```

## 4. UCI HAR 데이터셋을 이용하여 학습 및 평가

UCI HAR 데이터셋은 행동 인식의 'Hello World'와 같습니다. 이 데이터셋은 스마트폰의 가속도계와 자이로스코프에서 추출된 **561개의 특징(feature)** 을 이미 가지고 있어, 복잡한 신호처리 없이 바로 머신러닝 모델에 입력할 수 있다는 장점이 있습니다.

입문자에게 가장 효율적인 **Random Forest(랜덤 포레스트)**  알고리즘을 사용하여 데이터를 학습하고 추론하는 전체 과정을 코드로 알아보겠습니다

---

### 1. 학습을 위한 데이터 로딩

파일명 : day5/step4/uci-har-learning.py 참조

```python

# 1. 데이터 로드 함수 정의
def load_har_data(path, group):
    # 특징값(X) 로드: 561개의 센서 데이터 특징
    X = pd.read_csv(f'{path}/{group}/X_{group}.txt', sep='\s+', header=None)
    
    # 결과값(y) 로드: 1~6 사이의 행동 라벨
    y = pd.read_csv(f'{path}/{group}/y_{group}.txt', sep='\s+', header=None)
    
    return X, y

# 데이터 경로 (UCI HAR Dataset 폴더가 있는 위치)
path = './data/dataset/UCI HAR Dataset'
model_save_path = './model/har_model.pkl'

# 학습 및 테스트 데이터 불러오기
X_train, y_train = load_har_data(path, 'train')
X_test, y_test = load_har_data(path, 'test')

# 라벨 이름 로드 (1: Walking, 2: Walking_Upstairs, ...)
labels = ["Walking", "Walking_Up", "Walking_Down", "Sitting", "Standing", "Laying"]

```

---

### 2. 모델 학습 (Training)

딥러닝 이전에 가장 강력한 성능을 내는 랜덤 포레스트를 사용합니다. 데이터의 특성이 이미 잘 추출되어 있어 머신러닝만으로도 **90% 이상의 정확도**를 얻을 수 있습니다.

```python
# 모델 생성 (결정 트리 100개를 사용하는 랜덤 포레스트)
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)

# 학습 시작
print("모델 학습 중...")
rf_model.fit(X_train, y_train.values.ravel())
print("학습 완료!")

```

---

### 3. 추론 및 성능 평가 (Inference & Evaluation)

학습된 모델이 한 번도 보지 못한 테스트 데이터를 얼마나 잘 맞히는지 확인합니다.

```python
# 추론 (Inference)
y_pred = rf_model.predict(X_test)

# 성능 리포트 출력
print(f"전체 정확도: {accuracy_score(y_test, y_pred):.4f}")
print("\n[행동별 분류 성능]")
print(classification_report(y_test, y_pred, target_names=labels))

```

---

### 4. 학습한 모델 저장

```python
# 4. 모델 저장하기

model_save_path = './model/har_model.pkl'
joblib.dump(rf_model, model_save_path)
print(f"모델이 {model_save_path}에 저장되었습니다.")

```

---

### 5. 학습한 모델 로딩

```python
# 5. 모델 불러오기
loaded_model = joblib.load(model_save_path)
```

---

### 6. 실전 추론 예시 (Single Sample Inference)

만약 새로운 데이터 1건이 들어왔을 때 어떻게 동작하는지 보여주는 예시입니다.


```python
# 테스트 데이터셋에서 임의의 샘플 하나 추출
sample_idx = 100
sample_data = X_test.iloc[sample_idx].values.reshape(1, -1)
actual_label = labels[y_test.iloc[sample_idx, 0] - 1]

# 모델 추론
prediction = rf_model.predict(sample_data)
predicted_label = labels[prediction[0] - 1]

print(f"--- 단일 데이터 추론 결과 ---")
print(f"실제 행동: {actual_label}")
print(f"모델 예측: {predicted_label}")

```

---

1. 학습용 파일명 : day5/step4/uci-har-learning.py

```python
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib

# 1. 데이터 로드 함수 정의
def load_har_data(path, group):
    # 특징값(X) 로드: 561개의 센서 데이터 특징
    X = pd.read_csv(f'{path}/{group}/X_{group}.txt', sep='\s+', header=None)
    
    # 결과값(y) 로드: 1~6 사이의 행동 라벨
    y = pd.read_csv(f'{path}/{group}/y_{group}.txt', sep='\s+', header=None)
    
    return X, y

# 데이터 경로 (UCI HAR Dataset 폴더가 있는 위치)
path = './data/dataset/UCI HAR Dataset'

# 학습 및 테스트 데이터 불러오기
X_train, y_train = load_har_data(path, 'train')
X_test, y_test = load_har_data(path, 'test')

# 라벨 이름 로드 (1: Walking, 2: Walking_Upstairs, ...)
labels = ["Walking", "Walking_Up", "Walking_Down", "Sitting", "Standing", "Laying"]

# 2. 모델 학습 (Training)
# 모델 생성 (결정 트리 100개를 사용하는 랜덤 포레스트)
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)

# 학습 시작
print("모델 학습 중...")
rf_model.fit(X_train, y_train.values.ravel())
print("학습 완료!")

# 3. 추론 및 성능 평가 (Inference & Evaluation)
# 추론 (Inference)
y_pred = rf_model.predict(X_test)

# 성능 리포트 출력
print(f"전체 정확도: {accuracy_score(y_test, y_pred):.4f}")
print("\n[행동별 분류 성능]")
print(classification_report(y_test, y_pred, target_names=labels))

# 4. 모델 저장하기
model_save_path = './model/har_model.pkl'
joblib.dump(rf_model, model_save_path)
print(f"모델이 {model_save_path}에 저장되었습니다.")

```

2. 예측용 파일명 : day5/step4/uci-har-inference.py

```python
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib

# 1. 데이터 로드 함수 정의
def load_har_data(path, group):
    # 특징값(X) 로드: 561개의 센서 데이터 특징
    X = pd.read_csv(f'{path}/{group}/X_{group}.txt', sep='\s+', header=None)
    
    # 결과값(y) 로드: 1~6 사이의 행동 라벨
    y = pd.read_csv(f'{path}/{group}/y_{group}.txt', sep='\s+', header=None)
    
    return X, y

# 데이터 경로 (UCI HAR Dataset 폴더가 있는 위치)
path = './data/dataset/UCI HAR Dataset'
model_save_path = './model/har_model.pkl'

# 테스트 데이터 불러오기
X_test, y_test = load_har_data(path, 'test')

# 라벨 이름 로드 (1: Walking, 2: Walking_Upstairs, ...)
labels = ["Walking", "Walking_Up", "Walking_Down", "Sitting", "Standing", "Laying"]

# 2. 모델 불러오기
loaded_model = joblib.load(model_save_path)

# 3. 추론 및 성능 평가 (Inference & Evaluation)
# 추론 (Inference)
y_pred = loaded_model.predict(X_test)
print("저장된 모델로 추론에 성공했습니다.")

# 성능 리포트 출력
print(f"전체 정확도: {accuracy_score(y_test, y_pred):.4f}")
print("\n[행동별 분류 성능]")
print(classification_report(y_test, y_pred, target_names=labels))


#4. 실전 추론 예시 (Single Sample Inference)
# 테스트 데이터셋에서 임의의 샘플 하나 추출
sample_idx = 200
sample_data = X_test.iloc[sample_idx].values.reshape(1, -1)
actual_label = labels[y_test.iloc[sample_idx, 0] - 1]

# 모델 추론
prediction = loaded_model.predict(sample_data)
predicted_label = labels[prediction[0] - 1]

print(f"--- 단일 데이터 추론 결과 ---")
print(f"실제 행동: {actual_label}")
print(f"모델 예측: {predicted_label}")

```

---

실행결과

```PowerShell
저장된 모델로 추론에 성공했습니다.
전체 정확도: 0.9257

[행동별 분류 성능]
              precision    recall  f1-score   support

     Walking       0.89      0.97      0.93       496
  Walking_Up       0.90      0.89      0.89       471
Walking_Down       0.97      0.87      0.91       420
     Sitting       0.91      0.89      0.90       491
    Standing       0.90      0.92      0.91       532
      Laying       1.00      1.00      1.00       537

    accuracy                           0.93      2947
   macro avg       0.93      0.92      0.92      2947
weighted avg       0.93      0.93      0.93      2947

--- 단일 데이터 추론 결과 ---
실제 행동: Sitting
모델 예측: Sitting
```