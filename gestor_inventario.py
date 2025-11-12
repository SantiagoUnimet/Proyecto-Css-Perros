class GestorInventario:
    """
    Módulo para la administración de las existencias de ingredientes (Módulo 2).
    """
    def __init__(self):
        self._existencias = {}
        self._datos_locales_ruta = "datos_locales_inventario.json"

    # Métodos de Persistencia
    def cargar_datos_locales(self):
        """Carga las existencias guardadas desde el archivo JSON local."""
        try:
            with open(self._datos_locales_ruta, 'r', encoding='utf-8') as f:
                self._existencias = json.load(f)
                print(f"✅ Inventario cargado: {len(self._existencias)} ítems desde {self._datos_locales_ruta}")
        except FileNotFoundError:
            print("ℹ️ No se encontró archivo de inventario local. Iniciando con inventario vacío.")
        except json.JSONDecodeError:
            print("❌ Error al decodificar el archivo JSON de inventario.")

    def guardar_datos_locales(self):
        """Guarda las existencias actuales en un archivo JSON."""
        try:
            with open(self._datos_locales_ruta, 'w', encoding='utf-8') as f:
                json.dump(self._existencias, f, indent=4)
        except Exception as e:
            print(f"❌ Error al guardar inventario: {e}")

    # Métodos de Gestión
    def ver_existencias(self):
        """Muestra una lista del inventario actual y sus cantidades."""
        print("\n--- Existencias de Inventario ---")
        if not self._existencias:
            print("El inventario está vacío.")
            return

        for nombre, cantidad in self._existencias.items():
            print(f"- {nombre}: {cantidad}")


    def actualizar_existencia(self, nombre, cantidad, gestor_ingredientes):
        """Registra la compra (aumento) o el consumo (disminución) de un ingrediente."""
        if nombre not in gestor_ingredientes.get_ingredientes_maestros():
            return

        nueva_cantidad = self._existencias.get(nombre, 0) + cantidad
        
        if nueva_cantidad < 0:
             nueva_cantidad = 0
             
        self._existencias[nombre] = nueva_cantidad
        self.guardar_datos_locales() 

    def verificar_existencia_para_orden(self, requerimientos):
        """Verifica existencia sin consumir (usado por GestorMenu y Simulador)."""
        for nombre, cantidad_requerida in requerimientos.items():
            if self._existencias.get(nombre, 0) < cantidad_requerida:
                return False
        return True
