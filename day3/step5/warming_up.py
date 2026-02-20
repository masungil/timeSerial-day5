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
