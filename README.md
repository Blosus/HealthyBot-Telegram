# HealthyBot (Telegram)

Bot de Telegram en español que responde preguntas básicas de salud y nutrición.

- Responde saludos y conversación sencilla.
- Da información sobre proteína, carbohidratos, grasas, fibra, hidratación, calorías, vitaminas, keto, ayuno y dieta mediterránea.
- `/tip`: un consejo de salud al azar.
- `/bmi <peso kg> <altura cm>`: calcula el IMC y su categoría.

> La información es general y no sustituye la opinión de un profesional de la salud.

## Tecnologías

Python 3 y [python-telegram-bot](https://python-telegram-bot.org/) (async).

## Ejecutar

1. Crea un bot con [@BotFather](https://t.me/BotFather) y copia el token.
2. Instala las dependencias y ejecuta:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export BOT_TOKEN='tu_token'
python bot.py
```

## Pruebas

```bash
python test_bot.py
```
