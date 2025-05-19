import gspread
import json
from dotenv import load_dotenv
import os
from oauth2client.service_account import ServiceAccountCredentials

class SaverOnline:
    def __init__(self, sheet_name):
        load_dotenv()
        creds_json = os.getenv("credentials")

        # Convertir a dict
        if creds_json is None:
            raise ValueError("No se encontraron las credenciales en el .env")
        creds_info = json.loads(creds_json)
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_info, scope)
        client = gspread.authorize(creds)
        self.sheet = client.open(sheet_name).sheet1

    def guardar_datos(self, nombre_completo, correo, celular, colegio, puntaje_icfes, estrato):
        fila = [nombre_completo, correo, celular, colegio, puntaje_icfes, estrato]
        self.sheet.append_row(fila)
