#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from datetime import date

HOLIDAYS_2026 = {
    date(2026, 1, 1),
    date(2026, 2, 28),
    date(2026, 3, 1),
    date(2026, 3, 2),
    date(2026, 5, 5),
    date(2026, 5, 25),
    date(2026, 6, 6),
    date(2026, 8, 15),
    date(2026, 9, 24),
    date(2026, 9, 25),
    date(2026, 10, 3),
    date(2026, 10, 9),
    date(2026, 12, 25),
}

def main():
    today = date.today()
    weekday = today.weekday()
    if weekday >= 5:
        return
    if today in HOLIDAYS_2026:
        return

    mode = sys.argv[1] if len(sys.argv) > 1 else "morning"
    if mode == "morning":
        msg = "☀️ 아침 학습 체크인\n오늘의 주제: CNN, 정규화(Normalization), 드롭아웃(Dropout)\n수업 시간: 09:00 ~ 18:00\n준비물: 노트북, 어제 복습 노트\n화이팅! 💪"
    else:
        msg = "🌙 저녁 학습 체크인\n오늘 하루 수고했어.\n학습 시간 기록 + 복습 여부만 알려줘."
    print(msg)

if __name__ == "__main__":
    main()
