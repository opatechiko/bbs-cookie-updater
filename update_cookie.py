import os
import json
import gspread
from google.oauth2.service_account import Credentials

# ===============================
# スプレッドシート設定
# ===============================
SPREADSHEET_NAME = "カナダ監視設定"   # ← スプレッドシート名
WORKSHEET_NAME = "config"              # ← シート名
CELL_LOCATION = "B2"                   # ← 書き込みセル

# ===============================
# Google Sheets 認証
# ===============================
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

# ===============================
# シート取得とテスト書き込み
# ===============================
try:
    ws = gc.open(SPREADSHEET_NAME).worksheet(WORKSHEET_NAME)
    print(f"✅ Connected to sheet: {ws.title}")

    # 現在のセルの値を表示
    current_value = ws.acell(CELL_LOCATION).value
    print(f"Current value in {CELL_LOCATION}: {current_value}")

    # テスト書き込み
    ws.update(CELL_LOCATION, "TEST COOKIE")
    print(f"✅ Test write completed: {CELL_LOCATION} updated to 'TEST COOKIE'")

except Exception as e:
    print(f"❌ Error: {e}")
