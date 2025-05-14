
import json, datetime, os

CUMPLE_FILE = "cumples.json"
USERS_FILE = "users_activity.json"

def load_birthdays():
    if not os.path.exists(CUMPLE_FILE):
        return []
    with open(CUMPLE_FILE, 'r') as f:
        return json.load(f)

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

def detect_inactive_users():
    users = load_users()
    today = datetime.datetime.now()
    inactive = []
    for user, last_active in users.items():
        last_date = datetime.datetime.strptime(last_active, '%Y-%m-%d')
        if (today - last_date).days > 30:
            inactive.append(user)
    return inactive

if __name__ == "__main__":
    upcoming = upcoming_birthdays()
    print("Cumpleaños próximos (7 días):")
    print("\n".join(upcoming) if upcoming else "Ninguno")

    if datetime.datetime.now().day == 1:
        print("Usuarios inactivos (+30 días):")
        print("\n".join(detect_inactive_users()))
