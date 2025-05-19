import os
import telebot
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

BOT_TOKEN = os.environ.get('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)

contador_mensajes = {}

excel_file = 'datos_usuarios.xlsx'

# Crear el archivo si no existe
if not os.path.exists(excel_file):
    df_init = pd.DataFrame(columns=['ID', 'Nombre completo', 'Correo', 'Celular', 'Colegio', 'Puntaje Icfes', 'Estrato socioeconómico'])
    df_init.to_excel(excel_file, index=False)



@bot.message_handler(commands=['start'])
def send_welcome(message):
    
    user_id = message.from_user.id
    if user_id not in contador_mensajes:

        bot.reply_to(message,"""

        Hola, gracias por decirle sí a Icesi!
        Estoy aquí para acompañarte en el proceso de ingreso a la U. ¿Cómo puedo ayudarte? ✨😀

        Para mejorar tu experiencia, los datos personales que suministre por este medio serán tratados conforme con nuestra política de tratamiento de datos personales
        ▶️https://www.icesi.edu.co/r/politicadatos. Si estás de acuerdo continúa en el chat, en caso de ser menor de edad aceptas tener la autorización de tus padres.

        """)

        bot.reply_to(message,text="""

        👩🏻‍💻 Buen día, mucho gusto, soy tu asesor educativo🎓 Gracias por su interés en Icesi
    
            Por favor, me puedes confirmar los siguientes datos:
            Nombre completo:
            Correo:
            Celular:
            Colegio:
            Puntaje Icfes:
            Estrato socioeconómico: 

        """)
    else:
        bot.send_message(
            message.chat.id,
            """Que información deseas conocer sobre Icesi?",
            - becas y financiamiento 
            - Docentes
            - identidad institucional
            - Trayectorias profesionales
            - admisiones """
        )

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    texto = message.text.strip()
    
    if user_id not in contador_mensajes:
        contador_mensajes[user_id] = 1
    else:
        contador_mensajes[user_id] += 1

    if contador_mensajes[user_id] ==1:
        bot.send_message(message.chat.id, "Gracias por la información. Ahora sobre que quisieras saber de Icesi?")
        bot.send_message(
            message.chat.id,
            """Que información deseas conocer sobre Icesi?",
            - becas y financiamiento 
            - Docentes
            - identidad institucional
            - Trayectorias profesionales
            - admisiones """
        )

        

        datos = extraer_datos_usuario(texto)

        if datos:
            guardar_datos_en_excel(user_id, datos)
            bot.send_message(message.chat.id, "✅ ¡Datos guardados correctamente en la base de datos!")

        bot.set_webhook(url='https://1e59-190-130-100-127.ngrok-free.app/webhook-test/64e5a7ed-8d08-4e7f-9ede-22e7643f08c1/webhook')







def extraer_datos_usuario(texto):
    campos = ["Nombre completo", "Correo", "Celular", "Colegio", "Puntaje Icfes", "Estrato socioeconómico"]
    datos = {}
    for linea in texto.split('\n'):
        if ':' in linea:
            clave, valor = linea.split(':', 1)
            clave = clave.strip()
            valor = valor.strip()
            if clave in campos:
                datos[clave] = valor
    if len(datos) == len(campos):
        return datos
    return None

def guardar_datos_en_excel(user_id, datos):
    df = pd.read_excel(excel_file)
    datos_fila = {
        'ID': user_id,
        'Nombre completo': datos['Nombre completo'],
        'Correo': datos['Correo'],
        'Celular': datos['Celular'],
        'Colegio': datos['Colegio'],
        'Puntaje Icfes': datos['Puntaje Icfes'],
        'Estrato socioeconómico': datos['Estrato socioeconómico']
    }
    df = pd.concat([df, pd.DataFrame([datos_fila])], ignore_index=True)
    df.to_excel(excel_file, index=False)


bot.remove_webhook()


bot.infinity_polling()