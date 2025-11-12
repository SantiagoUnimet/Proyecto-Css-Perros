import matplotlib.pyplot as plt
import json
import random


# ----------------------------------------------------------------------
# 1. Clases de Entidad (Datos del Hot Dog)
# ----------------------------------------------------------------------

class Ingrediente:
    """
    Representa un ingrediente básico del sistema (Pan, Salchicha, Topping, etc.).
    """
    def __init__(self, nombre, categoria, tipo, tamaño, unidad, id_data=None):
        """Inicializa un Ingrediente."""
        # Atributos privados (-)
        self._nombre = nombre
        self._categoria = categoria
        self._tipo = tipo
        self._tamaño = tamaño
        self._unidad = unidad
        self._id = id_data if id_data is not None else {}

    # Métodos públicos (+)
    def to_dict(self):
        """Serializa el objeto a diccionario para guardarlo en JSON."""
        return {
            "nombre": self._nombre,
            "categoria": self._categoria,
            "tipo": self._tipo,
            "tamaño": self._tamaño,
            "unidad": self._unidad,
        }
        
    def get_nombre(self):
        return self._nombre

    def es_compatible(self, otro_ingrediente):
        """
        Valida la compatibilidad de este ingrediente con otro (ej: longitud de pan y salchicha).
        Retorna True si son compatibles.
        """
        # La compatibilidad es True si las longitudes son idénticas
        return self._tamaño == otro_ingrediente._tamaño


