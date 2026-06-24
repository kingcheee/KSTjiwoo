#!/usr/bin/env python3
"""브라우저 열기 - Playwright + Brave"""
from playwright.sync_api import sync_playwright
import time

brave_path = r"C:\Users\sxeyc\AppData\Local\BraveSoftware\Brave-Browser\Application\brave.exe"

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=False,
        executable_path=brave_path,
        args=['--no-sandbox', '--disable-blink-features=AutomationControlled']
    )
    page = browser.new_page()
    page.goto("https://www.google.com")
    print(f"[OK] 브라우저 열기 성공! 페이지: {page.title()}")
    time.sleep(5)
    browser.close()
    print("[OK] 브라우저 닫힘")
