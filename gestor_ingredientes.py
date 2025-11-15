import requests
import json
from ingredientes import Pan, Salchicha, Acompañante, Salsa, Topping
import pickle
from hotdogs import HotDog
from gestor_menu import cargar_datos_menu, guardar_datos_menu

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
                    cont_ing += 1
                    ingredientes[cont_ing] = nuevo_ingrediente
                    
            
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
        with open(archivo, 'rb') as a:
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



def listar_productos_categoria():

    print("1. Pan, 2. Salchicha, 3. Acompañante, 4. Salsa, 5. Toppings")
    num = input()
    for cat in ingredientes[0].values():
        if num == "1":
            if cat.get_categoria() == "Pan":
                print(cat.__str__())
        elif num == "2":
            if cat.get_categoria() == "Salchicha":
                print(cat.__str__())
        elif num == "3":
            if cat.get_categoria() == "Acompañante":
                print(cat.__str__())
        elif num == "4":
            if cat.get_categoria() == "Salsa":
                print(cat.__str__())
        elif num == "5":
            if cat.get_categoria() == "toppings":
                print(cat.__str__())


def listar_productos_categoria_tipo():
    print("1. Pan, 2. Salchicha, 3. Acompañante, 4. Salsa, 5. Toppings")
    num = input()
    if num == "1":
        for cat in ingredientes[0].values():
            if cat.get_categoria() == "Pan":
                obtener = input(f"Desea obtener la información de: {cat.get_nombre()}? s/n: ")
                if obtener == "s":
                    print(cat.__str__())
                    return
    elif num == "2":
        for cat in ingredientes[0].values():
            if cat.get_categoria() == "Salchicha":
                obtener = input(f"Desea obtener la información de: {cat.get_nombre()}? (s/n)")
                if obtener == "s":
                    print(cat.__str__())
                    return
    elif num == "3":
        for cat in ingredientes[0].values():
            if cat.get_categoria() == "Acompañante":
                obtener = input(f"Desea obtener la información de: {cat.get_nombre()}? (s/n)")
                if obtener == "s":
                    print(cat.__str__())
                    return
    elif num == "4":
        for cat in ingredientes[0].values():
            if cat.get_categoria() == "Salsa":
                obtener = input(f"Desea obtener la información de: {cat.get_nombre()}? (s/n)")
                if obtener == "s":
                    print(cat.__str__())
                    return
    elif num == "5":
        for cat in ingredientes[0].values():
            if cat.get_categoria() == "toppings":
                obtener = input(f"Desea obtener la información de: {cat.get_nombre()}? (s/n)")
                if obtener == "s":
                    print(cat.__str__())
                    return


def agregar_ingrediente():
    """Agrega un nuevo ingrediente al diccionario en memoria y guarda."""
    
    if not ingredientes:
        print("Error: No hay datos de ingredientes cargados.")
        return
        
    dict_ingredientes = ingredientes[0] 

    print("Seleccione la categoría del ingrediente a agregar:")
    print("1. Pan")
    print("2. Salchicha")
    print("3. Acompañante")
    print("4. Salsa")
    print("5. Topping")
    num = input("--> ")

    # Generar una nueva ID única
    try:
        nueva_llave = max(int(k) for k in dict_ingredientes.keys()) + 1
    except ValueError:
        nueva_llave = 1 # Si el diccionario estaba vacío

    nuevo_ingrediente = None

    if num == "1":
        categoria = "Pan"
        nombre = input("Indique el nombre del pan: ")
        tipo = input("Indique el tipo de pan (ej: Brioche, Integral): ")
        try:
            tamaño = int(input("Indique el tamaño en números (ej: 15): "))
        except ValueError:
            print("Error: El tamaño debe ser un número.")
            return
        unidad = input("Indique la unidad de medida (ej: cm): ")
        nuevo_ingrediente = Pan(categoria, nombre, tipo, tamaño, unidad)

    elif num == "2":
        categoria = "Salchicha"
        nombre = input("Indique el nombre de la salchicha: ")
        tipo = input("Indique el tipo de salchicha (ej: Polaca, Alemana): ")
        try:
            tamaño = int(input("Indique el tamaño en números (ej: 15): "))
        except ValueError:
            print("Error: El tamaño debe ser un número.")
            return
        unidad = input("Indique la unidad de medida (ej: cm): ")
        nuevo_ingrediente = Salchicha(categoria, nombre, tipo, tamaño, unidad)

    elif num == "3":
        categoria = "Acompañante"
        nombre = input("Indique el nombre del acompañante (ej: Papas Fritas): ")
        tipo = input("Indique el tipo (ej: Bastón): ")
        try:
            tamaño = int(input("Indique el tamaño/cantidad (ej: 100): "))
        except ValueError:
            print("Error: El tamaño/cantidad debe ser un número.")
            return
        unidad = input("Indique la unidad de medida (ej: gr): ")
        nuevo_ingrediente = Acompañante(categoria, nombre, tipo, tamaño, unidad)
    
    elif num == "4":
        categoria = "Salsa"
        nombre = input("Indique el nombre de la salsa (ej: Salsa de Tomate): ")
        base = input("Indique la base (ej: Tomate, Mayonesa): ")
        color = input("Indique el color (ej: Roja, Blanca): ")
        nuevo_ingrediente = Salsa(categoria, nombre, base, color)

    elif num == "5":
        categoria = "Topping"
        nombre = input("Indique el nombre del topping (ej: Cebolla Caramelizada): ")
        tipo = input("Indique el tipo (ej: Vegetal, Lácteo): ")
        presentacion = input("Indique la presentación (ej: Picada, Rallada): ")
        nuevo_ingrediente = Topping(categoria, nombre, tipo, presentacion)
    
    else:
        print("Opción no válida. No se agregó ningún ingrediente.")
        return

    if nuevo_ingrediente:
        # Asignación al diccionario
        dict_ingredientes[nueva_llave] = nuevo_ingrediente
        
        # Guardar los cambios en el archivo
        guardar_datos_inventario(ingredientes, "inventario.json")
        print(f"¡Ingrediente '{nombre}' agregado exitosamente con ID {nueva_llave}!")
        print(nuevo_ingrediente)
    else:
        print("No se pudo crear el ingrediente.")



