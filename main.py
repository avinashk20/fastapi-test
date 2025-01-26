from fastapi import FastAPI, HTTPException
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from models import UserData

app = FastAPI()

SPREADSHEET_ID = '1E1hIBpb5WV1x-e5oKBcQOpL9431I2B6itrHKLvSZxII'
RANGE_NAME = 'Sheet1!A2:B' 
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

def get_google_sheets_service():
    try:
        from google.oauth2 import service_account
        
        creds = service_account.Credentials.from_service_account_file(
            'creds/credentials.json', 
            scopes=SCOPES
        )
        return build('sheets', 'v4', credentials=creds)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Authentication error: {str(e)}")

@app.get("/users", response_model=list[UserData])
async def fetch_users():
    try:
        service = get_google_sheets_service()
        sheet = service.spreadsheets()
        
        result = sheet.values().get(
            spreadsheetId=SPREADSHEET_ID, 
            range=RANGE_NAME
        ).execute()
        
        values = result.get('values', [])
        
        if not values:
            raise HTTPException(status_code=404, detail="No data found")
        
        users = [UserData(email=row[0], phone=row[1]) for row in values]
        
        return users
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "hello world"}
    