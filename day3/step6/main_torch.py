import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import pandas as pd
import numpy as np
import koreanize_matplotlib # 한글 폰트 설정을 위한 라이브러리입니다. matplotlib에서 한글이 깨지는 문제를 해결해줍니다.
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

plt.rcParams['axes.unicode_minus'] = False 
plt.rcParams['figure.dpi'] = 150  # 고해상도 출력
plt.rcParams['lines.antialiased'] = True # 선 부드럽게 설정 강제화

# 1. 장치 설정 (RTX 50xx 확인)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"✅ 사용 가능한 장치: {device}")

# 2. 데이터 로드 및 전처리
df = pd.read_csv('./data/power_usage_dataset_3month.csv')
df['Date'] = pd.to_datetime(df['Date'])

# 시간 주기성 반영 (특성 공학)
df['hour_sin'] = np.sin(2 * np.pi * df['Date'].dt.hour / 23)
df['hour_cos'] = np.cos(2 * np.pi * df['Date'].dt.hour / 23)
df['weekday_sin'] = np.sin(2 * np.pi * df['Date'].dt.weekday / 6)
df['weekday_cos'] = np.cos(2 * np.pi * df['Date'].dt.weekday / 6)

features_list = ['Temperature', 'Usage', 'hour_sin', 'hour_cos', 'weekday_sin', 'weekday_cos']
scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(df[features_list].values)

# 시퀀스 생성 함수
def create_sequences(data, window_size=168):
    X, y = [], []
    for i in range(len(data) - window_size):
        X.append(data[i:i + window_size, :]) 
        y.append(data[i + window_size, 1]) # Target: Usage (index 1)
    return np.array(X), np.array(y)

window_size = 168
X, y = create_sequences(scaled_data, window_size)

# 데이터 분할 및 Tensor 변환
split = int(len(X) * 0.8)
X_train = torch.FloatTensor(X[:split]).to(device)
y_train = torch.FloatTensor(y[:split]).to(device)
X_test = torch.FloatTensor(X[split:]).to(device)
y_test = torch.FloatTensor(y[split:]).to(device)

train_loader = DataLoader(TensorDataset(X_train, y_train), batch_size=128, shuffle=True)

# 3. 모델 설계 (Stacked LSTM)
class StackedLSTM(nn.Module):
    def __init__(self, input_size):
        super(StackedLSTM, self).__init__()
        self.lstm1 = nn.LSTM(input_size, 128, batch_first=True)
        self.dropout1 = nn.Dropout(0.2)
        self.lstm2 = nn.LSTM(128, 64, batch_first=True)
        self.dropout2 = nn.Dropout(0.1)
        self.fc1 = nn.Linear(64, 16)
        self.fc2 = nn.Linear(1, 1) # 최종 출력

    def forward(self, x):
        # LSTM 레이어 통과
        out, _ = self.lstm1(x)
        out = self.dropout1(out)
        out, _ = self.lstm2(out)
        # 마지막 시점(last time step)의 출력만 사용
        out = self.dropout2(out[:, -1, :])
        out = torch.relu(self.fc1(out))
        # 예측값 생성 (1개 값으로 조정하기 위해 선형 변환 추가)
        # Note: 위 설계에서 fc2를 fc1의 출력 16에 맞춰 수정
        return nn.Linear(16, 1).to(device)(out)

# 위 forward 내부의 Linear 레이어를 생성자에서 정의하도록 수정하여 다시 선언
class FinalStackedLSTM(nn.Module):
    def __init__(self, input_size):
        super(FinalStackedLSTM, self).__init__()
        self.lstm1 = nn.LSTM(input_size, 128, batch_first=True)
        self.dropout1 = nn.Dropout(0.2)
        self.lstm2 = nn.LSTM(128, 64, batch_first=True)
        self.dropout2 = nn.Dropout(0.1)
        self.fc1 = nn.Linear(64, 16)
        self.fc2 = nn.Linear(16, 1)

    def forward(self, x):
        out, _ = self.lstm1(x)
        out = self.dropout1(out)
        out, _ = self.lstm2(out)
        out = self.dropout2(out[:, -1, :])
        out = torch.relu(self.fc1(out))
        return self.fc2(out)

model = FinalStackedLSTM(input_size=len(features_list)).to(device)
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 4. 모델 학습
print(f"🚀 {device}에서 학습을 시작합니다...")
model.train()
for epoch in range(50): 
    epoch_loss = 0
    for batch_X, batch_y in train_loader:
        optimizer.zero_grad()
        outputs = model(batch_X)
        loss = criterion(outputs.squeeze(), batch_y)
        loss.backward()
        optimizer.step()
        epoch_loss += loss.item()
    print(f"Epoch [{epoch+1}/50], Loss: {epoch_loss/len(train_loader):.6f}")

# 5. 예측 및 시각화
model.eval()
with torch.no_grad():
    predictions = model(X_test).cpu().numpy()

# 역스케일링 (전력 사용량 단위로 복구)
def inverse_scale(values, scaler, feature_count):
    dummy = np.zeros((len(values), feature_count))
    dummy[:, 1] = values.flatten() # Usage가 인덱스 1번
    return scaler.inverse_transform(dummy)[:, 1]

pred_original = inverse_scale(predictions, scaler, len(features_list))
actual_original = inverse_scale(y_test.cpu().numpy(), scaler, len(features_list))

# 결과 출력 (최근 1주일치 168시간 시각화)
plt.figure(figsize=(15, 6))
plt.plot(actual_original[:168], label='실제 전력량', color='#1f77b4', linewidth=2)
plt.plot(pred_original[:168], label='LSTM 예측값', color='#ff7f0e', linestyle='--', linewidth=2)
plt.title(f'{device} 가속: 전력 사용량 예측 결과 (최근 168시간)')
plt.xlabel('시간(Hour)')
plt.ylabel('사용량(kW)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

print("✨ 모든 과정이 완료되었습니다! 시각화 창을 확인하세요.")