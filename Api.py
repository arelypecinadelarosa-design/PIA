import requests
import json

url = "https://pokeapi.co/api/v2/"

respuesta = requests.get(url)

if respuesta.status_code == 200:
    datos = respuesta.json()

    print("Conexion exitosa")
    print(json.dumps(datos, indent=4))
else:
    print("Error al conectar con la API")
