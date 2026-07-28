import requests, os, base64, json
from datetime import datetime

# 👇 TROQUE AQUI: coloque seus dados
URL_ORIGEM = "https://seu-link-da-lista-ou-site.m3u"
USUARIO = "seu-nome-no-github"
REPO = "nome-do-seu-repositorio"

TOKEN = os.getenv("GITHUB_TOKEN")

def pegar_lista_nova():
    try:
        r = requests.get(URL_ORIGEM, timeout=15)
        r.raise_for_status()
        return r.text
    except:
        return None

def atualizar_no_git(conteudo):
    headers = {"Authorization": f"token {TOKEN}"}
    info = requests.get(f"https://api.github.com/repos/{USUARIO}/{REPO}/contents/lista.m3u?ref=main", headers=headers).json()
    dados = {
        "message": "Atualizei a lista ✅",
        "content": base64.b64encode(conteudo.encode("utf-8")).decode(),
        "sha": info["sha"],
        "branch": "main"
    }
    requests.put(f"https://api.github.com/repos/{USUARIO}/{REPO}/contents/lista.m3u", headers=headers, data=json.dumps(dados))

if __name__ == "__main__":
    nova = pegar_lista_nova()
    if nova: atualizar_no_git(nova)
