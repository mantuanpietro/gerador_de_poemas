import os
import json

from flask import Flask, jsonify, request
from flask_cors import CORS

from google import genai
from google.genai import types

from dotenv import load_dotenv

from config import POEMA_SCHEMA, SYSTEM_INSTRUCTION

# Carrega .env
load_dotenv(dotenv_path=".env")

# API KEY
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

print("API KEY:", GEMINI_API_KEY)

# Verifica chave
if not GEMINI_API_KEY:
    raise ValueError("API KEY não encontrada.")

# Cliente Gemini
cliente = genai.Client(api_key=GEMINI_API_KEY)

# Flask
app = Flask(__name__)

# CORS
CORS(app)

# Função gerar poema
def generate_poem(tema, sentimento, estilo):

    prompt = f"""
    Crie um poema bonito e emocional.

    Tema: {tema}
    Sentimento: {sentimento}
    Estilo: {estilo}

    Responda apenas em JSON.
    """

    print("GERANDO POEMA...")

    response = cliente.models.generate_content(

        model="gemini-2.5-flash",

        contents=prompt,

        config=types.GenerateContentConfig(

            system_instruction=SYSTEM_INSTRUCTION,

            response_mime_type="application/json",

            response_schema=POEMA_SCHEMA
        )
    )

    print("RESPOSTA GEMINI:")
    print(response)

    return response.text.strip()

# Página inicial
@app.route("/")
def root():

    return jsonify({
        "status": "success",
        "message": "API Gerador de Poemas funcionando!"
    })

# Gerar poema
@app.route("/generate", methods=["POST"])
def generate():

    try:

        data = request.get_json()

        print("DADOS RECEBIDOS:")
        print(data)

        if not data:

            return jsonify({
                "status": "error",
                "message": "JSON não enviado"
            }), 400

        tema = data.get("tema")
        sentimento = data.get("sentimento")
        estilo = data.get("estilo")

        print("TEMA:", tema)
        print("SENTIMENTO:", sentimento)
        print("ESTILO:", estilo)

        if not tema or not sentimento or not estilo:

            return jsonify({
                "status": "error",
                "message": "Preencha todos os campos"
            }), 400

        poema_json = generate_poem(
            tema,
            sentimento,
            estilo
        )

        print("JSON RECEBIDO:")
        print(poema_json)

        poema = json.loads(poema_json)

        return jsonify({
            "status": "success",
            "dados_poema": poema
        })

    except Exception as e:

        print("ERRO COMPLETO:")
        print(e)

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# Rodar servidor
if __name__ == "__main__":

    app.run(
        debug=True,
        port=5001
    )