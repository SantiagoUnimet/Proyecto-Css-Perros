import matplotlib as plt
import random
import json
from gestor_ingredientes import *



    # Métodos de Persistencia
def cargar_datos_locales():
        try:
            with open(datos_locales_ruta, 'r', encoding='utf-8') as f:
                historial_simulaciones = json.load(f)
                print(f"✅ Historial de {len(historial_simulaciones)} días de simulación cargado.")
        except FileNotFoundError:
            print("ℹ️ No se encontró historial de simulación.")
        except json.JSONDecodeError:
            print("❌ Error al decodificar el archivo JSON de simulación.")
            return historial_simulaciones
        
historial_simulaciones =cargar_datos_locales()

def guardar_datos_locales():
        try:
            with open(datos_locales_ruta, 'w', encoding='utf-8') as f:
                json.dump(historial_simulaciones, f, indent=4)
        except Exception as e:
            print(f"❌ Error al guardar historial de simulación: {e}")
            
    # Métodos de Simulación
def simular_dia(gestor_menu, gestor_inventario, gestor_ingredientes):
        """Simula un día de ventas completo y actualiza el inventario."""
        menu = gestor_menu.get_menu()
        if not menu:
            print("❌ No se puede simular el día: ¡El menú está vacío!")
            return

        # --- Inicialización de variables del día ---
        clientes_totales = random.randint(0, 200) 
        clientes_cambiaron_opinion = 0
        clientes_no_pudieron_comprar = 0
        total_hotdogs_vendidos = 0
        acompanantes_vendidos = 0
        hotdogs_que_causaron_marcha = []
        ingredientes_que_causaron_marcha = []
        ventas_dia = {}

        print(f"\n======== INICIANDO SIMULACIÓN DE DÍA ========")
        print(f"Clientes esperados: {clientes_totales}")

        nombres_menu = list(menu.keys())
        
        for i in range(clientes_totales):
            num_hotdogs_cliente = random.randint(0, 5)

            if num_hotdogs_cliente == 0:
                clientes_cambiaron_opinion += 1
                continue
            
            orden_cliente_exitosa = True
            orden_requerimientos = {} 
            hotdogs_a_comprar = []
            
            for _ in range(num_hotdogs_cliente):
                nombre_hd = random.choice(nombres_menu)
                hotdog = menu[nombre_hd]
                hotdogs_a_comprar.append(hotdog)
                
                requerimientos_hd = hotdog.obtener_requerimientos()
                
                # Integrar requerimientos a la orden total
                for ing, cant in requerimientos_hd.items():
                    orden_requerimientos[ing] = orden_requerimientos.get(ing, 0) + cant

            # --- Revisar Inventario y Consumir ---
            ingrediente_faltante = None
            hotdog_fallido = None

            # Buscar el ingrediente que causa el fallo (primero en fallar)
            for ingrediente, cantidad in orden_requerimientos.items():
                if gestor_inventario._existencias.get(ingrediente, 0) < cantidad:
                    orden_cliente_exitosa = False
                    ingrediente_faltante = ingrediente
                    
                    # Identificar cuál HotDog en la orden falló
                    for hd in hotdogs_a_comprar:
                        reqs_hd = hd.obtener_requerimientos()
                        if ingrediente in reqs_hd:
                            hotdog_fallido = hd.get_nombre()
                            break
                    
                    break

            if orden_cliente_exitosa:
                # Éxito: Restar inventario y registrar venta
                
                # Consumir el inventario
                for ing, cant in orden_requerimientos.items():
                    gestor_inventario.actualizar_existencia(ing, -cant, gestor_ingredientes)
                
                # Registrar estadísticas
                total_hotdogs_vendidos += num_hotdogs_cliente
                for hd in hotdogs_a_comprar:
                    ventas_dia[hd.get_nombre()] = ventas_dia.get(hd.get_nombre(), 0) + 1
                
                for hd in hotdogs_a_comprar:
                    if hd._acompanante_combo:
                        acompanantes_vendidos += 1
                
            else:
                # Fracaso: Cliente se marcha
                clientes_no_pudieron_comprar += 1
                hotdogs_que_causaron_marcha.append(hotdog_fallido)
                ingredientes_que_causaron_marcha.append(ingrediente_faltante)

        # --- Reporte Final del Día ---
        registrar_resultados(
            clientes_totales, clientes_cambiaron_opinion, clientes_no_pudieron_comprar,
            total_hotdogs_vendidos, ventas_dia, hotdogs_que_causaron_marcha, 
            ingredientes_que_causaron_marcha, acompanantes_vendidos
        )
        
        reportar_resultados()
        
