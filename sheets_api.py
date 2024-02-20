import json
import os

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build


def authenticate_sheets():
  creds_json_str = os.environ.get("SHEETS_API_KEY")
  if creds_json_str is None:
    raise ValueError("No se encontró la variable de entorno 'SHEETS_API_KEY'")

  try:
    creds_json = json.loads(creds_json_str)
  except json.JSONDecodeError:
    raise ValueError(
        "La variable de entorno 'SHEETS_API_KEY' no contiene un JSON válido")

  creds = Credentials.from_service_account_info(creds_json)
  service = build('sheets', 'v4', credentials=creds)
  return service


def append_to_sheet(service, spreadsheet_id, range_name, values):
  body = {'values': values}
  result = service.spreadsheets().values().append(
      spreadsheetId=spreadsheet_id,
      range=range_name,
      valueInputOption='USER_ENTERED',
      insertDataOption='INSERT_ROWS',
      body=body).execute()
  return result


def read_sheet(service, spreadsheet_id, range_name):
  result = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id,
                                               range=range_name).execute()
  return result.get('values', [])
