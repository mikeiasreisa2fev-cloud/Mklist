import requests, os, base64, json
from datetime import datetime

URL_ORIGEM = "https://seu-link-da-lista.m3u"
USUARIO = "seu-usuario"
REPO = "seu-repositorio"
# Token vem automaticamente do Actions, não precisa criar nada:
TOKEN = os.getenv("GITHUB_TOKEN")

def baixar():
    try:
        r = requests.get(URL_ORIGEM, timeout=15)
        r.raise_for_status()
        return r.text
    except:
        return None

def atualizar(conteudo):
    headers = {"Authorization": f"token {TOKEN}"}
    url = f"https://api.github.com/repos/{USUARIO}/{REPO}/contents/lista.m3u?ref=main"
    info = requests.get(url, headers=headers).json()
    dados = {
        "message": "Atualiza lista automática",
        "content": base64.b64encode(conteudo.encode("utf-8")).decode(),
        "sha": info["sha"],
        "branch": "main"
    }
    requests.put(url, headers=headers, data=json.dumps(dados))

if __name__ == "__main__":
    nova = baixar()
    if nova:
        atualizar(nova)
        print("✅ Atualizado com token interno do GitHub")
