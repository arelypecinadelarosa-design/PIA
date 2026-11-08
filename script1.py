
import requests
import json
import re
import csv

def validar_nombre(nombre):
    patron = r"^[a-z]+(?:-[a-z]+)*$"

    if re.fullmatch(patron, nombre):
        return True
    else:
        return False

def consultar_api(nombre):
    url = "https://pokeapi.co/api/v2/pokemon/" + nombre

    try:
        respuesta = requests.get(url, timeout=10)
        respuesta.raise_for_status()
        datos = respuesta.json()
        print("Conexion exitosa con PokéAPI")
        return datos

    except requests.exceptions.HTTPError:
        print("Error: Pokemon no encontrado.")

    except requests.exceptions.ConnectionError:
        print("Error: No hay conexion a internet.")

    except requests.exceptions.Timeout:
        print("Error: Tiempo de espera agotado.")

    except requests.exceptions.RequestException as error:
        print("Error en la consulta:", error)

    except ValueError:
        print("Error al leer los datos JSON.")

    return None


def organizar_datos(datos):
    pokemon = {
        "nombre": datos["name"],
        "numero": datos["id"],
        "altura": datos["height"],
        "peso": datos["weight"],
        "experiencia": datos["base_experience"],

        "tipos": ", ".join(
            elemento["type"]["name"]
            for elemento in datos["types"]
        ),
        "habilidades": ", ".join(
            elemento["ability"]["name"]
            for elemento in datos["abilities"]
        )
    }
    return pokemon

def guardar_json(lista):
    with open("pokemon.json", "w", encoding="utf-8") as archivo:
        json.dump(lista, archivo, indent=4, ensure_ascii=False)
    print("Archivo JSON guardado correctamente.")

def guardar_csv(lista):
    campos = [
        "nombre",
        "numero",
        "altura",
        "peso",
        "experiencia",
        "tipos",
        "habilidades"
    ]
    with open("pokemon.csv", "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(lista)
    print("Archivo CSV guardado correctamente.")

def guardar_txt(lista):
    with open("pokemon.txt", "w", encoding="utf-8") as archivo:
        for pokemon in lista:
            for clave, valor in pokemon.items():
                archivo.write(clave + ": " + str(valor) + "\n")
            archivo.write("----------------------\n")
    print("Archivo TXT guardado correctamente.")

def main():
    lista_pokemon = []
    print("================================")
    print("       CONSULTA POKEAPI")
    print("================================")
    cantidad = input("Cuantos Pokemon deseas consultar? ")
    if not re.fullmatch(r"[1-9][0-9]*", cantidad):
        print("Error: Ingresa un numero entero positivo.")
        return
    cantidad = int(cantidad)
    for i in range(cantidad):
        print("\nConsulta numero:", i + 1)
        nombre = input("Nombre del Pokemon: ").lower().strip()
        if not validar_nombre(nombre):
            print("Nombre no valido. Intenta nuevamente.")
            continue
        datos = consultar_api(nombre)
        if datos is not None:
            pokemon = organizar_datos(datos)
            lista_pokemon.append(pokemon)
            print("\nDatos obtenidos:")
            print(pokemon)

    if lista_pokemon:
        guardar_json(lista_pokemon)
        guardar_csv(lista_pokemon)
        guardar_txt(lista_pokemon)
        print("\nProceso terminado correctamente.")
    else:
        print("\nNo se obtuvieron datos para guardar.")


















if __name__ == "__main__":

    main()
