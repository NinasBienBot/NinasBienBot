
# WhatsApp Bot N.A.C.A.

Este bot está diseñado para ejecutarse con Flask y Twilio para responder mensajes de WhatsApp relacionados con el universo del podcast *Niñas Bien* y su partido ficticio N.A.C.A.

## Funcionalidades

- Respuestas automáticas a comandos como `/frase`, `/evento`, `/cumpleaños`, `/cumples`, etc.
- Registro de cumpleaños
- Recordatorio diario de cumpleaños próximos (7 días)
- Detección mensual de usuarios inactivos (+30 días sin enviar mensajes)

## Estructura del Proyecto

| Archivo | Descripción |
|--------|-------------|
| `app.py` | Código principal del bot Flask para WhatsApp |
| `scheduler.py` | Script que imprime cumpleaños próximos y usuarios inactivos |
| `requirements.txt` | Librerías necesarias para instalar con pip |
| `Procfile` | Instrucción para ejecutar el bot en Render o Heroku |
| `cumples.json` | Base de datos de cumpleaños |
| `users_activity.json` | Base de datos de actividad de usuarios |

## Instalación Local

1. Clona el repositorio:

```
git clone https://github.com/tu-usuario/tu-repo.git
cd tu-repo
```

2. Instala dependencias:

```
pip install -r requirements.txt
```

3. Ejecuta el bot:

```
python app.py
```

## Despliegue en Render

1. Sube el código a un repositorio de GitHub.
2. Entra a [Render](https://render.com/) y crea un nuevo **Web Service**.
3. Conecta tu repo de GitHub.
4. Render detectará automáticamente el `requirements.txt` y `Procfile`.
5. Establece el comando de start: `python app.py`.

Una vez desplegado, Render te dará una URL pública (ej. `https://naca-bot.onrender.com/whatsapp`).

6. Entra a tu cuenta de [Twilio](https://www.twilio.com/) > Sandbox de WhatsApp.
7. Coloca la URL de Render como webhook en la sección de mensajes entrantes.

## Cron Jobs

En Render o Railway:

- **Script:** `python scheduler.py`
- **Tareas:**
  - **Diario (8 AM):** enviar cumpleaños próximos
  - **Mensual (1ro):** detectar usuarios inactivos

## Comandos Disponibles en WhatsApp

- `/frase` – Recibe una frase icónica
- `/evento` – Info del evento ficticio
- `/episodio` o `podcast` – Último episodio del podcast
- `/cumpleaños DD-MM Nombre` – Registra cumpleaños
- `/cumples` – Ver próximos cumpleaños
- `hola` o `chisme` – Mensajes personalizados

---

Inspirado por el poder del chisme y el arte del podcasting bien hecho.
