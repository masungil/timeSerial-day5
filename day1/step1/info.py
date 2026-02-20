import torch
import pandas as pd

print(f"PyTorch 버전: {torch.__version__}")
print(f"Pandas 버전: {pd.__version__}")
print(f"GPU 사용 가능 여부: {torch.cuda.is_available()}")