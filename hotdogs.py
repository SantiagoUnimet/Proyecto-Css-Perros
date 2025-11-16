# ----------------------------------------------------------------------
# 2. Clases de Entidad (Datos del Hot Dog)
# ----------------------------------------------------------------------

class HotDog:
    """Representa una opción de Hot Dog disponible en el menú."""
    def __init__(self, nombre, pan, salchicha, toppings, salsas, acompanante):
        # Atributos privados (-)
        self._nombre = nombre
        self._pan = pan
        self._salchicha = salchicha
        self._toppings = toppings
        self._salsas = salsas
        self._acompanante = acompanante # Acompañante que viene en el combo

    def get_nombre(self):
        return self._nombre

    def get_pan(self):
        return self._pan

    def get_salchicha(self):
        return self._salchicha
        
    def get_ingredientes_nombres(self):
        """Retorna una lista con los nombres de todos los ingredientes que usa."""
        nombres = [self._pan.get_nombre(), self._salchicha.get_nombre()]
        if self._acompanante:
            nombres.append(self._acompanante.get_nombre())
        nombres.extend([t.get_nombre() for t in self._toppings])
        nombres.extend([s.get_nombre() for s in self._salsas])
        return nombres

    def to_dict(self):
        """Serializa el objeto a diccionario para guardarlo en JSON."""
        return {
            "nombre": self._nombre,
            "pan": self._pan.get_nombre() if self._pan else None,
            "salchicha": self._salchicha.get_nombre() if self._salchicha else None,
            "toppings": [t.get_nombre() for t in self._toppings if t],
            "salsas": [s.get_nombre() for s in self._salsas if s],
            "acompanante_combo": self._acompanante.get_nombre() if self._acompanante else None,
        }

    def obtener_requerimientos(self):
        """
        Calcula y retorna un diccionario con el total de ingredientes necesarios
        para preparar una unidad de este Hot Dog. Retorna: {nombre_ingrediente: cantidad}
        """
        requerimientos = {}

        # 1. Ingredientes Principales (siempre 1 unidad)
        if self._pan:
            requerimientos[self._pan.get_nombre()] = requerimientos.get(self._pan.get_nombre(), 0) + 1
        
        if self._salchicha:
            requerimientos[self._salchicha.get_nombre()] = requerimientos.get(self._salchicha.get_nombre(), 0) + 1
        
        # 2. Toppings y Salsas
        for topping in self._toppings:
            if topping:
                requerimientos[topping.get_nombre()] = requerimientos.get(topping.get_nombre(), 0) + 1

        for salsa in self._salsas:
            if salsa:
                requerimientos[salsa.get_nombre()] = requerimientos.get(salsa.get_nombre(), 0) + 1
                
        # 3. Acompañante del combo (si lo tiene)
        if self._acompanante:
            requerimientos[self._acompanante.get_nombre()] = requerimientos.get(self._acompanante.get_nombre(), 0) + 1

        return requerimientos

    def validar_inventario(self, gestor_inventario):
        """Verifica si hay inventario suficiente para preparar este HotDog."""
        requerimientos = self.obtener_requerimientos()
        # Se reutiliza el método del gestor de inventario
        puede_preparar, _ = gestor_inventario.verificar_existencia_para_orden(requerimientos)
        return puede_preparar