def eliminar_ingrediente():
    """
    Elimina un ingrediente del diccionario en memoria y guarda.
    Valida si el ingrediente está en uso en el menú de hotdogs
    y pide confirmación para eliminar los hotdogs afectados.
    """
    
    if not ingredientes:
        print("Error: No hay datos de ingredientes cargados.")
        return
        
    dict_ingredientes = ingredientes[0] 

    print("Seleccione la categoría del ingrediente a eliminar:")
    print("1. Pan")
    print("2. Salchicha")
    print("3. Acompañante")
    print("4. Salsa")
    print("5. Topping")
    num = input("--> ")

    # Mapeo para evitar código repetido
    # (Corregí "toppings" a "Topping" para que coincida con tu clase)
    categoria_map = {
        "1": "Pan", 
        "2": "Salchicha", 
        "3": "Acompañante", 
        "4": "Salsa", 
        "5": "Topping"
    }

    if num not in categoria_map:
        print("Opción no válida.")
        return

    categoria_str = categoria_map[num]
    
    # Listar solo los de esa categoría
    print(f"\n--- Ingredientes en '{categoria_str}' ---")
    encontrados = False
    for ing in dict_ingredientes.values():
        if ing.get_categoria() == categoria_str:
            print(ing) # Usa el __str__ de la clase
            encontrados = True
    
    if not encontrados:
        print(f"No hay ingredientes registrados en la categoría '{categoria_str}'.")
        return

    opcion = input(f"\nIndique el nombre exacto del {categoria_str} a eliminar: ")

    #Encontrar la llave y el objeto del ingrediente
    llave_a_eliminar = None
    ingrediente_a_eliminar = None
    
    for llave, ingrediente in dict_ingredientes.items():
        print(ingrediente.get_nombre)
        print(ingrediente)
        # (Esto asume que ya corregiste get_nombre() en ingredientes.py)
        if ingrediente.get_nombre() == opcion and ingrediente.get_categoria() == categoria_str:
            llave_a_eliminar = llave
            ingrediente_a_eliminar = ingrediente
            
            break # Encontramos el ingrediente
    
    if not ingrediente_a_eliminar:
        print(f"No se encontró un ingrediente con el nombre '{opcion}' en esta categoría.")
        return

    # 3. REQUISITO PDF: Validar contra el menú 
    print(f"Validando si '{opcion}' está en uso en el menú...")
    menu_data = cargar_datos_menu() # Carga el menú actual
    hotdogs_afectados = []

    if menu_data:
        dict_menu = menu_data[0] # Asumiendo la estructura [ { "nombre": HotDog_obj, ... } ]
        for nombre_hotdog, hotdog_obj in dict_menu.items():
            # Usamos el método de la clase HotDog para ver sus ingredientes
            requerimientos = hotdog_obj.obtener_requerimientos()
            if opcion in requerimientos:
                hotdogs_afectados.append(nombre_hotdog)

    # 4. Lógica de confirmación y borrado
    confirmado = False
    if hotdogs_afectados:
        print("="*30)
        print("  ADVERTENCIA  ")
        print(f"El ingrediente '{opcion}' es usado por los siguientes Hot Dogs:")
        for hd in hotdogs_afectados:
            print(f"  - {hd}")
        print("Si elimina el ingrediente, estos Hot Dogs también serán ELIMINADOS del menú.")
        
        confirm = input("¿Desea continuar? (s/n): ")
        if confirm.lower() == 's':
            # Eliminar los Hot Dogs afectados
            dict_menu_actualizado = menu_data[0]
            for nombre_hd in hotdogs_afectados:
                dict_menu_actualizado.pop(nombre_hd, None) # Borra el hotdog del dict
            
            guardar_datos_menu(menu_data) # Guarda el menú modificado
            print(f"Hot Dogs afectados eliminados del menú.")
            confirmado = True
        else:
            print("Operación cancelada. No se eliminó nada.")
            return # Salir de la función
    else:
        # No está en uso, se puede borrar directamente
        confirmado = True

    #Eliminar el ingrediente (si se confirmó o si no había conflictos)
    if confirmado:
        dict_ingredientes.pop(llave_a_eliminar)
        guardar_datos_inventario(ingredientes, "inventario.json")
        print(f"✅ ¡Ingrediente '{opcion}' eliminado exitosamente!")

