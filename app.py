
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import random, json, datetime, os

app = Flask(__name__)

chisme_phrases = [
    "‘Si por pendeja me caigo, por chismosa me levanto.’",
    "‘El chisme bien contado es periodismo ciudadano.’",
    "‘No es metiche si te lo cuentan solito.’"
]

help_text = """Comandos disponibles:
/frase - Recibe una frase icónica
/evento - Información del próximo evento
/ayuda - Lista de comandos
/episodio - Último episodio del podcast
/cumpleaños DD-MM Nombre - Registra tu cumple
/cumples - Ver próximos cumpleaños
"""

CUMPLE_FILE = "cumples.json"
USERS_FILE = "users_activity.json"

def load_birthdays():
    if not os.path.exists(CUMPLE_FILE):
        return []
    with open(CUMPLE_FILE, 'r') as f:
        return json.load(f)

def save_birthday(date_str, name):
    bd_list = load_birthdays()
    bd_list.append({"date": date_str, "name": name})
    with open(CUMPLE_FILE, 'w') as f:
        json.dump(bd_list, f)

def upcoming_birthdays():
    today = datetime.datetime.now().date()
    bd_list = load_birthdays()
    upcoming = []
    for bd in bd_list:
        bd_date = datetime.datetime.strptime(bd["date"], "%d-%m").replace(year=today.year).date()
        delta = (bd_date - today).days
        if 0 <= delta <= 7:
            upcoming.append(f"{bd['name']} - {bd['date']}")
    return upcoming

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

def save_users(data):
    with open(USERS_FILE, 'w') as f:
        json.dump(data, f)

def register_activity(from_number):
    users = load_users()
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    users[from_number] = today
    save_users(users)

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    incoming_msg = request.values.get("Body", "").strip()
    msg_lower = incoming_msg.lower()
    from_number = request.values.get("From", "")
    register_activity(from_number)

    resp = MessagingResponse()
    msg = resp.message()

    if msg_lower == "/frase" or msg_lower == "chisme":
        msg.body(random.choice(chisme_phrases))
    elif msg_lower == "/evento":
        msg.body("Siguiente evento N.A.C.A: 25 de mayo en el Parque México. ¡No faltes!")
    elif msg_lower == "/ayuda":
        msg.body(help_text)
    elif msg_lower == "/episodio" or msg_lower == "podcast":
        msg.body("Nuevo episodio: *La Chismosa del Año*. Escúchalo aquí: https://spotify.link/episodio123")
    elif msg_lower == "hola":
        msg.body("Hola, reina del chisme. ¿Qué se te ofrece hoy?")
    elif msg_lower.startswith("/cumpleaños"):
        try:
            parts = incoming_msg.split(" ", 2)
            date_str = parts[1]
            name = parts[2]
            datetime.datetime.strptime(date_str, "%d-%m")
            save_birthday(date_str, name)
            msg.body(f"Cumpleaños registrado: {name} el {date_str}")
        except:
            msg.body("Formato inválido. Usa: /cumpleaños DD-MM Nombre")
    elif msg_lower == "/cumples":
        upcoming = upcoming_birthdays()
        if upcoming:
            msg.body("Cumpleaños próximos:\n" + "\n".join(upcoming))
        else:
            msg.body("No hay cumpleaños próximos esta semana.")
    else:
        msg.body("No entendí tu mensaje. Usa /ayuda para ver lo que puedo hacer.")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
