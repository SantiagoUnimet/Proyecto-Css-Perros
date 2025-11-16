from hotdogs import HotDog
import json
import requests
import pickle
from gestor_inventario import *

# Métodos de Persistencia

def obtener_datos_menu():
    """Descarga y carga los datos iniciales de la API de GitHub."""
    
    api_menu = "https://raw.githubusercontent.com/FernandoSapient/BPTSP05_2526-1/refs/heads/main/menu.json"
    response = requests.get(api_menu)
    menu = {}

    try:
        if response.status_code == 200:
            datos = response.json()
            menu = {}
            cont_menu = 0
            for i in datos:
                for j in i:
                    if j == "Salsas":
                        nuevo_hotdog = HotDog(i["nombre"], i["Pan"], i["Salchicha"], i["toppings"], i[j], i["Acompañante"])
                    elif j == "salsas":
                        nuevo_hotdog = HotDog(i["nombre"], i["Pan"], i["Salchicha"], i["toppings"], i[j], i["Acompañante"])
                
                # CORRECCIÓN VITAL: Se usa el nombre del HotDog (i["nombre"]) como clave.
                menu[i["nombre"]] = nuevo_hotdog
                
                cont_menu += 1
            print(f"{cont_menu} combos cargados desde la API.")
            return menu
        
    except requests.exceptions.ConnectionError:
        print("Error de conexión: No se pudo acceder a la URL de GitHub.")
        return None
    except json.JSONDecodeError:
        print("Error de formato: El contenido de la URL no es un JSON válido.")
        return None

    
def cargar_datos_menu(archivo="menú.json"):
    """Carga los hotdogs agregados por el usuario desde el JSON local."""
    try:
        with open(archivo, 'rb') as a:
            return pickle.load(a)
    except Exception as e:
        return []


def guardar_datos_menu(menu, archivo="menú.json"):
    """Guarda los Hot Dogs locales en un archivo JSON."""
    try:
        with open(archivo, 'wb') as a:
            pickle.dump(menu, a)
    except Exception as e:
        print(f"Error al guardar el menú: {e}")
        return None
    
menu = cargar_datos_menu()

if not menu:
    print("No se encontró un menú cargado. Consultando a la API...")

    combo = obtener_datos_menu()
    print(combo)
    if combo:
        menu.append(combo)
        guardar_datos_menu(menu)




# Métodos de Gestión
def ver_lista_hotdogs(menu): 
#Muestra la lista de Hot Dogs actualmente en el menú.

    print("\n--- Menú Actual de Hot Dogs ---")
    if not menu:
        print("El menú está vacío.")
        return
        
    # Accede al diccionario de HotDogs en el índice 0 de la lista 'menu'.
    if isinstance(menu, list) and len(menu) > 0 and isinstance(menu[0], dict):
        hotdogs_dict = menu[0]
        # Itera sobre las CLAVES (los nombres de los HotDogs) del diccionario.
        for nombre in hotdogs_dict.keys():
            print(f"- {nombre}")


def agregar_hotdog_interactivo(menu_dict, guardar_func,):
    """
    Solicita datos al usuario, crea el objeto HotDog y lo añade al menú,
    validando la existencia y la longitud de pan/salchicha usando el diccionario de ingredientes.
    """
    print("\n--- CREACIÓN Y ADICIÓN DE NUEVO HOT DOG ---")
    
    # 1. Recolección de Datos (Input)
    nombre = input("▶️ Ingrese el Nombre del Hot Dog: ").strip()
    # Convertimos a minúsculas para buscar en el diccionario
    pan = input("▶️ Ingrese el Pan (ej: simple, especial): ").strip().lower()
    salchicha = input("▶️ Ingrese la Salchicha (ej: weiner, alemana): ").strip().lower()
    
    # ... (Recolección de toppings, salsas y acompañante)
    toppings_str = input("▶️ Ingrese los Toppings (separados por coma): ").strip()
    salsas_str = input("▶️ Ingrese las Salsas (separadas por coma): ").strip()
    acompanante = input("▶️ Ingrese el Acompañante: ").strip()
    
    if nombre in menu_dict: 
        print(f"❌ Error: El HotDog '{nombre}' ya existe.")
        return

    # ----------------------------------------------------------------------
    # VALIDACIÓN DE EXISTENCIA Y LONGITUD
    # ----------------------------------------------------------------------
    pan_size = ingredientes_data.get("Pan", {}).get(pan)
    salchicha_size = ingredientes_data.get("Salchicha", {}).get(salchicha)
    
    # 3a. Validar que el Pan esté registrado
    if pan_size is None:
        print(f"❌ Error de ingrediente: El Pan '{pan}' no está registrado en el catálogo.")
        # Aquí debería implementarse la lógica de 'seleccionar otro o cancelar'
        print("🚫 Creación de HotDog cancelada.")
        return
        
    # 3b. Validar que la Salchicha esté registrada
    if salchicha_size is None:
        print(f"❌ Error de ingrediente: La Salchicha '{salchicha}' no está registrada en el catálogo.")
        print("🚫 Creación de HotDog cancelada.")
        return
        
    # 3c. Validar que las longitudes coincidan
    if pan_size != salchicha_size:
        print("\n⚠️ Advertencia de Longitud:")
        print(f"El Pan '{pan}' tiene **{pan_size} pulgadas** y la Salchicha '{salchicha}' tiene **{salchicha_size} pulgadas**. ¡NO COINCIDEN!")
        
        respuesta_confirmacion = input("¿Desea crear este HotDog a pesar de la incompatibilidad? (S/N): ").strip().upper()
        if respuesta_confirmacion != 'S':
            print(f"🚫 Creación de HotDog '{nombre}' cancelada por el usuario.")
            return # Cancela la función
    
    # ----------------------------------------------------------------------

    # 4. Creación del objeto HotDog y Guardado
    toppings = [t.strip() for t in toppings_str.split(',') if t.strip()]
    salsas = [s.strip() for s in salsas_str.split(',') if s.strip()]
    
    nuevo_hotdog = HotDog(nombre, pan, salchicha, toppings, salsas, acompanante)
    
    menu_dict[nombre] = nuevo_hotdog
    guardar_func(menu_dict) 
    print(f"✅ HotDog '{nombre}' agregado al menú y guardado exitosamente.")


def eliminar_hotdog(menu_dict, guardar_func, nombre):
    """
    Elimina un HotDog de un diccionario de menú (Standalone).
    """
    if nombre not in menu_dict:
        print(f"❌ Error: HotDog '{nombre}' no encontrado.")
        return
    
    del menu_dict[nombre]
    guardar_func(menu_dict)
    print(f"✅ HotDog '{nombre}' eliminado del menú.")




print("\n--- LISTADO ANTES DE AGREGAR ---")
ver_lista_hotdogs(menu) 


print("\n--- INICIANDO ADICIÓN INTERACTIVA ---")
agregar_hotdog_interactivo(
    menu_dict=menu[0], 
    guardar_func=guardar_datos_menu
)

print("\n--- LISTADO DESPUÉS DE AGREGAR ---")
ver_lista_hotdogs(menu)
#Creo q ya