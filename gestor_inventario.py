# gestor_inventario.py

import json

class GestorInventario:
    """
    Módulo para la administración de las existencias de ingredientes (Módulo 2).
    """
    def __init__(self, catalogo_ingredientes):
        """Inicializa el gestor de inventario."""
        
        self._existencias = {} 
        self._datos_locales_ruta = "datos_locales_inventario.json"
        
        # Este catálogo ahora viene con claves en minúscula
        self._catalogo_ingredientes = catalogo_ingredientes 

        if not self._catalogo_ingredientes:
            print("⚠️ ADVERTENCIA (GestorInventario): Se recibió un catálogo de ingredientes vacío.")

        self.cargar_datos_locales()
    
    def cargar_datos_locales(self):
        """Carga las existencias guardadas desde el archivo JSON local."""
        try:
            with open(self._datos_locales_ruta, 'r', encoding='utf-8') as f:
                self._existencias = json.load(f)
                print(f"✅ Inventario de {len(self._existencias)} productos cargado.")
        except (FileNotFoundError, json.JSONDecodeError):
            print("ℹ️ No se encontró el archivo de inventario o hubo error de decodificación. Iniciando inventario vacío.")
            self._existencias = {}

    def guardar_datos_locales(self):
        """Guarda las existencias actuales en el archivo JSON local."""
        try:
            with open(self._datos_locales_ruta, 'w', encoding='utf-8') as f:
                json.dump(self._existencias, f, indent=4)
        except IOError:
            print("❌ Error al guardar los datos del inventario.")

    # 1. Visualizar todo el inventario
    def visualizar_inventario(self):
        """Muestra una lista de todos los ingredientes con su existencia."""
        print("\n--- Existencias de Inventario (Nombre: Cantidad) ---")
        if not self._existencias:
            print("El inventario está vacío.")
            return

        for nombre, cantidad in sorted(self._existencias.items()):
            # La validación 'in' ahora funcionará
            estado = "✅" if nombre in self._catalogo_ingredientes else "⚠️ (No en Catálogo)"
            print(f"{estado} {nombre}: {cantidad}")
        
        print(f"Total de productos con stock: {len(self._existencias)}")

    # 2. Buscar la existencia de un ingrediente específico
    def buscar_existencia_especifica(self):
        """Busca y muestra la cantidad de un ingrediente específico."""
        
        # Convierte la entrada a minúscula
        nombre = input("▶️ Ingrese el nombre exacto del ingrediente a buscar: ").strip().lower()
        
        cantidad = self._existencias.get(nombre)
        
        if cantidad is not None:
            print(f"✅ Existencia de '{nombre}': {cantidad} unidades")
        else:
            print(f"ℹ️ No hay existencias registradas para '{nombre}'.")
            
            # Esta validación ahora funcionará
            if nombre in self._catalogo_ingredientes: 
                print(f"   (Nota: El ingrediente '{nombre}' existe en el catálogo, pero no tiene inventario.)")
            else:
                print(f"   (Nota: El ingrediente '{nombre}' tampoco existe en el catálogo maestro.)")

    # 3. Listar las existencias de todos los ingredientes de una categoría
    def listar_existencias_por_categoria(self):
        """Muestra las existencias de ingredientes filtrados por categoría."""
        
        print("\nSeleccione la categoría a listar:")
        print("1. Pan")
        print("2. Salchicha")
        print("3. Acompañante")
        print("4. Salsa")
        print("5. Topping")
        num = input("--> ").strip()
        
        if num not in ["1", "2", "3", "4", "5"]:
            print("❌ Opción de categoría inválida.")
            return

        categoria_map = { "1": "Pan", "2": "Salchicha", "3": "Acompañante", "4": "Salsa", "5": "Topping" }
        categoria_str = categoria_map[num]
        print(f"\n--- Existencias en '{categoria_str}' ---")
        
        encontrados_en_categoria = False
        
        for ingrediente_obj in self._catalogo_ingredientes.values():
            if ingrediente_obj.get_categoria() == categoria_str:
                encontrados_en_categoria = True
                nombre_ing = ingrediente_obj.get_nombre()
                cantidad = self._existencias.get(nombre_ing, 0) # Default 0
                print(f"- {nombre_ing}: {cantidad} unidades")
        
        if not encontrados_en_categoria:
            print(f"No hay ingredientes registrados en el catálogo en la categoría '{categoria_str}'.")

    # 4. Actualizar la existencia de un producto específico (Interactivo)
    def actualizar_existencia_interactivo(self):
        """Permite al usuario añadir o quitar stock de un ingrediente."""
        
        nombre = input("▶️ Ingrese el nombre exacto del ingrediente a actualizar: ").strip().lower()
        
        # Esta validación ahora funcionará
        if nombre not in self._catalogo_ingredientes: 
            print(f"❌ Error: El ingrediente '{nombre}' no está registrado en el Gestor de Ingredientes.")
            print("Solo se puede actualizar el inventario de ingredientes existentes.")
            return
        
        try:
            cantidad_str = input(f"▶️ Ingrese la cantidad a AÑADIR (ej: 100) o QUITAR (ej: -25) para '{nombre}': ")
            cantidad = int(cantidad_str)
        except ValueError:
            print("❌ Error: La cantidad debe ser un número entero.")
            return

        self._actualizar_existencia_helper(nombre, cantidad)
        print(f"✅ Inventario actualizado. Nueva cantidad para '{nombre}': {self._existencias.get(nombre, 0)}")

    # --- Métodos de Ayuda ---

    def _actualizar_existencia_helper(self, nombre, cantidad):
        """Lógica interna para actualizar el stock."""
        nombre_lower = nombre.lower()
        nueva_cantidad = self._existencias.get(nombre_lower, 0) + cantidad
        
        if nueva_cantidad < 0:
            print(f"⚠️ Advertencia: Se intentó restar más de lo que había para '{nombre_lower}'. El inventario se ha fijado en 0.")
            nueva_cantidad = 0
            
        self._existencias[nombre_lower] = nueva_cantidad
        self.guardar_datos_locales() 

    def verificar_existencia_para_orden(self, requerimientos):
        """Verifica existencia sin consumir (usado por GestorMenu y Simulador)."""
        for nombre, cantidad_requerida in requerimientos.items():
            if self._existencias.get(nombre, 0) < cantidad_requerida:
                return False
        return True
    
    def actualizar_existencia(self, nombre, cantidad, gestor_ingredientes=None):
         """Función de compatibilidad usada por la simulación."""
         if nombre not in self._catalogo_ingredientes: 
            print(f"❌ ADVERTENCIA (GestorInventario): El ingrediente '{nombre}' no existe en el catálogo maestro. No se actualiza.")
            return
         self._actualizar_existencia_helper(nombre, cantidad)

         
