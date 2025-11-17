# ----------------------------------------------------------------------
# 1. Clases de Entidad (Datos del Ingrediente)
# ----------------------------------------------------------------------

class Ingrediente:
    """Representa un ingrediente básico del sistema (Pan, Salchicha, Topping, etc.)."""
    def __init__(self, categoria, nombre):
        """Inicializa un Ingrediente."""
        self._categoria = categoria
        self._nombre = nombre


    def __str__(self):
        """Muestra los atributos del la clase."""
        return f"{self._categoria}: {self._nombre}"


    def get_categoria(self):
        return self._categoria


    def get_nombre(self):
        return self._nombre


    def to_dict(self):
        """Convierte el objeto a un diccionario para serializar en JSON."""
        return {
            "categoria": self._categoria,
            "nombre": self._nombre,
            "clase": self.__class__.__name__ 
        }
    
    
class Pan(Ingrediente):
    """Crea una subclase de Ingrediente para el manejo de la API."""
    def __init__(self, categoria, nombre, tipo, tamaño, unidad):
        super().__init__(categoria, nombre)
        self._tipo = tipo
        self._tamaño = tamaño
        self._unidad = unidad
    

    def __str__(self):
        """Muestra los atributos de la clase."""
        return f"{self._categoria}: {self._nombre}, {self._tipo}, {self._tamaño}, {self._unidad}"
    

    def es_compatible(self, otro_ingrediente):
        """Valida la compatibilidad de este ingrediente con otro (ej: longitud de pan y salchicha).
        Retorna True si son compatibles.
        """
        return self._tamaño == otro_ingrediente._tamaño


    def get_nombre(self):
        return f"{self._nombre}"


    def to_dict(self):
        """Convierte el objeto a un diccionario."""
        data = super().to_dict()
        data.update({
            "tipo": self._tipo,
            "tamaño": self._tamaño,
            "unidad": self._unidad
        })
        return data


class Salchicha(Ingrediente):
    """Crea una subclase de Ingrediente para el manejo de la API."""
    def __init__(self, categoria, nombre, tipo, tamaño, unidad):
        super().__init__(categoria, nombre)
        self._tipo = tipo
        self._tamaño = tamaño
        self._unidad = unidad
    

    def __str__(self):
        """Muestra los atributos de la clase."""
        return f"{self._categoria}: {self._nombre}, {self._tipo}, {self._tamaño}, {self._unidad}"
    

    def es_compatible(self, otro_ingrediente):
        """Valida la compatibilidad de este ingrediente con otro (ej: longitud de pan y salchicha).
        Retorna True si son compatibles.
        """
        return self._tamaño == otro_ingrediente._tamaño
    

    def to_dict(self):
        """Convierte el objeto a un diccionario."""
        data = super().to_dict()
        data.update({
            "tipo": self._tipo,
            "tamaño": self._tamaño,
            "unidad": self._unidad
        })
        return data


class Acompañante(Ingrediente):
    """Crea una subclase de Ingrediente para el manejo de la API."""
    def __init__(self, categoria, nombre, tipo, tamaño, unidad):
        super().__init__(categoria, nombre)
        self._tipo = tipo
        self._tamaño = tamaño
        self._unidad = unidad
    

    def __str__(self):
        """Muestra los atributos de la clase."""
        return f"{self._categoria}: {self._nombre}, {self._tipo}, {self._tamaño}, {self._unidad}"
    

    def to_dict(self):
        """Convierte el objeto a un diccionario."""
        data = super().to_dict()
        data.update({
            "tipo": self._tipo,
            "tamaño": self._tamaño,
            "unidad": self._unidad
        })
        return data


class Salsa(Ingrediente):
    """Crea una subclase de Ingrediente para el manejo de la API."""
    def __init__(self, categoria, nombre, base, color):
        super().__init__(categoria, nombre)
        self._base = base
        self._color = color


    def __str__(self):
        """Muestra los atributos de la clase."""
        return f"{self._categoria}: {self._nombre}, {self._base}, {self._color}"


    def to_dict(self):
        """Convierte el objeto a un diccionario."""
        data = super().to_dict()
        data.update({
            "base": self._base,
            "color": self._color
        })
        return data


class Topping(Ingrediente):
    """Crea una subclase de Ingrediente para el manejo de la API."""
    def __init__(self, categoria, nombre, tipo, presentacion):
        super().__init__(categoria, nombre)
        self._tipo = tipo
        self._presentacion = presentacion


    def __str__(self):
        """Muestra los atributos de la clase."""
        return f"{self._categoria}: {self._nombre}, {self._tipo}, {self._presentacion}"


    def to_dict(self):
        """Convierte el objeto a un diccionario."""
        data = super().to_dict()
        data.update({
            "tipo": self._tipo,
            "presentacion": self._presentacion
        })
        return data

