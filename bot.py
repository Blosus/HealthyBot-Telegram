#!/usr/bin/env python3

import logging
import os
import random
import re
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN")

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

SALUDOS = ["hola", "hello", "hi", "buenas", "buenos días", "buenos dias", "buen día", "buen dia", "qué onda", "que onda", "hey", "ey", "saludos"]
COMO_ESTAS = ["cómo estás", "como estas", "cómo está", "como esta", "qué tal", "que tal", "cómo te va", "como te va", "todo bien", "cómo andas", "como andas"]

RESPUESTAS_SALUDO = [
    "¡Hola! Soy HealthyBot. Puedo darte info sobre dietas, nutrición e hidratación. ¿En qué te ayudo?",
    "¡Hey! Aquí para ayudarte con temas de salud y nutrición. ¿Qué quieres saber?",
    "¡Buenas! Escríbeme sobre lo que quieras saber: dieta, proteínas, hidratación, calorías... ¿qué necesitas?",
]

RESPUESTAS_COMO_ESTAS = [
    "¡Muy bien gracias! Listo para ayudarte con tips de salud. ¿Qué quieres saber?",
    "¡Todo bien por aquí! ¿Y tú cómo vas con tu alimentación? Cuéntame en qué te puedo ayudar.",
    "¡Excelente! Siempre listo para compartir info de nutrición. ¿Tienes alguna duda?",
]

TIPS = [
    "Toma agua antes de cada comida, ayuda a la digestión y a controlar las porciones.",
    "Intenta llenar la mitad de tu plato con verduras en cada comida.",
    "Come despacio — tu cerebro tarda ~20 minutos en registrar que estás lleno.",
    "Los frutos secos son un snack excelente: sacian y son buenos para el corazón.",
    "Empieza el día con un vaso de agua antes del café o desayuno.",
    "Prefiere frutas enteras al jugo — conservas la fibra y reduces el azúcar.",
    "Duerme bien: el mal sueño aumenta el apetito y afecta el metabolismo.",
]

INFO = {
    "proteína": (
        "*Proteína*\n\n"
        "Esencial para músculo, sistema inmune y hormonas.\n"
        "Ingesta recomendada: ~0.8–1.2g por kg de peso.\n\n"
        "Fuentes: pollo, huevo, atún, lentejas, yogur griego, tofu."
    ),
    "proteina": (
        "*Proteína*\n\n"
        "Esencial para músculo, sistema inmune y hormonas.\n"
        "Ingesta recomendada: ~0.8–1.2g por kg de peso.\n\n"
        "Fuentes: pollo, huevo, atún, lentejas, yogur griego, tofu."
    ),
    "carbohidratos": (
        "*Carbohidratos*\n\n"
        "Son la principal fuente de energía del cuerpo.\n"
        "Prefiere los complejos: avena, arroz integral, camote, legumbres.\n"
        "Limita los refinados: pan blanco, azúcar, refrescos."
    ),
    "carbohidrato": (
        "*Carbohidratos*\n\n"
        "Son la principal fuente de energía del cuerpo.\n"
        "Prefiere los complejos: avena, arroz integral, camote, legumbres.\n"
        "Limita los refinados: pan blanco, azúcar, refrescos."
    ),
    "grasas": (
        "*Grasas saludables*\n\n"
        "Necesarias para el cerebro, hormonas y vitaminas A, D, E, K.\n\n"
        "Buenas fuentes: aguacate, aceite de oliva, nueces, salmón, semillas.\n"
        "Evita: grasas trans y frituras procesadas."
    ),
    "grasa": (
        "*Grasas saludables*\n\n"
        "Necesarias para el cerebro, hormonas y vitaminas A, D, E, K.\n\n"
        "Buenas fuentes: aguacate, aceite de oliva, nueces, salmón, semillas.\n"
        "Evita: grasas trans y frituras procesadas."
    ),
    "hidratación": (
        "*Hidratación*\n\n"
        "Fórmula general: ~35ml por kg de peso al día.\n"
        "Ejemplo: si pesas 70kg → toma ~2.5L de agua diarios.\n\n"
        "Señales de deshidratación: orina oscura, cansancio, dolor de cabeza.\n"
        "Tip: empieza la mañana con un vaso de agua."
    ),
    "hidratacion": (
        "*Hidratación*\n\n"
        "Fórmula general: ~35ml por kg de peso al día.\n"
        "Ejemplo: si pesas 70kg → toma ~2.5L de agua diarios.\n\n"
        "Señales de deshidratación: orina oscura, cansancio, dolor de cabeza.\n"
        "Tip: empieza la mañana con un vaso de agua."
    ),
    "agua": (
        "*Agua*\n\n"
        "Fórmula general: ~35ml por kg de peso al día.\n"
        "Ejemplo: si pesas 70kg → toma ~2.5L de agua diarios.\n\n"
        "Señales de deshidratación: orina oscura, cansancio, dolor de cabeza.\n"
        "Tip: empieza la mañana con un vaso de agua."
    ),
    "fibra": (
        "*Fibra*\n\n"
        "Mejora la digestión, reduce el colesterol y regula el azúcar en sangre.\n"
        "Recomendado: 25g/día (mujeres) | 38g/día (hombres)\n\n"
        "Fuentes: legumbres, avena, frutas, verduras, chía, linaza."
    ),
    "calorías": (
        "*Calorías*\n\n"
        "Una caloría es una unidad de energía. No todas las calorías son iguales — la calidad importa.\n\n"
        "Aprox. recomendado:\n"
        "• Mujeres: 1,800–2,000 kcal/día\n"
        "• Hombres: 2,200–2,500 kcal/día\n\n"
        "Varía según edad, peso y actividad física."
    ),
    "calorias": (
        "*Calorías*\n\n"
        "Una caloría es una unidad de energía. No todas las calorías son iguales — la calidad importa.\n\n"
        "Aprox. recomendado:\n"
        "• Mujeres: 1,800–2,000 kcal/día\n"
        "• Hombres: 2,200–2,500 kcal/día\n\n"
        "Varía según edad, peso y actividad física."
    ),
    "mediterránea": (
        "*Dieta Mediterránea*\n\n"
        "Una de las más estudiadas y recomendadas del mundo.\n\n"
        "Verduras, frutas, granos enteros\n"
        "Aceite de oliva como grasa principal\n"
        "Pescado 2–3 veces por semana\n"
        "Poca carne roja\n\n"
        "Beneficios: reduce riesgo de enfermedades cardíacas y diabetes."
    ),
    "mediterranea": (
        "*Dieta Mediterránea*\n\n"
        "Una de las más estudiadas y recomendadas del mundo.\n\n"
        "Verduras, frutas, granos enteros\n"
        "Aceite de oliva como grasa principal\n"
        "Pescado 2–3 veces por semana\n"
        "Poca carne roja\n\n"
        "Beneficios: reduce riesgo de enfermedades cardíacas y diabetes."
    ),
    "keto": (
        "*Dieta Keto (Cetogénica)*\n\n"
        "Muy baja en carbohidratos, alta en grasas. El cuerpo quema grasa como energía principal.\n\n"
        "Carne, pescado, huevos, aguacate, nueces, aceites\n"
        "Pan, arroz, pasta, azúcar, la mayoría de frutas\n\n"
        "Útil para: pérdida de peso, control de azúcar en sangre.\n"
        "Consulta a un médico antes de empezarla."
    ),
    "ayuno": (
        "*Ayuno Intermitente*\n\n"
        "Patrón de alimentación que alterna periodos de comer y ayunar.\n\n"
        "El más común: 16:8 — ayunas 16h, comes en ventana de 8h.\n\n"
        "Beneficios: pérdida de peso, mejora de insulina, claridad mental.\n"
        "No recomendable para embarazadas, diabéticos o personas con trastornos alimenticios."
    ),
    "vitaminas": (
        "* Vitaminas clave*\n\n"
        "• Vitamina D — huesos e inmunidad. Fuente: sol, pescado graso, huevo.\n"
        "• Vitamina C — antioxidante. Fuente: cítricos, pimiento, kiwi.\n"
        "• B12 — energía y nervios. Fuente: carne, lácteos (suplemento si eres vegano).\n"
        "• Vitamina A — visión y piel. Fuente: zanahoria, camote, espinacas."
    ),
    "vitamina": (
        "💊 *Vitaminas clave*\n\n"
        "• Vitamina D — huesos e inmunidad. Fuente: sol, pescado graso, huevo.\n"
        "• Vitamina C — antioxidante. Fuente: cítricos, pimiento, kiwi.\n"
        "• B12 — energía y nervios. Fuente: carne, lácteos (suplemento si eres vegano).\n"
        "• Vitamina A — visión y piel. Fuente: zanahoria, camote, espinacas."
    ),
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "¡Hola! Soy HealthyBot \n\n"
        "Escríbeme sobre cualquier tema de salud y nutrición:\n"
        "proteína, carbohidratos, grasas, fibra, agua, calorías,\n"
        "dieta mediterránea, keto, ayuno, vitaminas...\n\n"
        "También puedes pedir un /tip o calcular tu /bmi."
    )


