"""
===========================================================
📌 데이터 시각화 — 시험공부 발표용 코드
===========================================================
강조: Matplotlib 파이차트, Seaborn 막대그래프가 핵심!
===========================================================
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# 한글 폰트 설정
plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

# 가상의 넷플릭스 데이터
netflix = pd.DataFrame({
    "title": ["오징어게임", "기묘한이야기", "더글로리", "D.P.", "마블영화",
              "기생충", "인터스텔라", "어바웃타임"],
    "type": ["TV Show", "TV Show", "TV Show", "TV Show", "Movie",
             "Movie", "Movie", "Movie"],
    "duration": [60, 50, 55, 45, 120, 132, 169, 123],
    "rating": [9.0, 8.7, 8.5, 8.8, 7.5, 8.6, 8.6, 8.3],
    "listed_in": ["Action, Drama", "Drama, Horror", "Drama, Thriller",
                  "Action, Crime", "Action, Adventure", "Drama, Thriller",
                  "Sci-Fi, Drama", "Drama, Romance"]
})


# ==========================================================
# 1. Matplotlib — 파이 차트 (Pie Chart) ⭐
# ==========================================================
# type(Movie vs TV Show) 비율 시각화

type_counts = netflix["type"].value_counts()

fig, ax = plt.subplots(figsize=(8, 6))

# ⚠️ 중요 속성들!
wedges, texts, autotexts = ax.pie(
    type_counts.values,           # 데이터 값
    labels=type_counts.index,     # 라벨 (Movie, TV Show)
    autopct='%0.f%%',             # 비율 표시 (소수점 없이)
    startangle=90,                # 시작 각도 90도
    explode=(0.05, 0.05),         # 조각 간격 띄우기
    colors=["#FF6B6B", "#4ECDC4"],  # 색상 지정
    shadow=True                   # 그림자 효과
)

ax.set_title("넷플릭스 콘텐츠 타입 비율", fontsize=14)

# suptitle: 더 큰 제목 추가
plt.suptitle("Netflix Content Analysis", fontsize=16, fontweight="bold")

plt.tight_layout()
plt.savefig("01_pie_chart.png", dpi=150)
plt.show()
print("✅ 파이 차트 저장 완료")


# ==========================================================
# 2. Seaborn — 수평 막대 그래프 (Bar Plot) ⭐
# ==========================================================
# 장르별 개수 시각화

# 장르 분리 → 카운트
genres = netflix["listed_in"].str.split(", ", expand=True)
stacked = genres.stack()
genre_counts = stacked.value_counts()

fig, ax = plt.subplots(figsize=(12, 6))

# 수평 막대 그래프
sns.barplot(
    x=genre_counts.values,    # x축: 개수
    y=genre_counts.index,     # y축: 장르 이름
    hue=genre_counts.index,   # 막대마다 다른 색상
    palette="RdGy",           # 컬러 테마 ⭐
    ax=ax
)

ax.set_xlabel("Count", fontsize=12)
ax.set_ylabel("Genre", fontsize=12)
ax.set_title("Seaborn 수평 막대 그래프: 장르별 콘텐츠 수", fontsize=14)

plt.tight_layout()
plt.savefig("02_barplot.png", dpi=150)
plt.show()
print("✅ 막대 그래프 저장 완료")


# ==========================================================
# 3. 그래프 선택 가이드
# ==========================================================
print("""
╔══════════════════════════════════════════════════════════╗
║              📊 그래프 선택 가이드                        ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  🥧 파이 차트  → 비율 보기 (전체 중 각 부분의 占比)      ║
║  📊 막대 그래프 → 범주 간 비교 (순위, 개수 등)           ║
║  📈 선 그래프  → 추이/트렌드 보기 (시간별 변화 등)       ║
║  🌡️ 히트맵    → 상관관계 보기 (변수 간 연관성)           ║
║  📦 박스플롯  → 분포 + 이상치 확인                       ║
║                                                          ║
║  Matplotlib: 기본 시각화 (세밀한 제어 가능)              ║
║  Seaborn: 세련된 디자인 (통계 시각화에 강점)             ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
""")


print("✅ 시각화 코드 끝!")
