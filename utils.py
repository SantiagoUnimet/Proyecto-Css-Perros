# ----------------------------------------------------------------------
# Módulo de Utilidades
# ----------------------------------------------------------------------
import requests
import json
import os
from ingredientes import * # Importamos todas las clases de ingredientes

# URLs de la API de GitHub (¡Corregidas!)
URL_INGREDIENTES = "https://raw.githubusercontent.com/FernandoSapient/BPTSP05_2526-1/refs/heads/main/ingredientes.json"
URL_MENU = "https://raw.githubusercontent.com/FernandoSapient/BPTSP05_2526-1/refs/heads/main/menu.json"

# Archivo local
ARCHIVO_LOCAL = "hotdog_ccs_local.json"

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

def descargar_datos_api():
    """
    Descarga los JSON de ingredientes y menú de la API de GitHub.
    Retorna diccionarios con los datos o None si falla.
    """
    print("Descargando datos desde la API de GitHub...")
    
    def fetch_json(url):
        """Función auxiliar para descargar y parsear un JSON."""
        try:
            response = requests.get(url, timeout=10) 
            response.raise_for_status() # Lanza error si es 404, 500, etc.
            return response.json()

        except requests.exceptions.HTTPError as e:
            print(f"\n--- ERROR HTTP al descargar {url} ---")
            print(f"Código de error: {e.response.status_code}")
            if e.response.status_code == 404:
                print("Diagnóstico: ERROR 404: Archivo no encontrado.")
            return None
        except requests.exceptions.ConnectionError as e:
            print(f"\n--- Error de Conexión al descargar {url} ---")
            print("Diagnóstico: No se pudo conectar a GitHub.")
            print("Verifica tu conexión a internet o firewall.")
            return None
        except requests.exceptions.Timeout:
            print(f"\n--- Error de Timeout al descargar {url} ---")
            return None
        except json.JSONDecodeError as e:
            print(f"\n--- Error al decodificar JSON de {url} ---")
            print(f"Error: {e}")
            print(f"Contenido (primeros 100 caracteres): {response.text[:100]}...")
            return None

    # --- Fin de la función auxiliar ---

    ingredientes_api = fetch_json(URL_INGREDIENTES)
    menu_api = fetch_json(URL_MENU)

    # Si alguno falló, no podemos continuar
    if not all([ingredientes_api, menu_api]):
        print("\nError fatal: No se pudieron descargar todos los datos base de la API.")
        return None, None

    print("Datos de la API (Ingredientes y Menú) descargados exitosamente.")
    return ingredientes_api, menu_api

def cargar_datos_locales():
    """Carga los datos del archivo JSON local si existe."""
    if not os.path.exists(ARCHIVO_LOCAL):
        print(f"No se encontró el archivo local '{ARCHIVO_LOCAL}'. Se creará uno nuevo al salir.")
        # El inventario ahora inicia en None (o vacío)
        return {"nuevos_ingredientes": [], "nuevos_hotdogs": [], "inventario": None, "estadisticas": []}
    
    try:
        with open(ARCHIVO_LOCAL, 'r', encoding='utf-8') as f:
            datos = json.load(f)
            print(f"Datos locales de '{ARCHIVO_LOCAL}' cargados.")
            # Asegurarse que las llaves principales existan
            datos.setdefault("nuevos_ingredientes", [])
            datos.setdefault("nuevos_hotdogs", [])
            datos.setdefault("inventario", None) # El inventario se carga desde aquí
            datos.setdefault("estadisticas", [])
            return datos
    except Exception as e:
        print(f"Error al cargar '{ARCHIVO_LOCAL}': {e}. Se usarán datos vacíos.")
        return {"nuevos_ingredientes": [], "nuevos_hotdogs": [], "inventario": None, "estadisticas": []}

def guardar_datos_locales(datos_a_guardar):
    """Guarda el estado actual (nuevos items, inventario) en el JSON local."""
    try:
        with open(ARCHIVO_LOCAL, 'w', encoding='utf-8') as f:
            json.dump(datos_a_guardar, f, indent=4)
        print(f"Datos guardados exitosamente en '{ARCHIVO_LOCAL}'.")
    except Exception as e:
        print(f"Error al guardar datos locales: {e}")

# --- Fábrica (Factory) para crear objetos ---

def crear_ingrediente_desde_dict(data):
    """
    Patrón Factory: Crea un objeto Ingrediente (Pan, Salchicha, etc.)
    a partir de un diccionario.
    """
    try:
        # 'categoria' ahora es agregada por GestorIngredientes
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
            # --- ¡CORRECCIÓN CLAVE! ---
            # La API usa "presentación" con acento
            return Topping(data['categoria'], data['nombre'], data['tipo'], data['presentación'])
        else:
            print(f"Error al crear ingrediente (JSON): Categoría '{tipo_clase}' desconocida.")
            return None
    
    except KeyError as e:
        # Esto captura si falta 'nombre', 'tipo', 'tamaño', 'presentación', etc.
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
