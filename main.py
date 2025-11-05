import requests

url = "http://127.0.0.1:5000/api/upload"
headers = {"Authorization": "Bearer seu_token_de_acesso_ftp_123"}
files = {"arquivo": open("teste.txt", "rb")}

res = requests.post(url, headers=headers, files=files)
print(res.json())
