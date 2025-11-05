from flask import Flask, request, jsonify
from ftplib import FTP
import os

app = Flask(__name__)

# Configuração FTP
FTP_HOST = 'smithioou3.ftp.evennode.com'
FTP_USER = 'smithioou3_9a76b'
FTP_PASS = '123456'

# Token simples de segurança (você pode mudar)
API_TOKEN = "seu_token_de_acesso_ftp_123"


def conectar_ftp():
    """Faz a conexão com o servidor FTP"""
    ftp = FTP(FTP_HOST)
    ftp.login(user=FTP_USER, passwd=FTP_PASS)
    return ftp


@app.route('/api/upload', methods=['POST'])
def api_upload():
    # Autenticação simples via token
    token = request.headers.get('Authorization')
    if token != f"Bearer {API_TOKEN}":
        return jsonify({"status": "erro", "mensagem": "Token inválido ou ausente"}), 401

    if 'arquivo' not in request.files:
        return jsonify({"status": "erro", "mensagem": "Nenhum arquivo enviado"}), 400

    arquivo = request.files['arquivo']
    if arquivo.filename == '':
        return jsonify({"status": "erro", "mensagem": "Nome de arquivo inválido"}), 400

    try:
        ftp = conectar_ftp()
        ftp.storbinary(f"STOR {arquivo.filename}", arquivo.stream)
        ftp.quit()
        return jsonify({"status": "sucesso", "mensagem": f"Arquivo '{arquivo.filename}' enviado com sucesso!"}), 200
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500


@app.route('/')
def home():
    return jsonify({
        "mensagem": "API FTP ativa! Use o endpoint /api/upload com método POST.",
        "exemplo": {
            "url": "/api/upload",
            "método": "POST",
            "headers": {"Authorization": "Bearer SEU_TOKEN"},
            "body": {"arquivo": "seu_arquivo.zip"}
        }
    })


if __name__ == '__main__':
    app.run(debug=True)
