#기본 실행을 위한 예제 
print ("Hello World")


# 디버깅을 위한 예제 
a = 10
b = 20
sum = a + b
print(sum)


# 두수를 더하는 함수 선언 
# 디버깅시 step over(F10)와 step into(F11)의 차이점 확인 () 
def add_numbers(a, b):
    return a + b

# 함수 사용 예시
result = add_numbers(10, 20)
print(f"결과: {result}") # 출력: 결과: 30
