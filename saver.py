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

    def guardar_datos(self, data_str: str):
        campos = [
            "Nombre completo",
            "Correo",
            "Celular",
            "Colegio",
            "Puntaje Icfes",
            "Estrato socioeconómico"
        ]
        datos = {}

        # Dividir por líneas y luego extraer campo: valor
        for linea in data_str.strip().split('\n'):
            if ':' in linea:
                clave, valor = linea.split(':', 1)
                clave = clave.strip()
                valor = valor.strip()
                if clave in campos:
                    datos[clave] = valor

        # Validar que están todos los campos
        if len(datos) != len(campos):
            raise ValueError("Faltan datos o hay campos incorrectos en la entrada")

        fila = [datos[campo] for campo in campos]
        self.sheet.append_row(fila)