async def tip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"{random.choice(TIPS)}")


async def bmi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) != 2:
        await update.message.reply_text("Uso: /bmi <peso en kg> <altura en cm>\nEjemplo: /bmi 70 175")
        return
    try:
        peso = float(args[0])
        altura = float(args[1]) / 100
        if peso <= 0 or altura <= 0:
            raise ValueError
        imc = peso / (altura ** 2)
        if imc < 18.5:
            cat = "Bajo peso"
        elif imc < 25:
            cat = "Peso normal"
        elif imc < 30:
            cat = "Sobrepeso"
        else:
            cat = "Obesidad"
        await update.message.reply_text(
            f"Tu IMC es: *{imc:.1f}*\nCategoría: *{cat}*\n\n_El IMC es solo una referencia. Consulta a un profesional de salud._",
            parse_mode="Markdown",
        )
    except ValueError:
        await update.message.reply_text("Por favor ingresa números válidos. Ejemplo: /bmi 70 175")


def es_saludo(texto):
    # \b evita que "hi" coincida con "hidratación".
    return any(re.match(rf"{re.escape(s)}\b", texto) for s in SALUDOS)


async def mensaje(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.lower().strip()

    if es_saludo(texto):
        await update.message.reply_text(random.choice(RESPUESTAS_SALUDO))
        return

    if any(c in texto for c in COMO_ESTAS):
        await update.message.reply_text(random.choice(RESPUESTAS_COMO_ESTAS))
        return

    for clave, respuesta in INFO.items():
        if clave in texto:
            await update.message.reply_text(respuesta, parse_mode="Markdown")
            return

    await update.message.reply_text(
        "No encontré info sobre eso.\n\n"
        "Puedes preguntarme sobre: proteína, carbohidratos, grasas, fibra, agua, calorías, vitaminas, keto, ayuno, dieta mediterránea.\n"
        "O pide un /tip o calcula tu /bmi."
    )


def main():
    if not BOT_TOKEN:
        raise SystemExit("Falta la variable de entorno BOT_TOKEN (el token que da @BotFather).")
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("tip", tip))
    app.add_handler(CommandHandler("bmi", bmi))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, mensaje))
    print("HealthyBot corriendo...")
    app.run_polling()


if __name__ == "__main__":
    main()