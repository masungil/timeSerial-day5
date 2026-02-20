import os

# TensorFlow 관련 환경 변수 설정
# CuDNN의 오토튠 기능을 끔 (일부 환경에서 안정성 확보)
os.environ['TF_CUDNN_USE_AUTOTUNE'] = '0'
# 로그 수준 설정 (0: 모두 출력, 1: INFO 제외, 2: WARNING 제외, 3: ERROR만 출력)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
# GPU 메모리 증가 허용 설정 (TensorFlow가 GPU 메모리를 전체 다 점유하지 않도록 함)
os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'

import tensorflow as tf
import numpy as np

# 시스템에 설치된 물리적인 GPU 장치 목록을 가져옴
gpus = tf.config.list_physical_devices('GPU')

if gpus:
    try:
        # GPU 메모리 동적 할당 설정 (RTX 50 시리즈 등 최신 그래픽카드에서 필수 권장)
        # 이 설정을 하면 필요한 만큼만 GPU 메모리를 할당하며 사용함
        tf.config.experimental.set_memory_growth(gpus[0], True)
    except RuntimeError as e:
        # 프로그램 시작 시 장치가 설정되어야 하므로 에러 발생 시 출력
        print(f"GPU 설정 중 에러 발생: {e}")

# 아주 단순한 행렬 곱셈 테스트 (GPU 연산 확인용)
print("🚀 TensorFlow GPU 연산 테스트 시작...")

# 테스트용 상수 행렬 정의
a = tf.constant([[1.0, 2.0], [3.0, 4.0]])
b = tf.constant([[1.0, 1.0], [0.0, 1.0]])

try:
    # 행렬 곱셈 수행 (실제 GPU 가속이 작동하는 지점)
    c = tf.matmul(a, b)
    print("✅ 결과값:\n", c)
    print("\n🎉 축하합니다! TensorFlow가 GPU(RTX 50XX 포함)에서 정상 작동합니다!")
except Exception as e:
    # 연산 중 에러 발생 시 예외 처리
    print(f"❌ 에러 발생: {e}")
