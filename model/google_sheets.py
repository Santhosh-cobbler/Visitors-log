import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os


def connect_sheet():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    cred_path = os.path.join(BASE_DIR, "credentials.json")

    creds = ServiceAccountCredentials.from_json_keyfile_name(
        cred_path, scope
    )

    client = gspread.authorize(creds)

    sheet = client.open("Air_data_connect").sheet1
    return sheet