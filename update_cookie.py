import time
import json
import os
import gspread
from google.oauth2.service_account import Credentials
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# ===============================
# 設定
# ===============================
BBS_URL = "https://bbs1.sekkaku.net/bbs/canada2025/"
USERNAME = "カナダ"
PASSWORD = "a"

# 書き込み先 Google Sheets の設定
SPREADSHEET_NAME = "カナダ監視設定"   # ← あなたのスプレッドシート名に変更
WORKSHEET_NAME = "config"              # ← Cookieを書き込むシート名
CELL_LOCATION = "B2"                   # ← Cookieを入れるセル

# ===============================
# Google Sheets 認証
# ===============================
print("🔑 Authenticating with Google Sheets...")

credentials_json = os.environ.get("GOOGLE_CREDENTIALS")
if not credentials_json:
    raise RuntimeError("❌ GOOGLE_CREDENTIALS 環境変数が設定されていません。")

creds_dict = json.loads(credentials_json)
creds = Credentials.from_service_account_info(
    creds_dict,
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
)

gc = gspread.authorize(creds)
ws = gc.open(SPREADSHEET_NAME).worksheet(WORKSHEET_NAME)
print("✅ Connected to Google Sheets.")

# ===============================
# Chromeドライバ設定
# ===============================
print("🚀 Launching headless Chrome...")

chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # ===============================
    # ログイン処理
    # ===============================
    print(f"🌐 Accessing {BBS_URL}")
    driver.get(BBS_URL)
    time.sleep(2)

    name_input = driver.find_element(By.NAME, "member_name")
    pw_input = driver.find_element(By.NAME, "member_password")

    name_input.clear()
    name_input.send_keys(USERNAME)
    pw_input.clear()
    pw_input.send_keys(PASSWORD)

    login_btn = driver.find_element(By.XPATH, "//input[@type='submit' and @value='ログイン']")
    login_btn.click()

    time.sleep(3)
    print("✅ Login completed.")

    # ===============================
    # クッキー取得
    # ===============================
    cookies = driver.get_cookies()
    cookie_str = "; ".join([f"{c['name']}={c['value']}" for c in cookies])
    print(f"🍪 Cookie: {cookie_str}")

    # ===============================
    # Google Sheetsへ書き込み（テスト）
    # ===============================
    print(f"Updating sheet {SPREADSHEET_NAME}, sheet {WORKSHEET_NAME}, cell {CELL_LOCATION}...")
    ws.update(CELL_LOCATION, "TEST COOKIE")
    print("✅ Test write completed")

except Exception as e:
    print(f"❌ Error: {e}")
finally:
    driver.quit()
    print("🧹 Chrome closed.")
