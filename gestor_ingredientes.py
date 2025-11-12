import requests
import json
from clasesperrosprueba import Ingrediente

# ----------------------------------------------------------------------
# 2. Modulo de Gestión de Ingredientes (Módulos)
# ----------------------------------------------------------------------

"""Módulo para la administración de ingredientes (Módulo 1)."""


def cargar_datos_api(self):
    """Descarga y carga los datos iniciales de la API de GitHub."""
    print("Cargando datos de la API de GitHub...")
    ingredientes_maestros = {}
    datos_locales_ruta = "datos_locales_ingredientes.json"
    API_URL = "https://raw.githubusercontent.com/FernandoSapient/BPTSP05_2526-1/refs/heads/main/ingredientes.json"
    try:
        response = requests.get(API_URL)

        if response.status_code == 200:
            datos_json = response.json()
            
            for nombre, data in datos_json.items():
                nuevo_ingrediente = Ingrediente(
                    nombre=nombre,
                    categoria=data.get("categoria", "Desconocida"),
                    tipo=data.get("tipo", "General"),
                    tamaño=data.get("longitud", 0.0), 
                    unidad=data.get("unidad", "u"),
                    id_data={"source": "API"}
                )
                    self._ingredientes_maestros[nombre] = nuevo_ingrediente
                
                print(f"✅ {len(self._ingredientes_maestros)} ingredientes cargados desde la API.")
            else:
                print(f"❌ Error al conectar con la API. Código de estado: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Error de conexión: No se pudo acceder a la URL de GitHub.")
        except json.JSONDecodeError:
            print("❌ Error de formato: El contenido de la URL no es un JSON válido.")
        
    def cargar_datos_locales(self):
        """Carga los ingredientes agregados por el usuario desde el JSON local."""
        try:
            with open(self._datos_locales_ruta, 'r', encoding='utf-8') as f:
                datos = json.load(f)
                
                for data in datos:
                    nombre = data['nombre']
                    # Evitar duplicados si un ingrediente API fue grabado localmente sin querer
                    if nombre in self._ingredientes_maestros:
                        continue 
                    nuevo_ingrediente = Ingrediente(
                        nombre=nombre,
                        categoria=data.get("categoria", "Desconocida"),
                        tipo=data.get("tipo", "General"),
                        tamaño=data.get("tamaño", 0.0), 
                        unidad=data.get("unidad", "u"),
                        id_data={"source": "Local"}
                    )
                    self._ingredientes_maestros[nombre] = nuevo_ingrediente
                    
                print(f"✅ {len(datos)} ingredientes locales cargados desde {self._datos_locales_ruta}.")
                
        except FileNotFoundError:
            print("ℹ️ No se encontró archivo de datos locales. Iniciando solo con datos de API.")
        except json.JSONDecodeError:
            print("❌ Error al decodificar el archivo JSON local.")

    def guardar_datos_locales(self):
        """Guarda los ingredientes agregados localmente en un archivo JSON."""
        datos_a_guardar = [ing.to_dict() for ing in self._ingredientes_maestros.values()]
        
        try:
            with open(self._datos_locales_ruta, 'w', encoding='utf-8') as f:
                json.dump(datos_a_guardar, f, indent=4)
            print(f"✅ Datos de ingredientes locales guardados en {self._datos_locales_ruta}")
        except Exception as e:
            print(f"❌ Error al guardar datos locales: {e}")

    def get_ingredientes_maestros(self):
        """Retorna el diccionario maestro de ingredientes."""
        return self._ingredientes_maestros

    def ver_lista_maestra_simple(self):
        """Muestra una lista simple de todos los ingredientes maestros."""
        print("\n--- Lista Maestra de Ingredientes ---")
        if not self._ingredientes_maestros:
            print("La lista maestra está vacía.")
            return

        for nombre, ing in self._ingredientes_maestros.items():
            print(f"- {nombre} ({ing._categoria}, {ing._tamaño}{ing._unidad})")


    def eliminar_ingrediente(self, nombre, gestor_menu, gestor_inventario):
        """
        Elimina un ingrediente, validando si es usado por un HotDog del menú y 
        pidiendo confirmación para eliminar los Hot Dogs asociados.
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
        print(f"✅ Ingrediente '{nombre}' eliminado correctamente.")
