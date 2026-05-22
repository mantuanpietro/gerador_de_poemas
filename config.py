POEMA_SCHEMA = {

    "type": "object",

    "properties": {

        "titulo": {
            "type": "string"
        },

        "tema": {
            "type": "string"
        },

        "sentimento": {
            "type": "string"
        },

        "poema": {

            "type": "array",

            "items": {
                "type": "string"
            }
        }
    },

    "required": [
        "titulo",
        "tema",
        "sentimento",
        "poema"
    ]
}

SYSTEM_INSTRUCTION = """
Você é um poeta profissional extremamente criativo.

Crie poemas:
- emocionantes
- profundos
- criativos
- bonitos

Sempre responda:
- em português
- apenas no JSON solicitado
"""