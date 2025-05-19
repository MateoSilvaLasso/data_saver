import gspread
from oauth2client.service_account import ServiceAccountCredentials

class SaverOnline:
    def __init__(self, creds_json_path, sheet_name):
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(creds_json_path, scope)
        client = gspread.authorize(creds)
        self.sheet = client.open(sheet_name).sheet1

    def guardar_datos(self, nombre_completo, correo, celular, colegio, puntaje_icfes, estrato):
        datos_fila = {
            'Nombre completo': nombre_completo,
            'Correo': correo,
            'Celular': celular,
            'Colegio': colegio,
            'Puntaje Icfes': puntaje_icfes,
            'Estrato socioeconómico': estrato
        }
        self.sheet.append_row(datos_fila)
