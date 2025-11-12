# Importa tus clases
from ingredientes import SistemaHotDogCCS
import gestordeingredientes

# Esta función principal será el punto de entrada
def main():
    # 1. Instanciar el sistema principal
    sistema = SistemaHotDogCCS()
    
    # 2. Iniciar el menú
    sistema.iniciar_principal()



main()