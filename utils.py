# ----------------------------------------------------------------------
# Módulo de Utilidades
# ----------------------------------------------------------------------

import requests
import json
import os
from ingredientes import *

def validar_input_numerico(prompt, tipo_dato=int, rango=None):
    """
    Valida que la entrada del usuario sea un número (int o float)
    y, opcionalmente, que esté en un rango [min, max].
    """
    while True:
        try:
            valor_str = input(prompt)
            valor_num = tipo_dato(valor_str)
            
            if rango:
                if not (rango[0] <= valor_num <= rango[1]):
                    print(f"Error: El valor debe estar entre {rango[0]} y {rango[1]}.")
                    continue
            return valor_num
        except ValueError:
            print(f"Error: Debe ingresar un número válido.")
        except Exception as e:
            print(f"Error inesperado: {e}")


def validar_confirmacion(prompt):
    """Pide una confirmación (S/N) al usuario."""
    while True:
        resp = input(prompt + " (S/N): ").strip().upper()
        if resp == 'S':
            return True
        if resp == 'N':
            return False
        print("Respuesta no válida. Por favor, ingrese S o N.")


def descargar_datos_api(url_ingredientes, url_menu):
    """
    Descarga los JSON de ingredientes y menú de la API de GitHub.
    Retorna diccionarios con los datos o None si falla.
    """
    print("Descargando datos desde la API de GitHub...")


    def fetch_json(url):
        """Función auxiliar para descargar y parsear un JSON."""
        try:
            response = requests.get(url, timeout=10) 
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"\n--- ERROR HTTP al descargar {url} ---")
            print(f"Código de error: {e.response.status_code}")
            return None
        except requests.exceptions.ConnectionError as e:
            print(f"\n--- Error de Conexión al descargar {url} ---")
            print("Diagnóstico: No se pudo conectar a GitHub.")
            return None
        except requests.exceptions.Timeout:
            print(f"\n--- Error de Timeout al descargar {url} ---")
            return None
        except json.JSONDecodeError as e:
            print(f"\n--- Error al decodificar JSON de {url} ---")
            print(f"Error: {e}")
            print(f"Contenido (primeros 100 caracteres): {response.text[:100]}...")
            return None
    ingredientes_api = fetch_json(url_ingredientes)
    menu_api = fetch_json(url_menu)
    if not all([ingredientes_api, menu_api]):
        print("\nError fatal: No se pudieron descargar todos los datos base de la API.")
        return None, None
    print("Datos de la API (Ingredientes y Menú) descargados exitosamente.")
    return ingredientes_api, menu_api


def cargar_datos_locales(archivo_local):
    """Carga los datos del archivo JSON local si existe."""
    if not os.path.exists(archivo_local):
        print(f"No se encontró el archivo local '{archivo_local}'. Se creará uno nuevo al salir.")
        return {
            "nuevos_ingredientes": [], 
            "nuevos_hotdogs": [], 
            "inventario": None, 
            "estadisticas": [],
            "api_ingredientes_eliminados": [],
            "api_hotdogs_eliminados": []
        }
    try:
        with open(archivo_local, 'r', encoding='utf-8') as f:
            datos = json.load(f)
            print(f"Datos locales de '{archivo_local}' cargados.")
            datos.setdefault("nuevos_ingredientes", [])
            datos.setdefault("nuevos_hotdogs", [])
            datos.setdefault("inventario", None)
            datos.setdefault("estadisticas", [])
            datos.setdefault("api_ingredientes_eliminados", [])
            datos.setdefault("api_hotdogs_eliminados", [])
            return datos
    except Exception as e:
        print(f"Error al cargar '{archivo_local}': {e}. Se usarán datos vacíos.")
        return {
            "nuevos_ingredientes": [], 
            "nuevos_hotdogs": [], 
            "inventario": None, 
            "estadisticas": [],
            "api_ingredientes_eliminados": [],
            "api_hotdogs_eliminados": []
        }


def guardar_datos_locales(datos_a_guardar, archivo_local):
    """Guarda el estado actual (nuevos items, inventario) en el JSON local."""
    try:
        with open(archivo_local, 'w', encoding='utf-8') as f:
            json.dump(datos_a_guardar, f, indent=4)
        print(f"Datos guardados exitosamente en '{archivo_local}'.")
    except Exception as e:
        print(f"Error al guardar datos locales: {e}")


def crear_ingrediente_desde_dict(data):
    """
    Patrón Factory: Crea un objeto Ingrediente (Pan, Salchicha, etc.)
    a partir de un diccionario.
    """
    try:
        tipo_clase = data.get("clase", data.get("categoria"))
        
        if tipo_clase is None:
            print(f"Error al crear ingrediente (JSON): Datos vacíos o sin categoría. Datos: {str(data)[:50]}")
            return None
        if tipo_clase == "Pan":
            return Pan(data['categoria'], data['nombre'], data['tipo'], data['tamaño'], data['unidad'])
        elif tipo_clase == "Salchicha":
            return Salchicha(data['categoria'], data['nombre'], data['tipo'], data['tamaño'], data['unidad'])
        elif tipo_clase == "Acompañante":
            return Acompañante(data['categoria'], data['nombre'], data['tipo'], data['tamaño'], data['unidad'])
        elif tipo_clase == "Salsa":
            return Salsa(data['categoria'], data['nombre'], data['base'], data['color'])
        elif tipo_clase == "Topping":
            return Topping(data['categoria'], data['nombre'], data['tipo'], data['presentación'])
        else:
            print(f"Error al crear ingrediente (JSON): Categoría '{tipo_clase}' desconocida.")
            return None
    except KeyError as e:
        print(f"Error al crear ingrediente '{data.get('nombre', '???')}' (JSON): Datos incompletos. Falta la llave {e}.")
        return None


def validar_input_texto(prompt):
    """Valida que la entrada de texto del usuario no esté vacía."""
    while True:
        try:
            texto = input(prompt).strip()
            if not texto:
                print("Error: La entrada no puede estar vacía.")
                continue
            return texto
        except EOFError:
            print("Entrada cancelada.")
            return None

