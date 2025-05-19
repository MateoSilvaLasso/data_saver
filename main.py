from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from saver import SaverOnline
from dotenv import load_dotenv
import os
app = FastAPI()


class UserData(BaseModel):
    info: str


@app.post("/save_user_data")
def save_user_data(user_data: UserData):
    try:
        saver = SaverOnline('TdG - I-Andy')
        saver.guardar_datos(user_data.info)
        return {"message": "Datos guardados correctamente en la base de datos."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))