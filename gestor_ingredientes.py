import requests
import json
from ingredientes import Pan, Salchicha, Acompañante, Salsa, Topping
import pickle

# ----------------------------------------------------------------------
# 2. Modulo de Gestión de Ingredientes (Módulos)
# ----------------------------------------------------------------------

"""Módulo para la administración de ingredientes (Módulo 1)."""


def obtener_datos_inventario():
    """Descarga y carga los datos iniciales de la API de GitHub."""
    ingredientes_maestros = {}

    api_ingredientes = "https://raw.githubusercontent.com/FernandoSapient/BPTSP05_2526-1/69230a26300dd14e74d4afa599bfc33cfeab085b/ingredientes.json"
    response = requests.get(api_ingredientes)

    try:
        if response.status_code == 200:
            datos = response.json()
            ingredientes = {}
            cont_ing = 0
            for i in datos:
                for j in i["Opciones"]:
                    if i["Categoria"] == "Pan":
                        nuevo_ingrediente = Pan(i["Categoria"], j["nombre"], j["tipo"], j["tamaño"], j["unidad"])
                    elif i["Categoria"] == "Salchicha":
                        nuevo_ingrediente = Salchicha(i["Categoria"], j["nombre"], j["tipo"], j["tamaño"], j["unidad"])
                    elif i["Categoria"] == "Acompañante":
                        nuevo_ingrediente = Acompañante(i["Categoria"], j["nombre"], j["tipo"], j["tamaño"], j["unidad"])
                    elif i["Categoria"] == "Salsa":
                        nuevo_ingrediente = Salsa(i["Categoria"], j["nombre"], j["base"], j["color"])
                    else:
                        nuevo_ingrediente = Topping(i["Categoria"], j["nombre"], j['tipo'], j["presentación"])
                    ingredientes["Ing"] = nuevo_ingrediente
                    cont_ing += 1
            
            print(f"{cont_ing} ingredientes cargados desde la API.")
            return ingredientes
        else:
            print(f"Error al conectar con la API. Código de estado: {response.status_code}")
        
    except requests.exceptions.ConnectionError:
        print("Error de conexión: No se pudo acceder a la URL de GitHub.")
        return None
    except json.JSONDecodeError:
        print("Error de formato: El contenido de la URL no es un JSON válido.")
        return None

    
def cargar_datos_inventario(archivo="inventario.json"):
    """Carga los ingredientes agregados por el usuario desde el JSON local."""
    try:
        with open(archivo, 'rb', encoding='utf-8') as a:
            return pickle.load(a)
    except Exception as e:
        return []


def guardar_datos_inventario(ingredientes, archivo="inventario.json"):
    """Guarda los ingredientes agregados localmente en un archivo JSON."""
    try:
        with open(archivo, "wb") as a:
            return pickle.dump(ingredientes, a)
    except Exception as e:
        print(f"Error al guardar datos locales: {e}")
        return None

ingredientes = cargar_datos_inventario()

if not ingredientes:
    print("No se encontraron ingredientes cargados. Consultando a la API...")

    ing = obtener_datos_inventario()
    if ing:
        ingredientes.append(ing)
        guardar_datos_inventario(ingredientes)






""" def get_ingredientes_maestros(self):
    """
    #Retorna el diccionario maestro de ingredientes.
"""
    return self._ingredientes_maestros
def ver_lista_maestra_simple(self):
    """
    #Muestra una lista simple de todos los ingredientes maestros.
"""
    print("\n--- Lista Maestra de Ingredientes ---")
    if not self._ingredientes_maestros:
        print("La lista maestra está vacía.")
        return
    for nombre, ing in self._ingredientes_maestros.items():
        print(f"- {nombre} ({ing._categoria}, {ing._tamaño}{ing._unidad})")


def eliminar_ingrediente(self, nombre, gestor_menu, gestor_inventario):
    """
    # pidiendo confirmación para eliminar los Hot Dogs asociados.
"""
    if nombre not in self._ingredientes_maestros:
        print(f"❌ Error: El ingrediente '{nombre}' no existe en la lista maestra.")
        return
    # 1. Verificar uso en el menú
    hotdogs_afectados = []
    menu = gestor_menu.get_menu()
    
    for hd_nombre, hotdog in menu.items():
        requerimientos = hotdog.obtener_requerimientos()
        if nombre in requerimientos:
            hotdogs_afectados.append(hd_nombre)
    # 2. Manejo de la Eliminación
    if hotdogs_afectados:
        print("\n⚠️ Advertencia Crítica: Uso del Ingrediente")
        print(f"El ingrediente '{nombre}' está siendo usado por los siguientes Hot Dogs:")
        for hd in hotdogs_afectados:
            print(f"  - {hd}")
        
        print("\nSi elimina este ingrediente, los Hot Dogs listados arriba serán eliminados del menú.")
        respuesta = input("¿Desea proceder con la eliminación? (S/N): ").strip().upper()
        
        if respuesta != 'S':
            print(f"🚫 Eliminación de '{nombre}' cancelada por el usuario.")
            return
        # Si el usuario confirma, procedemos a eliminar los Hot Dogs
        for hd_a_eliminar in hotdogs_afectados:
            gestor_menu.eliminar_hotdog(hd_a_eliminar, gestor_inventario=gestor_inventario) 
    # Eliminar el ingrediente de la lista maestra
    del self._ingredientes_maestros[nombre]
    self.guardar_datos_locales() 
    print(f"✅ Ingrediente '{nombre}' eliminado correctamente.")"""

