# ----------------------------------------------------------------------
# Módulo 1: Gestión de Ingredientes
# ----------------------------------------------------------------------
import utils
from ingredientes import *

class GestorIngredientes:
    """Administra el registro (alta, baja, consulta) de todos los ingredientes."""
    
    def __init__(self):
        # Un diccionario donde la llave es la categoría (Pan, Salsa...)
        # y el valor es una lista de objetos de esa categoría.
        self._ingredientes_por_categoria = {
            "Pan": [],
            "Salchicha": [],
            "Topping": [],
            "Salsa": [],
            "Acompañante": []
        }
        # Un diccionario para buscar rápidamente un ingrediente por su nombre
        self._ingredientes_por_nombre = {}
        
        # Guarda los ingredientes que vienen de la API para no guardarlos
        # duplicados en el JSON local.
        self._nombres_ingredientes_api = set()

    def cargar_ingredientes_api(self, ingredientes_data_api):
        """Carga los ingredientes base de la API (con estructura anidada)."""
        if not ingredientes_data_api:
            return
            
        # 1. Iteramos la lista de grupos (ej: {Categoria: "Pan", Opciones: [...]})
        for categoria_grupo in ingredientes_data_api:
            try:
                # 2. Obtenemos el nombre de la categoría
                categoria_nombre = categoria_grupo['Categoria']

                # 3. Manejar la 't' minúscula en "toppings"
                if categoria_nombre.lower() == 'toppings':
                    categoria_nombre = 'Topping'
                
                # 4. Capitalizar para que coincida con nuestras clases ("Pan", "Salsa")
                categoria_limpia = categoria_nombre.capitalize()

                # 5. Iteramos la lista interna de "Opciones"
                for ingrediente_data in categoria_grupo['Opciones']:
                    
                    # 6. ¡IMPORTANTE! Agregamos la categoría a los datos
                    #    del ingrediente, ya que no la tienen.
                    ingrediente_data['categoria'] = categoria_limpia
                    
                    # 7. Ahora sí, creamos el ingrediente
                    ingrediente = utils.crear_ingrediente_desde_dict(ingrediente_data)
                    
                    if ingrediente is None:
                        # La fábrica de utils.py ya imprimió el error
                        continue 
                    
                    # 8. Registrar el ingrediente
                    self._ingredientes_por_categoria[ingrediente.get_categoria()].append(ingrediente)
                    self._ingredientes_por_nombre[ingrediente.get_nombre()] = ingrediente
                    self._nombres_ingredientes_api.add(ingrediente.get_nombre())

            except KeyError as e:
                print(f"Error al leer API de ingredientes: falta la llave {e} en el grupo.")
            except Exception as e:
                print(f"Error inesperado al procesar grupo de ingredientes: {e}")
    
    def cargar_ingredientes_locales(self, ingredientes_data_local):
        """Carga los ingredientes creados por el usuario."""
        for data in ingredientes_data_local:
            try:
                ingrediente = utils.crear_ingrediente_desde_dict(data)
                # Evitar duplicados si el local se corrompe
                if ingrediente.get_nombre() not in self._ingredientes_por_nombre:
                    self._ingredientes_por_categoria[ingrediente.get_categoria()].append(ingrediente)
                    self._ingredientes_por_nombre[ingrediente.get_nombre()] = ingrediente
            except Exception as e:
                print(f"Error al cargar ingrediente local '{data.get('nombre')}': {e}")
                
    def get_ingredientes_para_guardar(self):
        """Retorna una lista de diccionarios de los ingredientes NO API."""
        locales = []
        for ingrediente in self._ingredientes_por_nombre.values():
            if ingrediente.get_nombre() not in self._nombres_ingredientes_api:
                locales.append(ingrediente.to_dict())
        return locales

    def buscar_ingrediente(self, nombre):
        """Busca un ingrediente por nombre. Retorna el objeto o None."""
        return self._ingredientes_por_nombre.get(nombre)

    def listar_por_categoria(self, categoria):
        """Módulo 1.1: Listar todos los productos de una categoría."""
        if categoria not in self._ingredientes_por_categoria:
            print(f"Categoría '{categoria}' no existe.")
            return
            
        lista = self._ingredientes_por_categoria.get(categoria, [])
        if not lista:
            print(f"No hay ingredientes registrados en la categoría '{categoria}'.")
            return
            
        print(f"\n--- Ingredientes en '{categoria}' ---")
        for ingrediente in lista:
            print(f"  -> {ingrediente}") # Llama al __str__ de la clase

    def listar_por_tipo(self, categoria, tipo):
        """Módulo 1.2: Listar todos los productos en esa categoría de un tipo."""
        if categoria not in self._ingredientes_por_categoria:
            print(f"Categoría '{categoria}' no existe.")
            return

        lista_filtrada = []
        for ingrediente in self._ingredientes_por_categoria.get(categoria, []):
            # Verificamos si el ingrediente tiene el atributo _tipo
            if hasattr(ingrediente, '_tipo') and ingrediente._tipo.lower() == tipo.lower():
                lista_filtrada.append(ingrediente)
                
        if not lista_filtrada:
            print(f"No se encontraron ingredientes del tipo '{tipo}' en '{categoria}'.")
            return
            
        print(f"\n--- Ingredientes en '{categoria}' (Tipo: {tipo}) ---")
        for ingrediente in lista_filtrada:
            print(f"  -> {ingrediente}")

    def agregar_ingrediente(self, ingrediente_obj):
        """Módulo 1.3: Agrega un nuevo ingrediente al sistema."""
        nombre = ingrediente_obj.get_nombre()
        if nombre in self._ingredientes_por_nombre:
            print(f"Error: Ya existe un ingrediente con el nombre '{nombre}'.")
            return False
            
        categoria = ingrediente_obj.get_categoria()
        self._ingredientes_por_categoria[categoria].append(ingrediente_obj)
        self._ingredientes_por_nombre[nombre] = ingrediente_obj
        print(f"Ingrediente '{nombre}' agregado exitosamente.")
        return True

    def eliminar_ingrediente(self, nombre, gestor_menu):
        """Módulo 1.4: Elimina un ingrediente."""
        ingrediente = self.buscar_ingrediente(nombre)
        if not ingrediente:
            print(f"Error: No se encontró el ingrediente '{nombre}'.")
            return

        # Validar si está en uso [cite: 41]
        hotdogs_afectados = gestor_menu.hotdogs_que_usan_ingrediente(nombre)
        
        if hotdogs_afectados:
            print(f"¡Advertencia! El ingrediente '{nombre}' es usado por los siguientes hot dogs:")
            for hd in hotdogs_afectados:
                print(f"  - {hd.get_nombre()}")
            print("Si lo elimina, estos hot dogs también serán eliminados del menú.")
            
            if not utils.validar_confirmacion("¿Desea continuar con la eliminación?"):
                print("Eliminación cancelada.")
                return

            # Eliminar los hot dogs afectados
            for hd in hotdogs_afectados:
                gestor_menu.eliminar_hotdog_directo(hd.get_nombre())

        # Eliminar el ingrediente
        categoria = ingrediente.get_categoria()
        self._ingredientes_por_categoria[categoria].remove(ingrediente)
        del self._ingredientes_por_nombre[nombre]
        
        print(f"Ingrediente '{nombre}' eliminado exitosamente.")
