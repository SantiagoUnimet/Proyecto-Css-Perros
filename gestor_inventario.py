# ----------------------------------------------------------------------
# Módulo 2: Gestión de Inventario
# ----------------------------------------------------------------------
import utils

class GestorInventario:
    """Almacena y gestiona las existencias de cada ingrediente."""
    
    def __init__(self, gestor_ingredientes):
        # Diccionario: {nombre_ingrediente: cantidad}
        self._inventario = {}
        # Referencia al gestor de ingredientes para validaciones [cite: 49]
        self._gestor_ingredientes = gestor_ingredientes

    def cargar_inventario_api(self, inventario_data_api):
        """Carga el inventario base de la API."""
        if inventario_data_api:
            self._inventario.update(inventario_data_api)

    def cargar_inventario_local(self, inventario_data_local):
        """
        Sobrescribe el inventario con el local (que guarda el estado
        después de las simulaciones).
        """
        if inventario_data_local:
            self._inventario.update(inventario_data_local)
            
    def get_inventario_para_guardar(self):
        """Retorna el diccionario de inventario actual para guardar en JSON."""
        return self._inventario

    def _validar_ingrediente_existe(self, nombre_ingrediente):
        """Verifica que el ingrediente esté registrado en el Módulo 1."""
        if not self._gestor_ingredientes.buscar_ingrediente(nombre_ingrediente):
            print(f"Advertencia: El ingrediente '{nombre_ingrediente}' existe en inventario pero no en el registro general.")
            return False
        return True

    def visualizar_todo(self):
        """Módulo 2.1: Visualizar todo el inventario."""
        print("\n--- Inventario Total ---")
        if not self._inventario:
            print("El inventario está vacío.")
            return
            
        for nombre, cantidad in self._inventario.items():
            if self._validar_ingrediente_existe(nombre):
                print(f"  -> {nombre}: {cantidad} unidades")

    def buscar_existencia(self, nombre_ingrediente):
        """Módulo 2.2: Buscar la existencia de un ingrediente específico."""
        if not self._validar_ingrediente_existe(nombre_ingrediente):
            print(f"El ingrediente '{nombre_ingrediente}' no está registrado.")
            return
            
        cantidad = self._inventario.get(nombre_ingrediente, 0)
        print(f"  -> Existencia de '{nombre_ingrediente}': {cantidad} unidades")
        return cantidad

    def listar_por_categoria(self, categoria):
        """Módulo 2.3: Listar existencias de todos los ingredientes de una categoría."""
        print(f"\n--- Inventario de '{categoria}' ---")
        # Obtenemos los ingredientes de esa categoría del Módulo 1
        ingredientes_en_categoria = self._gestor_ingredientes._ingredientes_por_categoria.get(categoria, [])
        
        if not ingredientes_en_categoria:
            print(f"No hay ingredientes registrados en la categoría '{categoria}'.")
            return
            
        encontrados = False
        for ingrediente in ingredientes_en_categoria:
            nombre = ingrediente.get_nombre()
            cantidad = self._inventario.get(nombre, 0)
            print(f"  -> {nombre}: {cantidad} unidades")
            encontrados = True
            
        if not encontrados:
             print(f"No hay inventario registrado para la categoría '{categoria}'.")

    def actualizar_existencia(self, nombre_ingrediente, cantidad):
        """Módulo 2.4: Actualizar la existencia de un producto (sumar)."""
        if not self._validar_ingrediente_existe(nombre_ingrediente):
            print(f"Error: No se puede agregar inventario de '{nombre_ingrediente}' porque no está registrado.")
            return
            
        if cantidad < 0:
            print("Error: La cantidad a agregar no puede ser negativa.")
            return

        self._inventario[nombre_ingrediente] = self._inventario.get(nombre_ingrediente, 0) + cantidad
        print(f"Inventario actualizado: {nombre_ingrediente} = {self._inventario[nombre_ingrediente]} unidades")

    # --- Métodos de Ayuda para Módulos 3 y 5 ---

    def verificar_existencia_para_orden(self, requerimientos):
        """
        Verifica si hay suficiente inventario para un diccionario de requerimientos.
        Retorna (True, None) si hay, o (False, nombre_ingrediente_faltante) si no.
        """
        for nombre_ing, cant_necesaria in requerimientos.items():
            cant_disponible = self._inventario.get(nombre_ing, 0)
            if cant_disponible < cant_necesaria:
                return False, nombre_ing # No hay suficiente
        return True, None # Hay suficiente de todo

    def restar_de_inventario(self, requerimientos):
        """Resta los ingredientes de una orden del inventario."""
        for nombre_ing, cant_a_restar in requerimientos.items():
            if nombre_ing in self._inventario:
                self._inventario[nombre_ing] -= cant_a_restar
                # Opcional: ¿Qué pasa si queda negativo? (No debería si se verificó antes)
                if self._inventario[nombre_ing] < 0:
                    print(f"¡Alerta! Inventario de '{nombre_ing}' quedó negativo.")
                    self._inventario[nombre_ing] = 0
            else:
                # Caso raro: se vendió algo que no estaba en inventario
                print(f"¡Alerta! Se vendió '{nombre_ing}' sin registro de inventario.")