def registrar_resultados(clientes_totales, clientes_cambiaron_opinion, clientes_no_pudieron_comprar, total_hotdogs_vendidos, ventas_dia, hotdogs_que_causaron_marcha, ingredientes_que_causaron_marcha, acompanantes_vendidos):
        """Almacena los resultados del día en el historial."""
        
        hotdog_mas_vendido = max(ventas_dia, key=ventas_dia.get) if ventas_dia else "N/A"
        
        resultados_dia = {
            "clientes_totales": clientes_totales,
            "clientes_cambiaron_opinion": clientes_cambiaron_opinion,
            "clientes_no_pudieron_comprar": clientes_no_pudieron_comprar,
            "total_hotdogs_vendidos": total_hotdogs_vendidos,
            "hotdog_mas_vendido": hotdog_mas_vendido,
            "promedio_hotdogs_por_cliente": total_hotdogs_vendidos / clientes_totales if clientes_totales > 0 else 0,
            "hotdogs_que_causaron_marcha": list(set(hotdogs_que_causaron_marcha)),
            "ingredientes_que_causaron_marcha": list(set(ingredientes_que_causaron_marcha)),
            "acompanantes_vendidos": acompanantes_vendidos
        }
        
        historial_simulaciones.append(resultados_dia)
        guardar_datos_locales()

def reportar_resultados():
        """Imprime las estadísticas del último día simulado."""
        if not historial_simulaciones:
            print("No hay simulaciones para reportar.")
            return

        resultados = historial_simulaciones[-1]
        
        print("\n--- REPORTE FINAL DEL DÍA SIMULADO ---")
        print(f"Total de Clientes: {resultados['clientes_totales']}") 
        print(f"Clientes que cambiaron de opinión: {resultados['clientes_cambiaron_opinion']}") 
        print(f"Clientes que NO pudieron comprar: {resultados['clientes_no_pudieron_comprar']}") 
        print(f"Total de Hot Dogs vendidos: {resultados['total_hotdogs_vendidos']}")
        print(f"Promedio de Hot Dogs por cliente: {resultados['promedio_hotdogs_por_cliente']:.2f}") 
        print(f"Hot Dog más vendido: {resultados['hotdog_mas_vendido']}") 
        print(f"Total de Acompañantes vendidos: {resultados['acompanantes_vendidos']}") 
        
        print("\nDetalles de Fallos:")
        print(f"Hot Dogs que causaron que el cliente se marchara: {', '.join(resultados['hotdogs_que_causaron_marcha'])}") 
        print(f"Ingredientes que causaron que el cliente se marchara: {', '.join(resultados['ingredientes_que_causaron_marcha'])}")

def mostrar_estadisticas_historicas():
        """Muestra gráficas de las métricas clave de la simulación histórica (Bono)."""
        if len(historial_simulaciones) < 2:
            print("⚠️ El módulo de estadísticas requiere al menos 2 días de simulación para generar gráficas.")
            return

        print("\n--- Generando Gráficas Históricas (Bono) ---")
        
        dias = range(1, len(historial_simulaciones) + 1)
        
        clientes_totales = [d['clientes_totales'] for d in historial_simulaciones]
        hotdogs_vendidos = [d['total_hotdogs_vendidos'] for d in historial_simulaciones]
        clientes_no_pudieron_comprar = [d['clientes_no_pudieron_comprar'] for d in historial_simulaciones]
        acompanantes_vendidos = [d['acompanantes_vendidos'] for d in historial_simulaciones]
        promedio_por_cliente = [d['promedio_hotdogs_por_cliente'] for d in historial_simulaciones]

        fig, axs = plt.subplots(2, 2, figsize=(12, 10))
        fig.suptitle('Estadísticas Históricas de Ventas de Hot Dog CCS', fontsize=16)

        axs[0, 0].plot(dias, clientes_totales, marker='o', label='Clientes Totales')
        axs[0, 0].plot(dias, hotdogs_vendidos, marker='x', label='Hot Dogs Vendidos')
        axs[0, 0].set_title('A. Clientes y Hot Dogs Vendidos')
        axs[0, 0].set_xlabel('Día de Simulación')
        axs[0, 0].set_ylabel('Cantidad')
        axs[0, 0].set_xticks(dias)
        axs[0, 0].legend()
        axs[0, 0].grid(True, linestyle='--', alpha=0.6)

        axs[0, 1].bar(dias, clientes_no_pudieron_comprar, color='red', alpha=0.7)
        axs[0, 1].set_title('B. Clientes Perdidos (Falta de Inventario)')
        axs[0, 1].set_xlabel('Día de Simulación')
        axs[0, 1].set_ylabel('Clientes')
        axs[0, 1].set_xticks(dias)
        axs[0, 1].grid(axis='y', linestyle='--', alpha=0.6)

        axs[1, 0].plot(dias, acompanantes_vendidos, marker='s', color='green')
        axs[1, 0].set_title('C. Acompañantes Vendidos')
        axs[1, 0].set_xlabel('Día de Simulación')
        axs[1, 0].set_ylabel('Cantidad')
        axs[1, 0].set_xticks(dias)
        axs[1, 0].grid(True, linestyle='--', alpha=0.6)

        axs[1, 1].plot(dias, promedio_por_cliente, marker='^', color='purple')
        axs[1, 1].set_title('D. Promedio de Hot Dogs por Cliente')
        axs[1, 1].set_xlabel('Día de Simulación')
        axs[1, 1].set_ylabel('Promedio')
        axs[1, 1].set_xticks(dias)
        axs[1, 1].grid(True, linestyle='--', alpha=0.6)

        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.show()
