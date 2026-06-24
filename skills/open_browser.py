#!/usr/bin/env python3
"""
Brave 브라우저로 URL 열기
사용자가 직접 볼 수 있고 조작할 수 있습니다.

사용법:
  python open_browser.py <URL>
  python open_browser.py https://www.google.com
"""
import sys
import subprocess

BRAVE_PATH = r"C:\Users\sxeyc\AppData\Local\BraveSoftware\Brave-Browser\Application\brave.exe"

def open_url(url: str, new_window: bool = False):
    """Brave 브라우저로 URL을 연다"""
    args = [BRAVE_PATH]
    if new_window:
        args.append("--new-window")
    args.append(url)
    proc = subprocess.Popen(args)
    print(f"[OK] 브라우저 열림: {url} (PID: {proc.pid})")
    return proc

def open_with_playwright(url: str, headless: bool = False):
    """Playwright로 URL을 연다 (자동화 가능)"""
    from playwright.sync_api import sync_playwright
    
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=headless,
            executable_path=BRAVE_PATH,
            args=['--no-sandbox', '--disable-blink-features=AutomationControlled']
        )
        page = browser.new_page()
        page.goto(url)
        print(f"[OK] 브라우저 열림: {url}")
        print(f"페이지 타이틀: {page.title()}")
        return browser, page

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("사용법: python open_browser.py <URL> [--playwright]")
        print("예시:")
        print("  python open_browser.py https://www.google.com")
        print("  python open_browser.py https://notebooklm.google.com --playwright")
        sys.exit(1)

    url = sys.argv[1]
    use_playwright = "--playwright" in sys.argv

    if use_playwright:
        browser, page = open_with_playwright(url, headless=False)
        # 사용자가 브라우저를 닫을 때까지 대기
        input("브라우저를 닫으려면 Enter를 눌러주세요...")
        browser.close()
    else:
        open_url(url)
