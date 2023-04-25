import requests
from transformers import GPT2Tokenizer
from os import getenv
from dotenv import load_dotenv

load_dotenv()

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
_LIMIT_TOKENS = 4096
_LIMIT_TOKENS_PROMPT = int(_LIMIT_TOKENS / 2)

def _contarTokens(text: str) -> int:
    tokens = tokenizer(text).data["input_ids"]
    return len(tokens)


async def refinarTexto(prompt: str) -> str:
    prompt = "Deixe o seguinte texto gramaticamente correto: \n\n" + prompt

    n_tokens = _contarTokens(prompt)

    params = {
        "model": "text-davinci-003",
        "prompt": prompt,
        "max_tokens": _LIMIT_TOKENS - n_tokens,
        "temperature": 0
    }

    headers = {
        "Authorization": "Bearer " + getenv("CHAT_GPT_API_KEY"),
        "User-Agent": "MyApp/1.0",
        "Content-Type": "application/json"
    }

    resposta = ""

    try:
        response = requests.post("https://api.openai.com/v1/completions", json=params, headers=headers, timeout=(60 * 5))
        resposta = str(response.json()["choices"][0]["text"])

        if resposta.startswith("\nR: "):
            resposta = resposta[len("\nR: "):]

        elif resposta.startswith("R: "):
            resposta = resposta[len("R: "):]

        elif resposta.startswith("\nResposta: "):
            resposta = resposta[len("\nResposta: "):]

        elif resposta.startswith("Resposta: "):
            resposta = resposta[len("Resposta: "):]
    except:
        resposta = prompt

    return resposta.strip()