import torch
import torch.nn as nn

# GPU 인식 확인
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"✅ 사용 가능 장치: {device}")
print(f"✅ GPU 모델명: {torch.cuda.get_device_name(0)}")

# 아주 간단한 연산 테스트
x = torch.randn(64, 10).to(device)
model = nn.Linear(10, 1).to(device)
output = model(x)

print("🚀 PyTorch 연산 성공!")