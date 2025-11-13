import json
import random


# ----------------------------------------------------------------------
# 1. Clases de Entidad (Datos del Hot Dog)
# ----------------------------------------------------------------------

class Ingrediente:
    """Representa un ingrediente básico del sistema (Pan, Salchicha, Topping, etc.)."""
    def __init__(self, categoria, nombre, tipo, tamaño, unidad):
        """Inicializa un Ingrediente."""
        # Atributos privados (-)
        self._categoria = categoria
        self._nombre = nombre
        self._tipo = tipo
        self._tamaño = tamaño
        self._unidad = unidad

    # Métodos públicos (+)
    def to_dict(self):
        """Serializa el objeto a diccionario para guardarlo en JSON."""
        return {
            "categoria": self._categoria,
            "nombre": self._nombre,
            "tipo": self._tipo,
            "tamaño": self._tamaño,
            "unidad": self._unidad,
        }
        
    def get_categoria(self):
        return self._categoria

    def es_compatible(self, otro_ingrediente):
        """Valida la compatibilidad de este ingrediente con otro (ej: longitud de pan y salchicha).Retorna True si son compatibles."""
        # La compatibilidad es True si las longitudes son idénticas
        return self._tamaño == otro_ingrediente._tamaño


