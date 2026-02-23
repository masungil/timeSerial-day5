# VS Code에서 파이썬 개발을 바로 시작할 수 있도록 하는 표준 설정 방법

## 1. Python 설치

### 1-1. Python 다운로드

* 공식 사이트: [https://www.python.org](https://www.python.org)
* **권장 버전**: Python 3.10 이상 (3.11 / 3.12도 OK)

⚠️ **중요**
설치 시 반드시 아래 체크!

> ☑ Add Python to PATH

### 1-2. 설치 후 확인

터미널(cmd / PowerShell)에서:

```bash
python --version
Python 3.12.12
```

---

## 2. VS Code 설치

### 2-1. 다운로드

* [https://code.visualstudio.com/](https://code.visualstudio.com/)

### 2-2. 설치 옵션 (권장)

> ☑ PATH 추가
>
> ☑ 우클릭 "Code로 열기"

---

## 3. VS Code 필수 확장(Extension) 설치

VS Code 실행 → **Extensions (Ctrl + Shift + X)**

### 🔹 필수 확장 3개

1. **Python** (Microsoft)
2. **Pylance** (자동 설치됨)
3. **Python Debugger** (자동 설치됨)

---

## 4. Python 인터프리터 선택

1. `Ctrl + Shift + P`
2. `Python: Select Interpreter`
3. 설치된 Python 버전 선택

---

## 5. 프로젝트 폴더 생성 & 열기

```text
day1/step1/
 └─ main.py
```

VS Code에서:

> File → Open Folder → day1/step1

---

## 6. **파이썬 가상환경(Virtual Environment)**

**파이썬 가상환경(Virtual Environment)** 이란, 동일한 컴퓨터 내에서 프로젝트별로 **독립된 파이썬 실행 환경**을 만드는 것입니다.

컴퓨터라는 큰 집 안에 여러 개의 **특수 목적용 방**을 만든다고 생각하시면 됩니다.

여러분이 요리사라고 가정했을 때, 거실 한복판(시스템 기본 환경)에서 모든 요리를 하면 재료가 뒤섞여 엉망이 될 것입니다. 그래서 목적에 맞는 **방**을 따로 만듭니다.

1. 한식 전용 방 (Project A)
  * **방 안의 도구:** 가스레인지, 뚝배기, 고추장 (Python 3.8, Pandas 1.0)
  * 이 방에서는 오직 한식만 만듭니다. 여기서 고추장을 다 써버려도 옆 방에는 아무런 영향이 없습니다.

2. 베이킹 전용 방 (Project B)

  * **방 안의 도구:** 오븐, 거품기, 강력분 (Python 3.11, PyTorch 2.0)
  * 이 방은 베이킹을 위해 온도를 다르게 설정하고 도구도 다르게 갖춰져 있습니다. 한식 방에 오븐이 없어도 상관 없습니다. 오븐은 빵을 만드는 곳에서 있으면 됩니다

3. 왜 방을 따로 쓰나요?

  * **벽(Isolation)이 있기 때문입니다:** 한식 방에서 요리하다가 실수로 물을 쏟아도(라이브러리 충돌), 옆에 있는 베이킹 방의 밀가루는 젖지 않습니다. 문제가 생기면 그 방만 깨끗이 치우거나 **방 자체를 허물고(삭제)** 다시 만들면 끝입니다.
  * **이사(Deployment)가 쉽습니다:** 친구가 "네가 만든 빵 나도 만들고 싶어!"라고 하면, 베이킹 방에 있는 **도구 목록(requirements.txt)** 만 적어서 보내주면 됩니다. 친구는 그 목록대로 자기 집에 똑같은 방을 꾸미기만 하면 같은 맛의 빵을 만들 수 있습니다.
  * **시스템 기본 환경(System)의 평화:** 거실(컴퓨터 기본 설정)은 항상 깨끗하게 유지됩니다. 지저분한 작업은 모두 닫힌 방 안에서만 이루어지니까요.

4. 요약

  * **방 만들기:** `conda create` 또는 `venv` (새 방 공사 시작)
  * **방 들어가기:** `activate` (문 열고 들어가기)
  * **방 안에서 요리하기:** `pip install` (방 안에 가구 들여놓기)
  * **방 나오기:** `deactivate` (불 끄고 문 잠그기)

---

5. 주요 가상환경 도구들

어떤 도구를 쓰느냐에 따라 관리 방식이 조금씩 다릅니다.

| 도구 이름 | 특징 |
| --- | --- |
| **venv** | 파이썬에 기본 내장된 도구. 가볍고 별도 설치가 필요 없음. |
| **Conda** | 아까 설명드린 도구. 파이썬 버전 자체도 프로젝트마다 다르게 설정 가능 (가장 강력). |
| **Pyenv** | 여러 버전의 파이썬 설치를 관리할 때 주로 사용. |
| **Poetry** | 패키지 의존성 관리와 배포까지 한 번에 해결하고 싶을 때 사용. |

---

### 1. 기본 가상환경 venv 사용 (표준 `venv` 기준)

터미널이나 명령 프롬프트에서 아주 간단하게 만들 수 있습니다.

1. **가상환경 생성:** `python -m venv myenv` (이름이 'myenv'인 폴더가 생깁니다)
2. **활성화:**
  * Windows: `call myenv\Scripts\activate 또는 myenv\Scripts\activate.bat`
  * Mac/Linux: `source myenv/bin/activate`
3. **패키지 설치:** `pip install requests` (이 설치는 'myenv' 안에만 설치됩니다)
4. **종료:** `deactivate`

---

### 2. Conda(콘다) 가상환경

**Conda(콘다)** 는 데이터 과학과 머신러닝 분야에서 가장 널리 쓰이는 **패키지 관리자** 이자 **가상 환경 관리 시스템** 입니다.

---

#### 1. Conda의 핵심 기능

Conda는 크게 두 가지 역할을 수행합니다.

* **패키지 관리 (Package Management):** 파이썬 라이브러리(Pandas, NumPy 등)뿐만 아니라, C, C++, R 등 다른 언어 기반의 소프트웨어도 쉽게 설치, 업데이트, 삭제해 줍니다.
* **가상 환경 관리 (Environment Management):** 프로젝트마다 요구하는 라이브러리 버전이 다를 때, 이를 독립적으로 분리해 줍니다. 예를 들어 A 프로젝트는 Python 3.8, B 프로젝트는 Python 3.11을 쓰도록 설정해도 서로 충돌하지 않습니다.

---

#### 2. 왜 Conda를 사용해야 할까?

파이썬 기본 관리자인 `pip`가 있음에도 Conda를 사용하는 이유는 다음과 같습니다.

| 특징 | pip | Conda |
| --- | --- | --- |
| **관리 대상** | 파이썬 패키지만 관리 | 파이썬 버전 및 패키지 + 시스템 레벨 라이브러리 |
| **의존성 체크** | 다소 단순함 (충돌 위험) | 매우 엄격함 (설치 전 호환성 자동 검사) |
| **언어 제약** | 파이썬 위주 | R, C, Java 등 언어 독립적 |
| **가상 환경** | `venv` 등 별도 도구 필요 | 자체 내장 (가장 강력한 기능) |

---

### 3. Conda의 종류: Anaconda vs Miniconda

Conda를 사용하기 위해 설치하는 배포판은 크게 두 가지로 나뉩니다.

* **Anaconda (아나콘다):**
  * **특징:** "전부 다 들어있는 종합 선물 세트"
  * 데이터 과학에 필요한 1,500개 이상의 패키지가 미리 설치되어 있습니다. 용량이 크지만(약 3GB+), 초보자가 시작하기에 매우 편리합니다.

* **Miniconda (미니콘다):**
  * **특징:** "최소한의 뼈대"
  * Conda 본체와 최소한의 패키지만 포함됩니다. 필요한 것만 골라 설치하고 싶은 숙련자나 용량 최적화가 필요한 서버 환경에 적합합니다.

---

#### 4. 자주 쓰는 명령어 예시

Conda를 설치한 후 터미널(또는 CMD)에서 사용하는 기본 명령어들입니다.

```bash
# 1. 'my_env'라는 이름의 새로운 가상환경 만들기 (파이썬 3.10 버전)
conda create -n my_env python=3.10

# 2. 만들어진 가상환경 목록 확인 
conda env list

# 3. 만들어진 가상환경 활성화하기
conda activate my_env

# 4. 필요한 패키지 설치하기 (예: numpy)
conda install numpy (이 설치는 'my_env' 안에만 설치됩니다)

# 5. 가상환경 종료하기
conda deactivate

```

### 4 Venv, conda 강점

#### **Venv의 강점**

* **표준화:** 파이썬을 설치하면 바로 쓸 수 있어 추가 설치가 필요 없습니다.
* **경량성:** 프로젝트마다 필요한 패키지만 담으므로 가볍고 클라우드/배포 환경(Docker 등)에 최적입니다.
* **범용성:** VS Code, PyCharm 등 대부분의 IDE에서 기본적으로 가장 잘 지원합니다.

#### **Conda의 강점**

* **의존성 해결 능력:** 서로 충돌하기 쉬운 복잡한 수학/과학 라이브러리를 설치할 때 충돌을 미리 감지하고 최적의 버전을 찾아줍니다.
* **비(非) 파이썬 라이브러리 지원:** GPU 가속을 위한 CUDA나 특정 시스템 라이브러리(FFmpeg 등)를 파이썬 패키지와 함께 한 번에 설치할 수 있습니다.
* **파이썬 버전 관리:** 여러 버전의 파이썬을 쉽게 바꿔가며 환경을 만들 수 있습니다.

### 5. 가상환경 생성 및 사용

#### 1. 터미널 가상환경 생성

**VS Code 작업 폴더** : `day1/step1`

VS Code 터미널 열기:

```
Ctrl + `
```

```bash
python -m venv .venv
```

#### 2. 터미널에서 가상환경 활성화

**Windows**

```bash
.venv\Scripts\activate
```

**macOS / Linux**

```bash
source .venv/bin/activate
```

성공 시:

```PowerShell
(venv)
```

#### 3. VS Code에 이전에 만든 가상환경 연결

```text
Ctrl + Shift + P
→ Python: Select Interpreter
→ venv 선택
```

#### 4.  VS Code에 가상환경 생성 및 연결

VS Code 터미널에서 진행하는 것을 UI에서 한번에 생성 및 연결을 할 수 있습니다

```text
Ctrl + Shift + P
→ Python: Select Interpreter 선택
+ Create Virtual Environment... 선택 
 Venv Creates a `.venv` virtual environment in the current workspace 
 Conda Creates a `.conda` Conda  environment in the current workspace 

```

원하는 Venv, Conda 를 선택합니다

```cmd
이 시스템에서 스크립트를 실행할 수 없으므로 작업폴더명\.venv\Scripts\Activate.ps1 파일을 로드할 수 없습니다. 자세한 내용은 about_Execution_Policies(https://go.microsoft.c
om/fwlink/?LinkID=135170)를 참조하십시오.
위치 줄:1 문자:3 + & C:/step1/.venv/Scripts/Activate.ps1
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : 보안 오류: (:) [    ], PSSecurityException
    + FullyQualifiedErrorId : Unauthorized   Access
```

만약 위와 같이 오류가 발생하면 PowerShell을 '관리자 권한'으로 실행합니다. 아래 명령어를 실행해주세요.

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 7. 기본 파이썬 코드 생성 및 실행

### 폴더 생성

위에 생성 했으면 생략해도 됩니다.

```PowerShell
# 폴더 생성
mkdir day1/step1
```

### 파이썬 코드 생성

파일명 : main.py

```python
print ("Hello World")
```

### ▶ 실행 방법

* 우측 상단 ▶ Run 버튼
* 또는 터미널:

```bash
python main.py
```

---

## 8. 디버깅(Debug) 설정

### 중단점 찍기

```python
a = 10
b = 20
sum = a + b
print(sum)
```

### ▶ 디버그 실행

```
F5 → Python File
```

✔ 변수, 스택, 값 실시간 확인 가능

---

## 9. VS Code 설정(생략해도 됨)

가상환경을 사용하지 않고 기본 파이썬 사용하는 방법입니다.

1. 기본 설치 경로 (찾아가는 방법)
파일 탐색기를 열고 다음 경로로 이동합니다 (사용자이름은 본인 계정명):
C:\Users\사용자이름\AppData\Local\Programs\Python\Python3x (x는 버전)
주의: AppData 폴더는 숨김 폴더이므로 탐색기 [보기] -> [표시] -> [숨긴 항목]을 체크해야 보입니다.
2. Windows 스토어 설치 버전
스토어를 통해 설치했다면, 보통 아래 경로에 설치됩니다:
C:\Users\사용자이름\AppData\Local\Microsoft\WindowsApps\

`Ctrl + ,` → Settings → JSON

```json
{
  "python.defaultInterpreterPath": "자신의 PC에 설치된 파이썬 경로/python",
  "python.analysis.typeCheckingMode": "basic",
  "python.formatting.provider": "black",
  "editor.formatOnSave": true,
  "editor.tabSize": 4
}
```

---

## 10. 코드 포맷터 & 린터 설정 (실무용)

### 설치

```bash
pip install black flake8
```

### 적용

* 저장 시 자동 정렬 (Black)
* 문법 오류 & 스타일 검사 (Flake8)

---

## 11. Jupyter Notebook

### 1. Jupyter Notebook 이란?

**Jupyter Notebook(주피터 노트북)** 은 라이브 코드, 방정식, 시각화 자료 및 설명 텍스트가 포함된 문서를 만들고 공유할 수 있는 **오픈 소스 웹 애플리케이션** 입니다.

쉽게 비유하자면, 코딩을 할 수 있는 '디지털 연습장'이나 '인터랙티브한 실험 노트'라고 생각하시면 됩니다.

---

### 2. 주요 특징

* **대화형 프로그래밍:** 코드를 한 줄 또는 블록(Cell) 단위로 실행하고, 그 결과를 즉시 확인할 수 있습니다.
* **다양한 언어 지원:** 이름의 유래이기도 한 **Ju**(Julia), **Py**(Python), **R**을 포함해 40가지 이상의 프로그래밍 언어를 지원합니다.
* **데이터 시각화:** 데이터 분석 결과를 그래프나 표 형태로 코드 바로 아래에 출력하여 직관적으로 보여줍니다.
* **문서화:** 마크다운(Markdown) 형식을 지원하여 코드에 대한 풍부한 설명이나 이론적 배경을 깔끔하게 정리할 수 있습니다.

---

### 3. 왜 사용하나요?

데이터 과학자와 개발자들이 주피터 노트북을 애용하는 이유는 다음과 같습니다.

| 장점 | 설명 |
| --- | --- |
| **가독성** | 코드와 결과물, 설명이 한곳에 있어 흐름을 파악하기 좋습니다. |
| **협업** | `.ipynb` 파일로 저장하여 다른 사람과 쉽게 공유하고 재현할 수 있습니다. |
| **교육용** | 복잡한 수식($E=mc^2$)과 코드를 병행 표기할 수 있어 교육 자료로 최적입니다. |
| **수정 용이성** | 전체 코드를 다시 실행할 필요 없이 특정 부분만 수정하고 다시 실행할 수 있습니다. |

---

### 4. 시작하는 방법

가장 대중적인 방법은 두 가지입니다.

1. **로컬 설치:** Python 배포판인 **Anaconda**를 설치하거나, 터미널에서 `pip install notebook` 명령어로 설치할 수 있습니다.
2. **클라우드 서비스:** 설치가 번거롭다면 구글에서 제공하는 **Google Colab**을 통해 웹 브라우저에서 바로 주피터 노트북 환경을 사용할 수 있습니다.

### 5. 설치

```bash
pip install notebook ipykernel
```

### 6. VS Code 확장

* **Jupyter (Microsoft)**

`.ipynb` 파일 바로 실행 가능.

아래 Jupyter Notebook을 작성하고 실행하는 방법을 알아 보겠습니다.

---

## 자주 발생하는 문제 해결

### python 인식 안될 때

* Python 재설치 해줍니다
* PATH 체크

```cmd
echo %PATH%

#실행 결과에 Python 설치 경로 확인 
C:\Python314\Scripts\;C:\Python314\;...
```

```power shell
$env:PATH

#실행 결과에 Python 설치 경로 확인 
C:\Python314\Scripts\;C:\Python314\
```

mac 또는 linux
```bash
ls /usr/bin/python* 

#실행결과 
   0 lrwxrwxrwx 1 root root       7 Jun 13  2023 /usr/bin/python -> python3
   0 lrwxrwxrwx 1 root root      10 Nov 12 12:15 /usr/bin/python3 -> python3.12
7836 -rwxr-xr-x 1 root root 8020928 Jan  8 11:30 /usr/bin/python3.12

```

### 가상환경 선택 안됨

```bash
python -m ipykernel install --user
```

### 한글 깨짐

```python
# 파일 상단
# -*- coding: utf-8 -*-
```

---

# Windows 11 환경에서 Conda 사용방법 

Conda 사용하기 위해 **Miniforge**를 설치하고 **VS Code**와 연동하는 방법을 알아보겠습니다.

---

## 1. Miniforge 설치 방법 (Windows 11)

### **① 설치 파일 다운로드**

1. [Miniforge 다운로드](https://conda-forge.org/download/)에 접속합니다.
2. **Windows x86_64 (amd64)** 링크를 클릭하여 `.exe` 설치 파일을 다운로드합니다.

### **② 설치 진행 시 주의사항**

설치 프로그램을 실행한 후, 다음 두 가지만 주의하세요.

* **Select Installation Type:** "Just Me"를 권장합니다.
* **Advanced Options:** * `Add Miniforge3 to my PATH environment variable`: **체크 해제** (권장)를 유지하세요. (체크 시 다른 프로그램과 충돌할 수 있습니다.)
* `Register Miniforge3 as my default Python`: **체크**하세요.

---

## 2. 가상환경 생성

설치가 끝나면 **시작 메뉴** 에서 **"Miniforge Prompt"** 를 검색해 실행합니다. 검은색 터미널 창이 뜨면 아래 명령어를 순서대로 입력하여 시계열 학습용 환경을 만듭니다.

```bash
# 1. 'mamba'를 사용하여 가상환경 생성 (파이썬 3.10 버전 권장)
mamba create -n ts_env python=3.10 -y

# 2. 가상환경 활성화
mamba activate ts_env

#만약 아래와 같은 오류 발생하면 
critical libmamba Shell not initialized

#현재 열려 있는 터미널 창에 다음 명령어를 입력하고 엔터를 누르세요.
mamba shell init --shell cmd.exe --root-prefix ~\miniforge3

#반드시 현재 실행중인 터미널 재시작 하고 
# 2. 가상환경 활성화를 다시 실행해주세요 
mamba activate ts_env
#정상적으로 처리되면 줄 맨 앞의 표시가 (base)에서 (ts_env)로 바뀝니다.

# 3. 필수 라이브러리 한 번에 설치
seaborn
mamba install pandas numpy pytorch matplotlib seaborn scikit-learn jupyter notebook ipykernel -y

```

---

## 3. VS Code와 연동하는 방법

VS Code에서 앞서 만든 `ts_env` 환경을 인식시켜야 코드가 정상적으로 실행됩니다.

### **① 필수 확장 프로그램 설치**

1. VS Code를 실행합니다.
2. 왼쪽 사이드바의 **Extensions(확장)** 아이콘(사각형 모양)을 클릭합니다.
3. **Python** (Microsoft 제작)과 **Jupyter** 확장을 검색하여 설치합니다.

### **② 파이썬 인터프리터 설정**

1. VS Code 안에서 아무 `.py` 파일을 만들거나 엽니다.
2. `Ctrl + Shift + P`를 눌러 명령 팔레트를 엽니다.
3. **"Python: Select Interpreter"** 를 입력하고 선택합니다.
4. 목록에서 `Python 3.10.x ('ts_env': miniforge3)` 항목을 선택합니다.

### **③ Jupyter Notebook 연동 (시계열 실습용)**

1. `.ipynb` 파일을 새로 만듭니다.
2. 오른쪽 상단의 **"Select Kernel"** 을 클릭합니다.
3. **"Python Environments..."** 를 선택한 후, 아까 만든 `ts_env`를 선택합니다.

---

## 4. 설치 확인 테스트

VS Code 하단의 터미널(Terminal)에서 아래 코드를 실행해 보세요.

파일명 : info.py

```python
import torch
import pandas as pd

print(f"PyTorch 버전: {torch.__version__}")
print(f"Pandas 버전: {pd.__version__}")
print(f"GPU 사용 가능 여부: {torch.cuda.is_available()}")

```

---
# VS Code에서 주피터 노트북 사용방법

## 1. 필수 확장 프로그램 설치

먼저 VS Code를 열고 왼쪽 사이드바의 **확장(Extensions)**  아이콘(테트리스 블록 모양)을 클릭합니다.

* 검색창에 **"Python"** 을 입력하고 Microsoft에서 만든 확장 프로그램을 설치하세요.
* 그 다음 **"Jupyter"** 를 검색하여 역시 Microsoft에서 제공하는 확장을 설치합니다.

## 2. 새 노트북 파일 만들기

두 가지 방법

* **방법 A:** 상단 메뉴에서 `File` > `New File`을 누른 후 파일 형식을 **Jupyter Notebook**으로 선택합니다.
  파일명은 test.ipynb 으로 저장합니다.
* **방법 B:** 파일 탐색기에서 새 파일을 만들 때 파일명 끝에 확장자를 **`.ipynb`** 로 지정하여 만들고 생성한 파일을 열러서 작업을 합니다. (예: `test.ipynb`)

### 3. 커널(Kernel) 선택하기

노트북 파일을 열면 오른쪽 상단에 **[Select Kernel]** 이라는 버튼이 보일 겁니다.

* 이 버튼을 누르고 설치된 **Python 버전(또는 가상환경)** 을 선택합니다.
* 처음 실행할 때 주피터 관련 패키지가 설치되어 있지 않다면, VS Code가 "Jupyter 패키지를 설치하시겠습니까?"라는 팝업을 띄웁니다. 이때 **[Install]** 을 눌러주면 설치됩니다.

---

## 핵심 단축키

주피터 노트북은 마우스보다 키보드로 작업할 때 훨씬 빠릅니다. 셀 왼쪽 테두리를 마우스로 클릭하면 **명령 모드**입니다. 이때 아래 키를 눌러보세요.

* **`A`**: 현재 셀 위에 새 셀 추가 (Above)
* **`B`**: 현재 셀 아래에 새 셀 추가 (Below)
* **`DD`**: 현재 셀 삭제 (Delete)
* **`M`**: 셀을 마크다운(텍스트 설명) 모드로 변경
* **`Y`**: 셀을 코드(Python) 모드로 변경
* **`Ctrl + Enter`**: 현재 셀 실행
* **`Shift + Enter`**: 현재 셀 실행 후 다음 셀로 이동

---

## 데이터 시각화 확인하기

주피터의 진가는 결과를 바로 보는 데 있습니다. 아래 코드를 한 셀에 넣고 실행(`Shift + Enter`)해 보세요.

```python
import matplotlib.pyplot as plt

plt.plot([1, 2, 3, 4], [1, 4, 9, 16])
plt.title("Hello Jupyter!")
plt.show()

```

그래프가 코드 바로 아래에 나타난다면 성공입니다!

---

## Python 시계열 분석 필수 라이브러리 및 용어

1. Pandas
2. NumPy
3. Matplotlib
4. Seaborn
5. 텐서 (LSTM 등 AI 모델 학습)

---

## 1. Pandas란 무엇인가?

Pandas는 파이썬에서 **데이터 조작 및 분석**을 위해 사용하는 오픈소스 라이브러리입니다. 표(Table) 형태의 데이터를 다루는 데 최적화되어 있으며, 대용량 데이터를 처리할 때 매우 효율적입니다.

핵심은 두 가지 자료구조입니다:

* **Series (시리즈):** 1차원 배열 형태 (엑셀의 한 개의 열)
* **DataFrame (데이터프레임):** 2차원 표 형태 (엑셀의 시트 전체)

---

### 1. Pandas로 무엇을 할 수 있는지

단순히 데이터를 보는 것을 넘어, 데이터를 '요리'하는 거의 모든 과정을 수행할 수 있습니다.

#### 다양한 파일 읽기 및 저장

CSV, Excel, SQL 데이터베이스, JSON, HTML 등 거의 모든 형태의 데이터를 불러오고 다시 저장할 수 있습니다.

#### 데이터 전처리 (Cleaning)

실제 데이터는 대개 지저분합니다. Pandas를 사용하면 다음 작업이 순식간에 끝납니다:

* 비어있는 값(결측치) 채우기 또는 삭제
* 중복된 데이터 제거
* 잘못된 형식의 데이터 수정 (예: 날짜 형식 통일)

#### 데이터 조작 및 변형

* **필터링:** 특정 조건에 맞는 데이터만 뽑아내기 (예: "매출이 1억 원 이상인 상점만 보기")
* **정렬:** 오름차순/내림차순 정렬
* **그룹화 (Grouping):** 특정 기준에 따라 데이터를 묶고 통계 내기 (예: "도시별 평균 기온 계산")
* **병합 (Merge/Join):** 여러 개의 표를 하나로 합치기

#### 데이터 분석 및 통계

기초적인 통계값(평균, 중앙값, 표준편차 등)을 코드 한 줄로 산출할 수 있으며, 간단한 그래프 시각화도 지원합니다.

---

### 2. 왜 Pandas인가요?

* **속도:** 파이썬 기본 리스트보다 훨씬 빠릅니다. (내부가 C 언어로 작성 되어 있습니다)
* **유연성:** 수백만 행의 데이터도 가볍게 핸들링합니다.
* **호환성:** 머신러닝 라이브러리인 Scikit-learn, 데이터 시각화 라이브러리인 Matplotlib 등과 완벽하게 연동됩니다.

---

## 2. NumPy란 무엇인가?

NumPy는 **Numerical Python**의 약자로, 수치 계산을 위해 만들어진 파이썬의 핵심 라이브러리입니다. 파이썬의 기본 리스트(List)는 사용하기 쉽지만, 숫자가 수백만 개, 수억 개가 되면 계산 속도가 매우 느려집니다. NumPy는 이를 해결하기 위해 **ndarray(n-dimensional array)** 라는 다차원 배열 객체를 제공합니다.

---

### 1. NumPy로 무엇을 할 수 있나요?

#### ⚡ 고성능 산술 연산 (Vectorization)

반복문(`for`문)을 쓰지 않고도 배열 전체에 연산을 적용할 수 있습니다. 예를 들어, 100만 개의 데이터에 각각 2를 곱할 때 파이썬 리스트보다 훨씬 빠르게 처리합니다.

#### 복잡한 수학 및 통계 계산

* **선형 대수(Linear Algebra):** 행렬 곱, 역행렬 계산 등 (딥러닝의 핵심 계산)
* **통계 분석:** 평균, 표준편차, 분산, 상관계수 산출
* **푸리에 변환 및 난수 생성:** 과학 계산과 시뮬레이션에 필수적인 기능들

#### 🧩 데이터의 구조 변경

데이터의 형태를 자유자재로 바꿀 수 있습니다.

* 예: 12개의 숫자가 일렬로 늘어선 데이터를 3행 4열의 표 형태로 바꾸기 (`reshape`)

#### 🖼️ 이미지 및 신호 처리

컴퓨터 입장에서 이미지는 '숫자로 이루어진 행렬'입니다. NumPy를 사용하면 이미지의 밝기를 조절하거나 필터를 입히는 등의 작업을 숫자를 계산하듯 처리할 수 있습니다.

---

### 2. 왜 NumPy를 써야 하나요?

| 특징 | 설명 |
| --- | --- |
| **압도적인 속도** | 내부가 C언어로 구현되어 있어 파이썬 기본 연산보다 수십~수백 배 빠릅니다. |
| **적은 메모리 사용** | 데이터를 촘촘하게 저장하여 메모리 효율이 매우 좋습니다. |
| **표준의 위상** | **Pandas, Matplotlib, Scikit-learn, TensorFlow** 등 거의 모든 데이터 관련 도구가 NumPy 위에서 돌아갑니다. |

---

> **비유하자면:**
> * **파이썬 리스트:** 이것저것 담을 수 있는 만능 장바구니 (조금 느림)
> * **NumPy 배열:** 규격화된 상자들이 착착 쌓여있는 초고속 컨베이어 벨트
>

---

## 3. Matplotlib이란 무엇인가?

데이터 분석의 마지막 꽃은 바로 '시각화'입니다. **Matplotlib(맷플롯립)** 은 파이썬에서 데이터를 그래프나 차트로 그려주는 가장 기본적이면서도 강력한 **시각화 라이브러리** 입니다.

Pandas로 데이터를 정리하고 NumPy로 계산했다면, Matplotlib은 그 결과물을 눈에 보이는 그림으로 만들어줍니다.

Matplotlib은 파이썬에서 2D 그래프를 그릴 때 표준처럼 사용되는 도구입니다. 엑셀에서 만들 수 있는 거의 모든 종류의 차트를 구현할 수 있으며, 출판물 수준의 고품질 이미지를 생성할 수 있습니다.

---

### 1. Matplotlib 기능

#### 1. 기본적인 그래프 그리기

가장 많이 쓰이는 데이터 시각화 기능을 모두 제공합니다.

* **Line Plot:** 선 그래프 (시간에 따른 변화 추이)
* **Bar Chart:** 막대 그래프 (항목 간의 수치 비교)
* **Histogram:** 히스토그램 (데이터의 분포 확인)
* **Scatter Plot:** 산점도 (두 변수 간의 상관관계 확인)
* **Pie Chart:** 파이 차트 (비율 표시)

#### 2. 정밀한 디자인 제어

그래프의 아주 작은 부분까지 사용자가 직접 조절할 수 있습니다.

* 축(Axis)의 레이블, 타이틀, 범례(Legend) 설정
* 선의 색상, 굵기, 스타일(점선 등) 변경
* 그래프 안에 화살표나 텍스트로 설명 추가

#### 3. 다중 그래프 (Subplots)

하나의 이미지 안에 여러 개의 그래프를 나란히 배치하여 데이터를 다각도에서 비교할 수 있습니다.

---

### 2. Matplotlib의 특징

* **커스터마이징의 끝판왕:** 거의 모든 요소를 코드로 수정할 수 있어 자유도가 매우 높습니다.
* **확장성:** **Seaborn** 같은 더 예쁜 시각화 도구들도 사실 Matplotlib을 기반으로 만들어졌습니다.
* **다양한 저장 포맷:** PNG, JPG뿐만 아니라 벡터 그래픽인 PDF, SVG 파일로도 저장할 수 있어 논문이나 보고서용으로 적합합니다.

---

## 4. Seaborn이란 무엇인가?

**Seaborn(시본)** 은 Matplotlib을 바탕으로 만들어진 **통계 데이터 시각화 라이브러리** 입니다. 쉽게 말해, Matplotlib이 "그래프를 그릴 수 있는 도화지와 붓"이라면, Seaborn은 "복잡한 그림도 뚝딱 그려주는 고급 템플릿"과 같습니다.

Matplotlib은 자유도가 높지만 코드가 복잡하고 기본 디자인이 투박하다는 단점이 있습니다. Seaborn은 이를 보완하여 **코드 한두 줄만으로 훨씬 예쁘고 복잡한 통계 차트** 를 그릴 수 있게 해줍니다. 특히 Pandas의 DataFrame과 환상적인 궁합을 자랑합니다.

---

### 1. Seaborn으로 무엇을 할 수 있나요?

#### 복잡한 통계 관계 시각화

단순한 막대그래프를 넘어 데이터의 분포와 관계를 깊이 있게 보여줍니다.

* **Violin Plot:** 데이터의 분포(밀도)와 범위를 바이올린 모양으로 시각화합니다.
* **Heatmap:** 데이터 간의 상관관계를 색상의 농도로 표현하여 한눈에 파악하게 합니다.
* **Joint Plot:** 두 변수 간의 산점도와 각 변수의 히스토그램을 동시에 보여줍니다.

#### 테마와 색상 자동 설정

Matplotlib에서는 일일이 설정해야 했던 색상 팔레트와 격자 스타일을 기본적으로 제공합니다. `set_theme()` 한 줄이면 세련된 디자인의 그래프가 완성됩니다.

#### 회귀선(Regression) 표시

데이터의 흐름을 분석하여 자동으로 추세선(회귀선)을 그려주는 기능을 제공하여, 변수 간의 관계를 파악하기 매우 쉽습니다.

#### 다중 비교 (FacetGrid)

데이터의 카테고리별로(예: 성별, 요일별) 그래프를 여러 개로 쪼개어 한 번에 비교하는 작업을 매우 직관적으로 처리합니다.

---

## 5. Matplotlib vs Seaborn 비교

| 특징 | Matplotlib | Seaborn |
| --- | --- | --- |
| **목적** | 범용적인 그래프 그리기 | 통계 데이터 분석 및 시각화 |
| **난이도** | 세세한 설정이 필요해 코드가 김 | 내부 알고리즘이 복잡한 계산을 대신해 코드가 짧음 |
| **디자인** | 기본 디자인이 다소 투박함 | 현대적이고 세련된 기본 디자인 제공 |
| **데이터 호환** | 리스트, 넘파이 배열 등 다양함 | **Pandas DataFrame**에 최적화됨 |

---

## 6. 텐서란?

**텐서(Tensor)** 를 가장 명확하게 정의하자면, **"다차원 배열을 담는 수학적·데이터적 컨테이너"** 라고 할 수 있습니다.

단순히 숫자 하나인지, 여러 개의 숫자가 나열된 것인지에 따라 이름이 달라지는데, 이를 계층적으로 이해하는 것이 중요합니다.

---

### 1. 텐서의 계층적 구조 (Rank)

텐서는 차원(Dimension)에 따라 **Rank(랭크)** 라는 단위를 사용하여 구분합니다.

* **Rank 0: 스칼라 (Scalar)**
  * 하나의 숫자값입니다. (예: 현재 온도 `25.5`)
  * 방향성 없이 크기만 가집니다.

* **Rank 1: 벡터 (Vector)**
  * 숫자들의 1차원 나열입니다. (예: 오늘 시간별 온도 리스트 `[20, 22, 25, 23...]`)

* **Rank 2: 행렬 (Matrix)**
  * 가로와 세로가 있는 2차원 표 형태입니다. (예: 엑셀 시트 데이터)

* **Rank 3 이상: 텐서 (Tensor)**
  * 행렬을 여러 겹으로 쌓은 다차원 구조입니다.
  * **예시:** 컬러 이미지는 `(높이, 너비, 채널[R,G,B])` 형태의 Rank 3 텐서입니다.

---

### 2. 왜 딥러닝에서는 '행렬' 대신 '텐서'라고 부를까?

컴퓨터 공학적 관점에서 텐서는 단순히 데이터를 담는 그릇을 넘어 **연산의 단위**가 되기 때문입니다.

1. **데이터의 묶음 처리 (Batch Processing):**
24시간 편의점 32개의 4종류의 아이스크림 판매량을 시계열 텐서로 구성한다면, 데이터의 모양은 `(32, 24, 4)`가 됩니다. 이렇게 **차원이 확장된 데이터 덩어리**를 처리하기 위해 텐서라는 개념이 필수적입니다.
2. **GPU 연산 최적화:**
TensorFlow나 PyTorch 같은 프레임워크는 이 '텐서' 단위의 데이터를 GPU(그래픽 카드)로 보내 한꺼번에 병렬 계산합니다. 수만 개의 가중치를 동시에 계산하기에 가장 효율적인 구조가 바로 텐서입니다.

---

### 3. 요약하자면

* **수학적으로:** 데이터의 차원을 확장한 일반적인 개념.
* **컴퓨터적으로:** 다차원 배열(Multi-dimensional Array) 객체.
* **딥러닝적으로:** GPU가 한꺼번에 계산하기 좋게 뭉쳐놓은 **데이터의 입방체**.
