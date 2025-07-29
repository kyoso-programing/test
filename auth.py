# auth.py
import gspread
from google.oauth2.service_account import Credentials

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = "1ia3ljvxeVCgZo5gXryN96yHHlDwlv6THmLDmM8UiI1U"

def get_gspread_client():
    creds = Credentials.from_service_account_file(
        "auth.json",  # ← ここにサービスアカウント鍵のファイル名を指定
        scopes=SCOPES
    )
    return gspread.authorize(creds)
