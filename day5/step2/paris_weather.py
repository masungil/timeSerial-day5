from datetime import datetime
from meteostat import daily

# 파리의 기상 데이터를 불러오는 예제 코드입니다.

# 1. 기간 설정 (2006-12-01 ~ 2010-11-26)
start = datetime(2006, 12, 16)
end = datetime(2010, 11, 26)

# 2. 일 단위 데이터 불러오기
# 관측소 ID를 직접 사용하여 데이터 호출 (07149는 파리 오를리 공항)
data = daily('07149', start, end)
data = data.fetch()

# 3. 결과 확인 (기온, 강수량 등)
print(data.head())

data.to_csv('./data/paris_weather_data.csv')