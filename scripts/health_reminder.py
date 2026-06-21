#!/usr/bin/env python3
import sys
mode = sys.argv[1] if len(sys.argv)>1 else "lunch"
if mode=="lunch":
    print("🥗 점심 시간!\n오늘 스파게티 뭐 먹을지 고민중이면 '오늘의 스파게티 추천해줘' 라고 해줘!")
elif mode=="vitamin":
    print("💊 영양제 시간이야!\n오늘 하루도 파이팅 💪")
