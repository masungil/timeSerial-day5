# 최신 GPU를 WSL2(Ubuntu 22.04)에서 구동하기 위한 절차

RTX 같은 최신 GPU를 WSL2(Ubuntu 22.04)에서 구동하기 위한 절차는 **Host(Windows)** 와 **Guest(Ubuntu)** 단계로 진행합니다.

---

## 1단계: Host(Windows) 시스템 준비

WSL2에서 GPU를 쓰기 위해서는 하드웨어를 직접 제어하는 Windows 측의 설정이 가장 먼저 선행되어야 합니다.

1. **NVIDIA 드라이버 설치/업데이트**: [NVIDIA 공식 홈페이지](https://www.nvidia.com/Download/index.aspx)에서 RTX 최신 **Game Ready** 또는 **Studio** 드라이버를 다운로드하여 설치합니다.
2. **WSL 가상화 기능 활성화**:
* `제어판 > 프로그램 및 기능 > Windows 기능 켜기/끄기`에서 **Linux용 Windows 하위 시스템**과 **가상 머신 플랫폼**이 체크되어 있는지 확인합니다.

* **PowerShell** 명령어를 사용하면 훨씬 빠르고 정확하게 확인할 수 있습니다.

* **관리자 권한**으로 PowerShell을 열고 아래 명령어를 입력하세요.

```powershell
# WSL 및 가상 머신 플랫폼 활성화 상태 확인
Get-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux
Get-WindowsOptionalFeature -Online -FeatureName VirtualMachinePlatform

```

* **State가 `Enabled`인 경우**: 이미 켜져 있는 상태입니다.
* **State가 `Disabled`인 경우**: 꺼져 있으므로 활성화가 필요합니다.

* 명령어로 즉시 활성화하기 (필요한 경우) 만약 확인 결과가 `Disabled`라면, 제어판에 들어갈 필요 없이 아래 명령어로 즉시 활성화할 수 있습니다.

```powershell
# 1. WSL 활성화
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart

# 2. 가상 머신 플랫폼 활성화
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

```

> **주의**: 이 명령어를 실행한 후에는 시스템을 반드시 **재부팅**해야 설정이 완전히 적용됩니다.

---

* 현재 설치된 WSL이 **버전 2**로 작동하는지도 확인해두는 것이 좋습니다. (RTX 최신 GPU 가속은 반드시 버전 2여야 합니다.)

```powershell
wsl -l -v

```

* 앞으로 설치할 모든 리눅스 배포판이 자동으로 버전 2로 설치되도록 전역 설정을 변경합니다.

```powershell
wsl --set-default-version 2

```

---

## 2단계: WSL2 Ubuntu 22.04 설치

PowerShell(관리자 권한)에서 특정 버전을 지정하여 설치합니다.

1. **Ubuntu 22.04 설치**:
```powershell
wsl --install -d Ubuntu-22.04

```

2. **계정 설정**: 설치 완료 후 뜨는 터미널 창에서 사용자 `Username`과 `Password`를 입력합니다.
3. **버전 확인**: PowerShell에서 `wsl -l -v`를 입력하여 Ubuntu-22.04의 VERSION이 **2**인지 확인합니다. 만약 1이라면 `wsl --set-version Ubuntu-22.04 2`로 변경해 줍니다.

---

## 3단계: Ubuntu 22.04 내부 설치 절차

이제 Ubuntu 터미널 내에서 GPU 연산 환경을 구축합니다.

### ① 시스템 업데이트 및 기본 도구 설치

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y build-essential pkg-config

```

### ② Miniconda 설치 (가상환경 관리)

```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
# 약관 동의(yes) 및 설치 후 터미널 재시작
source ~/.bashrc

```

### ③ NVIDIA CUDA 저장소 등록 및 툴킷 설치

RTX 최신 아키텍처에서는 CUDA 12.x 버전을 권장합니다.

```bash
wget https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt update
sudo apt -y install cuda-toolkit-12-3

```

### ④ 가상환경 생성 및 TensorFlow 설치

```bash
# 약관 동의가 필요한 경우 미리 수행
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r

# tf_gpu 가상 환경 생성 및 진입(활성화)
conda create -n tf_gpu python=3.10 -y
conda activate tf_gpu

# TensorFlow 및 RTX 40 이하 GPU 가속 패키지 설치시 아래 명령 실행합니다 
pip install tensorflow[and-cuda]

# TensorFlow 및 RTX 50XX 이상 GPU 가속 패키지 설치시 아래 명령 실행합니다 
pip install tensorflow[and-cuda]==2.21.0rc0

```

### ⑤ 환경 변수 설정 (중요: 라이브러리 인식)

가상환경을 켤 때마다 라이브러리 경로를 자동으로 잡도록 설정합니다.

```bash
mkdir -p $CONDA_PREFIX/etc/conda/activate.d
echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CONDA_PREFIX/lib/' > $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh
conda deactivate
conda activate tf_gpu

```

---

## 4단계: 최종 점검 및 실행

가상환경 내에서 아래 코드를 실행하여 RTX XXXX(GPU:0)이 잡히는지 확인합니다.

```bash
python -c "import tensorflow as tf; print('✅ 사용 가능한 GPU:', tf.config.list_physical_devices('GPU'))"

```

**⚠️ 주의사항:** RTX 최신 칩셋의 경우 첫 학습 시 **JIT 컴파일** 메시지와 함께 초기 지연이 발생할 수 있습니다. 이는 고장이나 멈춤이 아니니 약 10~20분 정도 기다려 주시면 이후부터는 초고속으로 작동합니다.

이 과정을 "**길들이기(Warming up)**"라고 합니다. 한 번 완료되면 컴파일된 결과가 캐시에 저장되어 다음부터는 즉시 실행됩니다.

---

### 🚀 첫 학습(JIT 컴파일용) 워밍업 예제 코드

이 코드는 실제 복잡한 데이터를 돌리기 전에 GPU에게 "공부할 시간"을 주는 간단한 예제입니다. 이 코드를 실행하고 **최대 20~30분 정도** 아무 반응이 없더라도 절대 끄지 마세요.

파일명 : warming_up.py
```python
import os

# CUDA 컴파일 관련 캐시 및 설정을 강제합니다.
# TF_CPP_MIN_LOG_LEVEL '2': 경고(Warning)와 에러(Error) 메시지만 표시하여 출력을 깔끔하게 유지합니다.
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
# TF_FORCE_GPU_ALLOW_GROWTH 'true': GPU 메모리를 필요한 만큼만 동적으로 할당하게 합니다.
os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'

import tensorflow as tf
from tensorflow.keras import layers, models, Input
import numpy as np

# 시스템의 물리적 GPU 장치 목록을 확인합니다.
gpu_devices = tf.config.list_physical_devices('GPU')
if gpu_devices:
    try:
        # RTX 50 시리즈와 같은 최신 그래픽카드는 초기 메모리 점유 방식에 민감하므로 필수 설정입니다.
        # 이 설정을 통해 런타임 중에 메모리 할당량을 점진적으로 늘립니다.
        tf.config.experimental.set_memory_growth(gpu_devices[0], True)
        print("✅ RTX 50XX GPU 메모리 설정 완료")
    except RuntimeError as e:
        # 프로그램 실행 도중에 설정을 변경하려고 하면 에러가 발생할 수 있습니다.
        print(f"❌ GPU 설정 에러: {e}")

# 매우 간단한 Sequential 모델 정의 (테스트용)
# 입력 데이터 형태(Input shape)를 정의하고 밀집층(Dense)을 쌓습니다.
model = models.Sequential([
    Input(shape=(10,)),                 # 10개의 특성을 가진 입력 데이터
    layers.Dense(64, activation='relu'), # 64개 노드를 가진 은닉층 (ReLU 활성화 함수)
    layers.Dense(1)                      # 출력층 (단일 값 예측)
])

# 모델 컴파일: 최적화 도구(Adam)와 손실 함수(Mean Squared Error) 설정
model.compile(optimizer='adam', loss='mse')

# 테스트를 위한 무작위(Random) 데이터 생성
# 1000개의 샘플과 10개의 특성을 가진 학습 데이터 생성
x_train = np.random.random((1000, 10))
y_train = np.random.random((1000, 1))

print("🚀 학습 시작 (GPU 연산 확인 및 컴파일 유도)...")

# 모델 학습 실행 (Warming Up)
# 실제 GPU 내부에서 연산 그래프가 생성되고 실행되는지 확인하는 단계입니다.
# verbose=1: 학습 진행 상황을 실시간으로 확인합니다.
model.fit(x_train, y_train, epochs=5, batch_size=32, verbose=1)

print("\n🎉 축하합니다! TensorFlow가 GPU(RTX 50XX)에서 정상적으로 학습을 수행합니다!")
```

---

## 5단계: VC code을 사용하여 실행하는 방법

Windows 11에 저장된 소스 코드를 WSL2(Ubuntu 22.04) 환경의 GPU로 실행하는 것은 매우 효율적인 개발 방식입니다. VS Code의 **Remote - WSL** 확장을 사용하면 윈도우의 편리함과 리눅스의 GPU 성능을 동시에 누릴 수 있습니다.

---

### 1. VS Code 확장 프로그램 설치 (Windows 측)

가장 먼저 VS Code가 WSL2 내부와 통신할 수 있도록 다리를 놓아주어야 합니다.

1. Windows에서 VS Code를 실행합니다.
2. 왼쪽 사이드바의 **Extensions(확장)** 아이콘(사각형 모양)을 클릭합니다.
3. "**WSL**"을 검색하여 Microsoft에서 만든 **WSL 확장 프로그램** 을 설치합니다. (예전 이름은 Remote - WSL입니다.)

---

### 2. WSL2 Ubuntu 터미널에서 프로젝트 폴더 열기

윈도우 폴더에 있는 소스를 WSL로 연결하는 가장 쉬운 방법은 터미널 명령어를 사용하는 것입니다.

1. **Ubuntu 22.04 터미널**을 실행합니다.
2. 윈도우의 특정 폴더로 이동합니다. WSL2에서 윈도우 드라이브는 `/mnt/` 아래에 마운트되어 있습니다.
* 예: 윈도우 `C:\Users\Name\Projects` 폴더인 경우:
```bash
cd /mnt/c/Users/Name/Projects

```

3. 해당 폴더에서 VS Code를 실행합니다.
```bash
code .

```

4. 잠시 기다리면 VS Code 창이 새로 뜨면서 왼쪽 하단 파란색 바에 "**WSL: Ubuntu-22.04**" 라고 표시됩니다. 이제 VS Code는 리눅스 환경 내부에서 동작하는 상태가 되었습니다.

---

### 3. 내 가상환경(Interpreter) 설정

소스 코드가 열렸다면, 앞서 만든 `tf_gpu` 가상환경을 VS Code에 연결해야 합니다.

1. 콘솔에 가상환경(Interpreter) 설정
2. vscode에 가상환경(Interpreter) 설정

두가지 방법 중 편한것을 사용하시면 됩니다

#### 콘솔에 가상환경(Interpreter) 설정

1. VS Code 상단 메뉴에서 `Terminal > New Terminal`을 열어 하단 터미널이 뜨게 합니다.
2. 터미널에 `conda activate tf_gpu`를 입력하여 가상환경이 tf_gpu가 되게 설정합니다.
3. 터미널에 아래와 같이 나오는지 확인합니다
```bash
(tf_gpu) 계정명@호스트명:소스폴더$ 
```

#### vscode에 연결

1. **Python 인터프리터 선택**:
* 단축키 `Ctrl + Shift + P`를 누릅니다.
* "**Python: Select Interpreter**"를 입력하고 선택합니다.
* 목록에서 `Python 3.10.x ('tf_gpu': conda)`를 찾아 클릭합니다.

2. 이제 VS Code 오른쪽 하단에 가상환경 이름이 표시되며, 코드 작성 시 자동 완성 및 디버깅이 이 환경을 기준으로 작동합니다.

---

## 6단계 코드 실행 및 GPU 확인

소스 코드 파일(예: `warming_up.py`)을 열고 실행합니다.

1. 코드 상단에 제가 드린 **JIT 컴파일 워밍업 코드** 또는 **GPU 확인 코드**를 넣습니다.
2. 터미널에서 직접 실행합니다.
```bash
python warming_up.py


```

3. **성공 확인**
```bash
...(로그 생략)
✅ RTX 50XX GPU 메모리 설정 및 Autotuner 비활성화 완료
🚀 학습 시작 (가속 기능 제외 안전 모드)...
Epoch 1/5
32/32 ━━━━━━━━━━━━━━━━━━━━ 2s 18ms/step - loss: 0.1116
Epoch 2/5
32/32 ━━━━━━━━━━━━━━━━━━━━ 0s 2ms/step - loss: 0.0956
Epoch 3/5
32/32 ━━━━━━━━━━━━━━━━━━━━ 0s 2ms/step - loss: 0.0916
Epoch 4/5
32/32 ━━━━━━━━━━━━━━━━━━━━ 0s 2ms/step - loss: 0.0909
Epoch 5/5
32/32 ━━━━━━━━━━━━━━━━━━━━ 0s 3ms/step - loss: 0.0881

🎉 축하합니다! TensorFlow가 RTX 50XX에서 작동합니다!
```

4. 만약 설치된  gpu가 RTX 50 계열이면 **RTX 50(Blackwell)** 은 최소 **CUDA 12.6.3 이상** 의 컴파일러가 필요합니다, 만약 시스템(WSL2)에 설치된 CUDA 툴킷이 그보다 낮은 **12.3** 버전이라 하드웨어에 맞는 실행 파일을 생성하지 못할 수 있습니다.
그러면  **WSL2 내부의 CUDA 툴킷 자체를 업데이트** 해야 합니다.

---

### 근본적인 해결책: WSL2용 CUDA 12.8 설치

현재 설치된 `conda` 환경의 CUDA 라이브러리보다 시스템 레벨의 CUDA가 우선시되거나 충돌할 수 있습니다. 아래 명령어로 WSL2용 최신 드라이버 지원 툴킷을 설치해 보세요.

**1. 기존 충돌 가능성 있는 패키지 정리**

```bash
conda activate tf_gpu
pip uninstall tensorflow tf-nightly -y

```

**2. WSL2 Ubuntu 터미널에서 CUDA 12.8 설치 (NVIDIA 공식)**
아래 명령어를 한 줄씩 복사해서 실행하세요. (Ubuntu 22.04 기준)

```bash
wget https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt-get update
sudo apt-get -y install cuda-toolkit-12-8

```

**3. TensorFlow Re-install (rtx 50XX 최신 GPU 가속)**

```bash
pip install tf-nightly[and-cuda]==2.21.0rc0

```

---

## 7단계. Ubuntu에 나눔 폰트 설치

---

### 1.  폰트 설치

WSL2(Linux) 환경에서 Windows에 설치된 한글 폰트를 사용하려고 할 때 발생하는 전형적인 문제입니다. **Linux 시스템 자체에 해당 폰트 파일이 없거나, Matplotlib이 리눅스용 폰트 캐시를 갱신하지 못했기 때문**입니다.

리눅스 환경에서는 '맑은 고딕'보다 **나눔 폰트**를 설치하여 사용하는 것이 가장 안정적입니다. 터미널에서 다음 명령어를 입력하세요.

```bash
# 1. 폰트 설치
sudo apt-get update
sudo apt-get install -y fonts-nanum

# 2. 폰트 캐시 갱신
sudo fc-cache -fv

```

### 2. Matplotlib 폰트 캐시 삭제

폰트를 설치해도 Matplotlib은 기존의 폰트 리스트를 기억하고 있어 한글을 못 불러올 수 있습니다. 캐시 파일을 강제로 지워야 합니다.

```bash
# 터미널에서 실행
rm -rf ~/.cache/matplotlib

```

### 3. 코드 수정 (폰트 설정 부분)

설치한 **NanumGothic**으로 코드를 변경합니다.

```python
# [단계 6] 결과 시각화 부분 수정
import matplotlib.pyplot as plt

# 폰트 설정 (나눔고딕)
plt.rcParams['font.family'] = 'NanumGothic'
plt.rcParams['axes.unicode_minus'] = False 

# ... 나머지 시각화 코드

```

pyTorch 라이브러리를 사용하여 GPU 사용여부 확인할 수 있는 예제는 test_gpu_pyTorch.py 파일 참고 하세요.

tensorflow 라이브러리를 사용하여 GPU 사용여부 확인할 수 있는 예제는 test_gpu_tensorFlow.py 파일 참고 하세요. 