listar_productos_categoria()

""" def eliminar_ingrediente():
    """
#Elimina un ingrediente en el diccionario en memoria y guarda.
"""
    
    if not ingredientes:
        print("Error: No hay datos de ingredientes cargados.")
        return
        
    dict_ingredientes = ingredientes[0] 

    print("Seleccione la categoría del ingrediente a eliminar:")
    print("1. Pan")
    print("2. Salchicha")
    print("3. Acompañante")
    print("4. Salsa")
    print("5. Topping")
    num = input("--> ")

    '''# Generar una nueva ID única
    try:
        nueva_llave = max(int(k) for k in dict_ingredientes.keys()) + 1
    except ValueError:
        nueva_llave = 1 # Si el diccionario estaba vacío '''

    ingrediente_a_eliminar = None

    if num == "1":
        for cat in dict_ingredientes.values():
            if cat.get_categoria() == "Pan":
                print(cat.__str__())
        opcion = input("Indique el nombre del pan a eliminar: ")
        for cat in dict_ingredientes.values():
            print(cat.get_nombre)
            if cat.get_nombre() == opcion:
                print(cat)
                ingrediente_a_eliminar = cat

    elif num == "2":
        for cat in dict_ingredientes.values():
            if cat.get_categoria() == "Salchicha":
                print(cat.__str__())
        opcion = input("Indique el nombre de la salchicha a eliminar: ")
        for cat in dict_ingredientes.values():
            if cat.get_nombre() == opcion:
                print(cat)
                ingrediente_a_eliminar = cat

    elif num == "3":
        for cat in dict_ingredientes.values():
            if cat.get_categoria() == "Acompañante":
                print(cat.__str__())
        opcion = input("Indique el nombre del acompañante a eliminar: ")
        for cat in dict_ingredientes.values():
            if cat.get_nombre() == opcion:
                print(cat)
                ingrediente_a_eliminar = cat
    
    elif num == "4":
        for cat in dict_ingredientes.values():
            if cat.get_categoria() == "Salsa":
                print(cat.__str__())
        opcion = input("Indique el nombre de la salsa a eliminar: ")
        for cat in dict_ingredientes.values():
            if cat.get_nombre() == opcion:
                print(cat)
                ingrediente_a_eliminar = cat

    elif num == "5":
        for cat in dict_ingredientes.values():
            if cat.get_categoria() == "toppings":
                print(cat.__str__())
        opcion = input("Indique el nombre del topping a eliminar: ")
        for cat in dict_ingredientes.values():
            if cat.get_nombre() == opcion:
                print(cat)
                ingrediente_a_eliminar = cat
    
    else:
        print("Opción no válida. No se agregó ningún ingrediente.")
        return

    if ingrediente_a_eliminar != None:
        # Asignación al diccionario
        dict_ingredientes.pop(cat)
        
        # Guardar los cambios en el archivo
        guardar_datos_inventario(ingredientes, "inventario.json")
        print(f"¡Ingrediente '{nombre}' eliminado exitosamente!")
    else:
        print("No se pudo crear el ingrediente.")

eliminar_ingrediente() """