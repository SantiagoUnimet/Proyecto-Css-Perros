# ----------------------------------------------------------------------
# Módulo Bonus: Estadísticas
# ----------------------------------------------------------------------

import matplotlib.pyplot as plt

class GestorEstadisticas:
    """Maneja y grafica los reportes de simulación."""
    
    def __init__(self):
        self.reportes_diarios = []


    def cargar_estadisticas(self, data_estadisticas):
        """Carga el historial de reportes desde el JSON local."""
        if data_estadisticas:
            self.reportes_diarios = data_estadisticas


    def get_estadisticas_para_guardar(self):
        """Retorna la lista de reportes para guardar."""
        return self.reportes_diarios


    def agregar_reporte(self, reporte_dict):
        """Añade un nuevo reporte diario a la lista."""
        self.reportes_diarios.append(reporte_dict)
        print("Reporte del día guardado para estadísticas.")

    
    def mostrar_estadisticas(self):
        """Grafica los valores numéricos de los reportes."""
        num_dias = len(self.reportes_diarios)
        
        if num_dias < 2:
            print(f"Se necesita simular al menos 2 días para mostrar gráficas (Días simulados: {num_dias}).")
            return

        print(f"Generando gráficas para {num_dias} días simulados...")
        
        dias = range(1, num_dias + 1)
        total_clientes = [r['total_clientes'] for r in self.reportes_diarios]
        clientes_opinion = [r['clientes_opinion'] for r in self.reportes_diarios]
        clientes_no_compra = [r['clientes_no_compra'] for r in self.reportes_diarios]
        promedio_hd = [r['promedio_hd_cliente'] for r in self.reportes_diarios]
        total_acomp = [r['total_acomp_vendidos'] for r in self.reportes_diarios]

        try:
            fig, axs = plt.subplots(3, 2, figsize=(15, 12))
            fig.suptitle('Estadísticas de Simulación "Hot Dog CCS"')

            axs[0, 0].plot(dias, total_clientes, marker='o', color='b')
            axs[0, 0].set_title('Total de Clientes por Día')
            axs[0, 0].set_xlabel('Día')
            axs[0, 0].set_ylabel('Clientes')

            axs[0, 1].plot(dias, clientes_opinion, marker='o', color='g')
            axs[0, 1].set_title('Clientes que cambiaron de opinión')
            axs[0, 1].set_xlabel('Día')
            axs[0, 1].set_ylabel('Clientes')

            axs[1, 0].plot(dias, clientes_no_compra, marker='o', color='r')
            axs[1, 0].set_title('Clientes que no pudieron comprar')
            axs[1, 0].set_xlabel('Día')
            axs[1, 0].set_ylabel('Clientes')

            axs[1, 1].plot(dias, promedio_hd, marker='o', color='purple')
            axs[1, 1].set_title('Promedio de Hot Dogs por Cliente Atendido')
            axs[1, 1].set_xlabel('Día')
            axs[1, 1].set_ylabel('Promedio HDs')

            axs[2, 0].plot(dias, total_acomp, marker='o', color='orange')
            axs[2, 0].set_title('Total Acompañantes Vendidos')
            axs[2, 0].set_xlabel('Día')
            axs[2, 0].set_ylabel('Cantidad')
            
            axs[2, 1].axis('off')

            plt.tight_layout(rect=[0, 0.03, 1, 0.95])
            plt.show()
            
        except ImportError:
            print("\nError: Se necesita la librería 'matplotlib' para las gráficas.")
            print("Por favor, instálala con: pip install matplotlib")
        except Exception as e:
            print(f"Error al generar la gráfica: {e}")

