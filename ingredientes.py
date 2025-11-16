# ----------------------------------------------------------------------
# 1. Clases de Entidad (Datos del Ingrediente)
# ----------------------------------------------------------------------

class Ingrediente:
    """Representa un ingrediente básico del sistema (Pan, Salchicha, Topping, etc.)."""
    def __init__(self, categoria, nombre):
        """Inicializa un Ingrediente."""
        # Atributos privados (-)
        self._categoria = categoria
        self._nombre = nombre

    # Métodos públicos (+)
    def __str__(self):
        """Muestra los atributos del la clase."""
        return {
            "categoria": self._categoria,
            "nombre": self._nombre,
        }
        
    def get_categoria(self):
        return self._categoria
    
    def get_nombre(self):
        return {self._nombre}


    
class Pan(Ingrediente):
    def __init__(self, categoria, nombre, tipo, tamaño, unidad):
        super().__init__(categoria, nombre)
        self._tipo = tipo
        self._tamaño = tamaño
        self._unidad = unidad
    
    def __str__(self):
        """SMuestra los atributos de la clase."""
        return f"{self._categoria}: {self._nombre}, {self._tipo}, {self._tamaño}, {self._unidad}"
    
    def es_compatible(self, otro_ingrediente):
        """Valida la compatibilidad de este ingrediente con otro (ej: longitud de pan y salchicha).Retorna True si son compatibles."""
        # La compatibilidad es True si las longitudes son idénticas
        return self._tamaño == otro_ingrediente._tamaño
    
    

class Salchicha(Ingrediente):
    def __init__(self, categoria, nombre, tipo, tamaño, unidad):
        super().__init__(categoria, nombre)
        self._tipo = tipo
        self._tamaño = tamaño
        self._unidad = unidad
    
    def __str__(self):
        """SMuestra los atributos de la clase."""
        return f"{self._categoria}: {self._nombre}, {self._tipo}, {self._tamaño}, {self._unidad}"
    
    def es_compatible(self, otro_ingrediente):
        """Valida la compatibilidad de este ingrediente con otro (ej: longitud de pan y salchicha).Retorna True si son compatibles."""
        # La compatibilidad es True si las longitudes son idénticas
        return self._tamaño == otro_ingrediente._tamaño

class Acompañante(Ingrediente):
    def __init__(self, categoria, nombre, tipo, tamaño, unidad):
        super().__init__(categoria, nombre)
        self._tipo = tipo
        self._tamaño = tamaño
        self._unidad = unidad
    
    def __str__(self):
        """SMuestra los atributos de la clase."""
        return f"{self._categoria}: {self._nombre}, {self._tipo}, {self._tamaño}, {self._unidad}"


class Salsa(Ingrediente):
    def __init__(self, categoria, nombre, base, color):
        super().__init__(categoria, nombre)
        self._base = base
        self._color = color
    
    def __str__(self):
        """SMuestra los atributos de la clase."""
        return f"{self._categoria}: {self._nombre}, {self._base}, {self._color}"

class Topping(Ingrediente):
    def __init__(self, categoria, nombre, tipo, presentacion):
        super().__init__(categoria, nombre)
        self._tipo = tipo
        self._presentacion = presentacion
    
    def __str__(self):
        """SMuestra los atributos de la clase."""
        return f"{self._categoria}: {self._nombre}, {self._tipo}, {self._presentacion}"