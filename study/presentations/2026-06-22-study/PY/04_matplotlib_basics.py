"""
===========================================================
📌 Matplotlib 기초 — 스터디 발표용 치트시트
===========================================================
목표: 데이터를 시각적으로 표현하는 핵심 그래프 5가지 익히기
시간: 발표 약 3분분량
===========================================================
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 한글 폰트 설정 (Windows)
plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

# ==========================================================
# 0. 가상의 타이타닉 데이터 생성
# ==========================================================
np.random.seed(42)
n = 200
titanic = pd.DataFrame({
    "survived": np.random.choice([0, 1], n, p=[0.6, 0.4]),
    "pclass": np.random.choice([1, 2, 3], n, p=[0.2, 0.3, 0.5]),
    "age": np.random.normal(30, 12, n).clip(1, 80).astype(int),
    "fare": np.random.exponential(30, n).round(2),
    "sex": np.random.choice(["male", "female"], n, p=[0.65, 0.35]),
    "embarked": np.random.choice(["S", "C", "Q"], n, p=[0.7, 0.2, 0.1])
})

# ==========================================================
# 1. 선 그래프 (Line Plot) — 추이 보기
# ==========================================================
# 비유: 📈 주식 차트 — 시간에 따른 변화 추이를 보여줄 때!
# 언제 쓸까? → 특정 값의 변화 추세를 확인할 때

# 객실 등급별 생존율 추이
survival_by_class = titanic.groupby("pclass")["survived"].mean()

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(survival_by_class.index, survival_by_class.values,
        marker="o", linewidth=2, markersize=10, color="#2196F3")
ax.set_xlabel("객실 등급 (Pclass)", fontsize=12)
ax.set_ylabel("생존율", fontsize=12)
ax.set_title("📈 선 그래프: 객실 등급별 생존율 추이", fontsize=14)
ax.set_ylim(0, 1)
ax.grid(True, alpha=0.3)

# 값 표시
for x, y in zip(survival_by_class.index, survival_by_class.values):
    ax.annotate(f"{y:.1%}", (x, y), textcoords="offset points",
                xytext=(0, 10), ha="center", fontsize=11, fontweight="bold")

plt.tight_layout()
plt.savefig("01_line_plot.png", dpi=150)
plt.show()
print("✅ 선 그래프 저장 완료: 01_line_plot.png")


# ==========================================================
# 2. 막대 그래프 (Bar Plot) — 비교하기
# ==========================================================
# 비유: 📊 순위표 — 범주 간 값을 비교할 때!
# 언제 쓸까? → 두 개 이상의 범주 간 차이를 비교할 때

# 승선 항구별 생존자 수
survival_by_port = titanic.groupby("embarked")["survived"].sum()

fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(survival_by_port.index, survival_by_port.values,
              color=["#FF6B6B", "#4ECDC4", "#45B7D1"], edgecolor="white", linewidth=1.5)
ax.set_xlabel("승선 항구 (Embarked)", fontsize=12)
ax.set_ylabel("생존자 수", fontsize=12)
ax.set_title("📊 막대 그래프: 승선 항구별 생존자 수", fontsize=14)

# 값 표시
for bar in bars:
    height = bar.get_height()
    ax.annotate(f"{int(height)}명",
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 5), textcoords="offset points",
                ha="center", fontsize=11, fontweight="bold")

plt.tight_layout()
plt.savefig("02_bar_plot.png", dpi=150)
plt.show()
print("✅ 막대 그래프 저장 완료: 02_bar_plot.png")


# ==========================================================
# 3. 히트맵 (Heatmap) — 상관관계 보기
# ==========================================================
# 비유: 🌡️ 온도계 — 색깔로 강도를 표현할 때!
# 언제 쓸까? → 여러 변수 간의 상관관계를 한눈에 파악할 때

# 수치형 변수들의 상관행렬
numeric_cols = titanic[["survived", "pclass", "age", "fare"]]
corr_matrix = numeric_cols.corr()

fig, ax = plt.subplots(figsize=(8, 6))
im = ax.imshow(corr_matrix, cmap="RdBu_r", vmin=-1, vmax=1)

# 축 설정
ax.set_xticks(range(len(corr_matrix.columns)))
ax.set_yticks(range(len(corr_matrix.columns)))
ax.set_xticklabels(corr_matrix.columns, fontsize=11)
ax.set_yticklabels(corr_matrix.columns, fontsize=11)

# 값 표시
for i in range(len(corr_matrix)):
    for j in range(len(corr_matrix)):
        val = corr_matrix.iloc[i, j]
        color = "white" if abs(val) > 0.5 else "black"
        ax.text(j, i, f"{val:.2f}", ha="center", va="center",
                fontsize=12, fontweight="bold", color=color)

plt.colorbar(im, ax=ax, label="상관계수")
ax.set_title("🌡️ 히트맵: 타이타닉 변수 간 상관관계", fontsize=14)
plt.tight_layout()
plt.savefig("03_heatmap.png", dpi=150)
plt.show()
print("✅ 히트맵 저장 완료: 03_heatmap.png")


# ==========================================================
# 4. 박스플롯 (Box Plot) — 분포와 이상치 보기
# ==========================================================
# ==========================================================
# 비유: 📦 택배 박스 — 데이터가 어디에 모여있는지, 이상한 값은 없는지 확인!
# 언제 쓸까? → 데이터의 분포, 중앙값, 이상치를 확인할 때

fig, ax = plt.subplots(figsize=(8, 5))

# 등급별 나이 분포
age_by_class = [titanic[titanic["pclass"] == c]["age"].values for c in [1, 2, 3]]
bp = ax.boxplot(age_by_class, labels=["1등석", "2등석", "3등석"],
                patch_artist=True, notch=True)

colors = ["#FF6B6B", "#4ECDC4", "#45B7D1"]
for patch, color in zip(bp["boxes"], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)

ax.set_xlabel("객실 등급", fontsize=12)
ax.set_ylabel("나이", fontsize=12)
ax.set_title("📦 박스플롯: 객실 등급별 나이 분포", fontsize=14)
ax.grid(True, alpha=0.3, axis="y")

plt.tight_layout()
plt.savefig("04_boxplot.png", dpi=150)
plt.show()
print("✅ 박스플롯 저장 완료: 04_boxplot.png")

# 박스플롿 해석법:
# 📦 박스 안 = 전체 데이터의 50%가 모여있는 구간 (IQR)
# 선 = 중앙값
# 수엱 = 정상 범위
# 동그라미 = 이상치 (Outlier)


# ==========================================================
# 5. 바이올린 플롯 (Violin Plot) — 분포 밀도까지 보기
# ==========================================================
# 비유: 🎻 바이올린 — 박스플롯 + 데이터 밀도까지 함께 보여줘!
# 언제 쓸까? → 박스플롯보다 더 상세한 분포 형태를 파악하고 싶을 때

fig, ax = plt.subplots(figsize=(8, 5))

age_by_class = [titanic[titanic["pclass"] == c]["age"].values for c in [1, 2, 3]]
parts = ax.violinplot(age_by_class, positions=[1, 2, 3], showmeans=True, showmedians=True)

colors = ["#FF6B6B", "#4ECDC4", "#45B7D1"]
for i, pc in enumerate(parts["bodies"]):
    pc.set_facecolor(colors[i])
    pc.set_alpha(0.7)

ax.set_xticks([1, 2, 3])
ax.set_xticklabels(["1등석", "2등석", "3등석"])
ax.set_xlabel("객실 등급", fontsize=12)
ax.set_ylabel("나이", fontsize=12)
ax.set_title("🎻 바이올린 플롯: 객실 등급별 나이 분포 (밀도 포함)", fontsize=14)
ax.grid(True, alpha=0.3, axis="y")

plt.tight_layout()
plt.savefig("05_violin_plot.png", dpi=150)
plt.show()
print("✅ 바이올린 플롯 저장 완료: 05_violin_plot.png")


# ==========================================================
# 6. 그래프 선택 가이드 — 상황별 추천
# ==========================================================
print("""
╔══════════════════════════════════════════════════════════╗
║           📊 그래프 선택 가이드                          ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  📈 선 그래프  → 추이/트렌드 보기 (시간별 변화 등)       ║
║  📊 막대 그래프 → 범주 간 비교 (순위, 개수 등)           ║
║  🌡️ 히트맵    → 상관관계 보기 (변수 간 연관성)           ║
║  📦 박스플롯  → 분포 + 이상치 확인                       ║
║  🎻 바이올린  → 분포 밀도까지 상세히 확인                ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
""")

print("✅ Matplotlib 기초 치트시트 끝!")
print("다음 파일: 05_hypothesis_testing.py → ")
