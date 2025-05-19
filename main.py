from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from saver import SaverOnline
app = FastAPI()


class UserData(BaseModel):
    nombre_completo: str
    correo: str
    celular: str
    colegio: str
    puntaje_icfes: str
    estrato: str


@app.post("/save_user_data")
def save_user_data(user_data: UserData):
    try:
        saver = SaverOnline('./credentials.json', 'TdG - I-Andy')
        saver.guardar_datos(user_data.nombre_completo, user_data.correo, user_data.celular, user_data.colegio, user_data.puntaje_icfes, user_data.estrato)
        return {"message": "Datos guardados correctamente en la base de datos."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))