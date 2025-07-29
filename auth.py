import gspread
from google.oauth2.service_account import Credentials

# スプレッドシートID（必要に応じて変更）
SPREADSHEET_ID = "1ia3ljvxeVCgZo5gXryN96yHHlDwlv6THmLDmM8UiI1U"

# JSONキーのパス（client_secret.jsonは.gitignoreに含める）
SERVICE_ACCOUNT_FILE = "client_secret.json"

# 使用するスコープ（最小限に）
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", 
          "https://www.googleapis.com/auth/drive"]

# 認証とクライアントの作成
credentials = Credentials.from_service_account_file(
    "student-465406-8c6c35e39ecf.json",
    scopes=SCOPES
)
client = gspread.authorize(credentials)
