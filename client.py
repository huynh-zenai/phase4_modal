import requests, base64, pathlib
url = "https://txt2img-sd15--inference-web.modal.run/"
resp = requests.post(url, json={"prompt": "studio photo of an ancient dragon"})
pathlib.Path("dragon.png").write_bytes(base64.b64decode(resp.json()["data"]))