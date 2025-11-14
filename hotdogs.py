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
        self._acompanante = acompanante

    def get_nombre(self):
        return self._nombre

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

        # 2. Toppings, Salsas y Acompañante de Combo
        for topping in self._toppings:
            if topping:
                requerimientos[topping.get_nombre()] = requerimientos.get(topping.get_nombre(), 0) + 1

        for salsa in self._salsas:
            if salsa:
                requerimientos[salsa.get_nombre()] = requerimientos.get(salsa.get_nombre(), 0) + 1
                
        if self._acompanante_combo:
            requerimientos[self._acompanante_combo.get_nombre()] = requerimientos.get(self._acompanante_combo.get_nombre(), 0) + 1

        return requerimientos

    def validar_inventario(self, gestor_inventario):
        """Verifica si hay inventario suficiente para preparar este HotDog."""
        requerimientos = self.obtener_requerimientos()
        return gestor_inventario.verificar_existencia_para_orden(requerimientos)
    
    

