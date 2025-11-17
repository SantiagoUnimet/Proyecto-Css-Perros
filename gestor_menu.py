# ----------------------------------------------------------------------
# Módulo 3: Gestión del menú
# ----------------------------------------------------------------------

import utils
from hotdogs import HotDog

class GestorMenu:
    """Administra el menú de Hot Dogs (alta, baja, consulta)."""
    def __init__(self, gestor_ingredientes):
        self._hotdogs = []
        self._hotdogs_por_nombre = {}
        self._gestor_ingredientes = gestor_ingredientes
        self._nombres_hotdogs_api = set()
        self._nombres_api_eliminados = set()


    def _buscar_ingredientes_para_hotdog(self, data):
        """
        Ayudante para cargar_menu. Busca los OBJETOS ingredientes
        a partir de los NOMBRES en el JSON.
        """
        try:
            if 'nombre' not in data:
                print("Error procesando hotdog (JSON): Falta la llave 'nombre'.")
                return None
            pan_nombre = data['Pan']
            sal_nombre = data['Salchicha']
            top_nombres = data['toppings']
            aco_nombre = data['Acompañante']
            sal_nombres = data.get('Salsas', data.get('salsas'))
            if sal_nombres is None:
                print(f"Advertencia: Hotdog '{data.get('nombre')}' no tiene llave 'Salsas' ni 'salsas'. Asignando lista vacía.")
                sal_nombres = []
            pan_obj = self._gestor_ingredientes.buscar_ingrediente(pan_nombre)
            sal_obj = self._gestor_ingredientes.buscar_ingrediente(sal_nombre)
            if not pan_obj:
                print(f"No se pudo cargar '{data['nombre']}': El ingrediente 'pan' ({pan_nombre}) no existe.")
                return None
            if not sal_obj:
                print(f"No se pudo cargar '{data['nombre']}': El ingrediente 'salchicha' ({sal_nombre}) no existe.")
                return None
            top_objs = [self._gestor_ingredientes.buscar_ingrediente(t) for t in top_nombres]
            sal_objs = [self._gestor_ingredientes.buscar_ingrediente(s) for s in sal_nombres]
            aco_obj = self._gestor_ingredientes.buscar_ingrediente(aco_nombre)
            top_objs = [t for t in top_objs if t]
            sal_objs = [s for s in sal_objs if s]
            return HotDog(data['nombre'], pan_obj, sal_obj, top_objs, sal_objs, aco_obj)
        except KeyError as e:
            print(f"Error procesando hotdog '{data.get('nombre', '???')}' (JSON): Falta la llave {e}.")
            return None
        except Exception as e:
            print(f"Error inesperado procesando hotdog '{data.get('nombre', '???')}': {e}")
            return None


    def cargar_menu_api(self, menu_data_api, api_eliminados_local):
        """Carga el menú base de la API."""
        if not menu_data_api:
            return
        self._nombres_api_eliminados = set(api_eliminados_local)
        for data in menu_data_api:
            nombre_hd = data.get('nombre')
            if nombre_hd in self._nombres_api_eliminados:
                continue
            hotdog = self._buscar_ingredientes_para_hotdog(data)
            if hotdog:
                self._hotdogs.append(hotdog)
                self._hotdogs_por_nombre[hotdog.get_nombre()] = hotdog
                self._nombres_hotdogs_api.add(hotdog.get_nombre())


    def cargar_menu_local(self, menu_data_local):
        """Carga el menú creado por el usuario."""
        for data in menu_data_local:
            if data['nombre'] not in self._hotdogs_por_nombre:
                hotdog = self._buscar_ingredientes_para_hotdog(data)
                if hotdog:
                    self._hotdogs.append(hotdog)
                    self._hotdogs_por_nombre[hotdog.get_nombre()] = hotdog


    def get_menu_para_guardar(self):
        """Retorna una lista de diccionarios de los hotdogs NO API."""
        locales = []
        for hotdog in self._hotdogs:
            if hotdog.get_nombre() not in self._nombres_hotdogs_api:
                locales.append(hotdog.to_dict())
        return locales


    def get_hotdogs(self):
        """Retorna la lista de todos los objetos HotDog."""
        return self._hotdogs


    def buscar_hotdog(self, nombre):
        """Busca un hotdog por nombre. Retorna el objeto o None."""
        return self._hotdogs_por_nombre.get(nombre)


    def ver_lista_hotdogs(self):
        """Módulo 3.1: Ver la lista de hot dogs."""
        print("\n--- Menú de Hot Dogs ---")
        if not self._hotdogs:
            print("No hay hot dogs en el menú.")
            return
        for hd in self._hotdogs:
            print(f"  -> {hd.get_nombre()}")


    def ver_inventario_para_hotdog(self, nombre_hotdog, gestor_inventario):
        """Módulo 3.2: Ver si hay inventario para un hot dog específico."""
        hotdog = self.buscar_hotdog(nombre_hotdog)
        if not hotdog:
            print(f"Error: No se encontró el hot dog '{nombre_hotdog}'.")
            return
        if hotdog.validar_inventario(gestor_inventario):
            print(f"¡Hay inventario suficiente para preparar '{nombre_hotdog}'!")
        else:
            print(f"No hay inventario suficiente para preparar '{nombre_hotdog}'.")
            req = hotdog.obtener_requerimientos()
            _, ing_faltante = gestor_inventario.verificar_existencia_para_orden(req)
            if ing_faltante:
                print(f"  (Falta o no hay suficiente: {ing_faltante})")


    def agregar_hotdog(self, hotdog_obj, gestor_inventario):
        """Módulo 3.3: Agrega un nuevo hot dog al menú."""
        nombre = hotdog_obj.get_nombre()
        if nombre in self._hotdogs_por_nombre:
            print(f"Error: Ya existe un hot dog con el nombre '{nombre}'.")
            return False
        pan = hotdog_obj.get_pan()
        salchicha = hotdog_obj.get_salchicha()
        if hasattr(pan, 'es_compatible') and not pan.es_compatible(salchicha):
            print(f"Advertencia: El tamaño del pan ({pan._tamaño}{pan._unidad}) no coincide con la salchicha ({salchicha._tamaño}{salchicha._unidad}).")
            if not utils.validar_confirmacion("¿Desea agregarlo de todas formas?"):
                print("Registro de hot dog cancelado.")
                return False
        if not hotdog_obj.validar_inventario(gestor_inventario):
            print("Advertencia: No hay inventario suficiente de uno o más ingredientes para este hot dog.")
        self._hotdogs.append(hotdog_obj)
        self._hotdogs_por_nombre[nombre] = hotdog_obj
        print(f"Hot dog '{nombre}' agregado al menú exitosamente.")
        return True


    def eliminar_hotdog(self, nombre_hotdog, gestor_inventario):
        """Módulo 3.4: Elimina un hot dog (con validación de inventario)."""
        hotdog = self.buscar_hotdog(nombre_hotdog)
        if not hotdog:
            print(f"Error: No se encontró el hot dog '{nombre_hotdog}'.")
            return
        if gestor_inventario is not None:
            if hotdog.validar_inventario(gestor_inventario):
                print(f"Advertencia: Aún hay inventario suficiente para seguir vendiendo '{nombre_hotdog}'.")
                if not utils.validar_confirmacion("¿Está seguro de que desea eliminarlo del menú?"):
                    print("Eliminación cancelada.")
                    return
        if nombre_hotdog in self._nombres_hotdogs_api:
            self._nombres_api_eliminados.add(nombre_hotdog)
            print(f"'{nombre_hotdog}' agregado a la lista de eliminación permanente de la API.")
        self.eliminar_hotdog_directo(nombre_hotdog)
        print(f"Hot dog '{nombre_hotdog}' eliminado del menú.")


    def eliminar_hotdog_directo(self, nombre_hotdog):
        """Elimina un hotdog sin validaciones (usado por Módulo 1)."""
        hotdog = self._hotdogs_por_nombre.get(nombre_hotdog)
        if hotdog:
            self._hotdogs.remove(hotdog)
            del self._hotdogs_por_nombre[nombre_hotdog]
            print(f"(Hot dog '{nombre_hotdog}' eliminado por dependencia de ingrediente)")


    def hotdogs_que_usan_ingrediente(self, nombre_ingrediente):
        """Retorna una lista de hotdogs (objetos) que usan un ingrediente."""
        afectados = []
        for hotdog in self._hotdogs:
            if nombre_ingrediente in hotdog.get_ingredientes_nombres():
                afectados.append(hotdog)
        return afectados


    def get_api_eliminados_para_guardar(self):
        """Retorna la lista de hotdogs API eliminados."""
        return list(self._nombres_api_eliminados)
    
