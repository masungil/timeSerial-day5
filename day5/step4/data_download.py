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