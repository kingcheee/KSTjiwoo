"""
===========================================================
📌 파이썬 기초 — 스터디 발표용 치트시트
===========================================================
목표: 파이썬 문법의 핵심만 빠르게 이해하기
시간: 발표 약 3분분량
===========================================================
"""

# ==========================================================
# 1. 변수와 기본 연산
# ==========================================================
# 파이썬은 변수 선언 시 타입을 지정할 필요 없어!
# 파이썬이 알아서 판단해줌 (동적 타이핑)

name = "규연"          # 문자열 (str)
age = 25              # 정수 (int)
height = 165.5        # 실수 (float)
is_student = True     # 불리언 (bool)

# 기본 연산
a = 10
b = 3
print(a + b)   # 13  (덧셈)
print(a - b)   # 7   (뺄셈)
print(a * b)   # 30  (곱셈)
print(a / b)   # 3.33 (나눗셈 — 결과가 실수)
print(a // b)  # 3   (몫)
print(a % b)   # 1   (나머지)
print(a ** b)  # 1000 (거듭제곱)


# ==========================================================
# 2. 자료구조 — 데이터를 담는 그릇들
# ==========================================================

# --- 리스트(List): 변경 가능한 순서있는 컬렉션 ---
# 비유: 🛒 쇼핑 장바구니 (뭐든 넣고, 빼고, 바꿀 수 있어)
fruits = ["사과", "바나나", "포도"]
fruits.append("딸기")          # 끝에 추가 → ["사과", "바나나", "포도", "딸기"]
fruits.remove("바나나")       # 특정 값 삭제 → ["사과", "포도", "딸기"]
print(fruits[0])              # "사과" (0부터 시작!)
print(fruits[-1])             # "딸기" (뒤에서 첫 번째)
print(fruits[0:2])            # ["사과", "포도"] (슬라이싱 — 0번째부터 1번째까지)

# 리스트 컴프리헨션 (리스트를 한 줄로 만드는 간단한 방법)
squares = [x**2 for x in range(5)]  # [0, 1, 4, 9, 16]


# --- 튜플(Tuple): 변경 불가능한 리스트 ---
# 비유: 📩 우편봉투 (한 번 넣으면 바꿀 수 없어)
coordinates = (10, 20)
# coordinates[0] = 5  → 에러! 변경 불가능


# --- 딕셔너리(Dictionary): 키-값 쌍으로 저장 ---
# 비유: 📖 영한사전 ("사과"를 찾으면 "apple"이 나와)
student = {
    "name": "규연",
    "age": 25,
    "major": "컴퓨터공학"
}
print(student["name"])        # "규연"
student["age"] = 26           # 값 변경 가능 → 딕셔너리 자체는 변경 가능!
print(student.keys())         # 키 목록 → dict_keys(['name', 'age', 'major'])
print(student.values())       # 값 목록 → dict_values(['규연', 26, '컴퓨터공학'])


# --- 집합(Set): 중복을 허용하지 않는 컬렉션 ---
# 비유: 🎰 로또 번호 (같은 번호가 두 개 있을 수 없어)
lotto = {1, 2, 3, 4, 5, 5, 5}   # 중복 자동 제거!
print(lotto)  # {1, 2, 3, 4, 5}

set_a = {1, 2, 3, 4}
set_b = {3, 4, 5, 6}
print(set_a & set_b)  # {3, 4}  교집합
print(set_a | set_b)  # {1, 2, 3, 4, 5, 6}  합집합
print(set_a - set_b)  # {1, 2}  차집합


# ==========================================================
# 3. 조건문 — 프로그램의 갈래길
# ==========================================================
# 비유: 🚦 신호등 (빨간불이면 멈추고, 초록불이면 가고)

score = 85

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"      # ← 여기에 해당!
elif score >= 70:
    grade = "C"
else:
    grade = "F"

print(f"점수 {score}점의 등급: {grade}")

# 삼항 연산자 (조건문을 한 줄로!)
result = "합격" if score >= 80 else "불합격"


# ==========================================================
# 4. 반복문 — 같은 작업 반복하기
# ==========================================================
# 비유: 🏭 공장 컨베이어 벨트 (물건 하나씩 꺼내서 처리)

# --- for 반복문: 정해진 횟수만큼 반복 ---
for i in range(5):        # 0, 1, 2, 3, 4
    print(f"{i}번째!")

# 리스트 순회
fruits = ["사과", "바나나", "포도"]
for fruit in fruits:
    print(f"오늘의 과일: {fruit}")

# enumerate: 인덱스와 값을 동시에
for index, fruit in enumerate(fruits):
    print(f"{index}번: {fruit}")

# --- while 반복문: 조건이 참인 동안 반복 ---
count = 0
while count < 3:
    print(f"카운트: {count}")
    count += 1

# break: 반복문 강제 종료 (비유: 비상구 🚪)
# continue: 이번 차례 건너뛰기 (다음 반복으로)
for i in range(10):
    if i == 3:
        continue    # 3은 건너뛰기
    if i == 7:
        break       # 7에서 멈추기
    print(i)        # 0, 1, 2, 4, 5, 6


# ==========================================================
# 5. 함수 — 재사용 가능한 코드 블록
# ==========================================================
# 비유: ☕ 커피머신 (버튼 누르면 (= 호출하면) 커피 (= 결과)가 나와)

# 기본 함수
def greet(name):
    """이름을 받아서 인사말을 반환하는 함수"""
    return f"안녕, {name}!"

print(greet("규연"))  # "안녕, 규연!"

# 기본값 파라미터
def order_coffee(drink="아메리카노"):
    # 음료를 안 정하면 자동으로 아메리카노!
    print(f"{drink} 주문 완료!")

order_coffee()              # "아메리카노 주문 완료!"
order_coffee("카페라떼")     # "카페라떼 주문 완료!"

# 가변 인자 (*args): 몇 개든 받을 수 있어
def add_all(*numbers):
    # 비유: 🛒 장바구니에 물건을 아무리 넣어도 다 계산해주는 카운터
    return sum(numbers)

print(add_all(1, 2, 3, 4, 5))  # 15

# 키워드 가변 인자 (**kwargs): 이름 붙은 인자를 여러 개 받기
def print_info(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

print_info(name="규연", age=25, city="광주")
# name: 규연
# age: 25
# city: 광주


# ==========================================================
# 6. 예외 처리 — 예상치 못한 상황 대비
# ==========================================================
# 비유: 🪄 안전망 (아무리 높은 곳에서 떨어져도 안전망이 받쳐줘)

try:
    # 에러가 발생할 수 있는 코드
    result = 10 / 0
except ZeroDivisionError:
    # 0으로 나눌 때 실행
    print("0으로 나눌 수 없어요!")
except Exception as e:
    # 그 외 모든 에러
    print(f"에러 발생: {e}")
else:
    # 에러가 없을 때 실행
    print(f"결과: {result}")
finally:
    # 무조건 실행 (에러 유무 상관없이)
    print("연산 끝!")

# 실제 예시: 파일 읽기
try:
    with open("data.txt", "r", encoding="utf-8") as f:
        content = f.read()
        print(content)
except FileNotFoundError:
    print("파일이 없어요! 경로를 확인해보세요.")


# ==========================================================
# 7. 파일 입출력 — 데이터 읽고 쓰기
# ==========================================================

# 파일 쓰기
""" 
with open("output.txt", "w", encoding="utf-8") as f:
    f.write("안녕하세요!\n")
    f.write("파이썬 파일 입출력 테스트입니다.\n")
"""

# 파일 읽기
""" 
with open("output.txt", "r", encoding="utf-8") as f:
    content = f.read()          # 전체 읽기
    lines = f.readlines()       # 줄 단위로 읽기 (리스트로 반환)
"""

# CSV 파일 읽기 (판다스를 더 많이 쓰지만, 기초 버전)
"""
import csv
with open("data.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)  # 각 행이 리스트로 반환
"""


# ==========================================================
# 8. 클래스 — 객체 지향 프로그래밍
# ==========================================================
# 비유: 🏗️ 건물 설계도 (클래스)로 → 실제 건물 (객체) 만들기

class Student:
    """학생을 나타내는 클래스"""
    
    def __init__(self, name, age, major):
        # 생성자: 객체가 만들어질 때 자동 실행
        # self = 이 객체 자신을 가리킴
        self.name = name
        self.age = age
        self.major = major
        self.grades = []
    
    def add_grade(self, grade):
        """성적 추가"""
        self.grades.append(grade)
    
    def get_average(self):
        """평균 계산"""
        if not self.grades:
            return 0
        return sum(self.grades) / len(self.grades)
    
    def __str__(self):
        # print()로 출력할 때 보여질 문자열
        return f"학생: {self.name}, 나이: {self.age}, 전공: {self.major}"

# 객체 생성 (= 설계도로 건물 짓기)
s1 = Student("규연", 25, "컴퓨터공학")
s1.add_grade(90)
s1.add_grade(85)
print(s1)                        # 학생: 규연, 나이: 25, 전공: 컴퓨터공학
print(f"평균: {s1.get_average()}")  # 평균: 87.5

# --- 상속: 기존 클래스를 확장하기 ---
class GraduateStudent(Student):
    """대학원생 클래스 (학생 클래스를 상속)"""
    
    def __init__(self, name, age, major, thesis_title):
        super().__init__(name, age, major)  # 부모 생성자 호출
        self.thesis_title = thesis_title
    
    # __str__ 오버라이딩 (부모의 메서드를 재정의)
    def __str__(self):
        base = super().__str__()
        return f"{base}, 논문: {self.thesis_title}"

g1 = GraduateStudent("지우", 27, "AI", "딥러닝 최적화 연구")
print(g1)  # 학생: 지우, 나이: 27, 전공: AI, 논문: 딥러닝 최적화 연구


# ==========================================================
# 9. 모듈과 패키지 — 코드 재사용의 극대화
# ==========================================================

# 방법 1: 전체 모듈 가져오기
# import math
# print(math.pi)       # 3.141592...
# print(math.sqrt(16))  # 4.0

# 방법 2: 특정 함수만 가져오기
# from math import sqrt, pi
# print(sqrt(16))  # 4.0

# 방법 3: 별칭 붙이기
# import numpy as np      # numpy를 np로 줄여서 사용
# import pandas as pd     # pandas를 pd로 줄여서 사용

# 직접 만든 모듈 가져오기
# from my_module import my_function


print("✅ 파이썬 기초 치트시트 끝!")
print("다음 파일: 02_numpy_basics.py → ")
