# ----------------------------------------------------------------------
# Módulo 5: Simular un día de ventas
# ----------------------------------------------------------------------
import random

class Simulador:
    """Ejecuta la simulación de un día de ventas."""
    
    def __init__(self, gestor_menu, gestor_inventario, gestor_ingredientes):
        self._gestor_menu = gestor_menu
        self._gestor_inventario = gestor_inventario
        self._gestor_ingredientes = gestor_ingredientes # ¡ESTA LÍNEA ES NUEVA!

    def simular_dia(self):
        """Ejecuta la lógica de simulación de un día."""
        
        menu_disponible = self._gestor_menu.get_hotdogs()
        if not menu_disponible:
            print("\nError de simulación: No hay hot dogs en el menú.")
            return None # No se puede simular
            
        # 1. Generar clientes
        num_clientes_dia = random.randint(0, 200) 
        
        # Variables para el reporte [cite: 85-92]
        clientes_cambio_opinion = 0
        clientes_no_compraron = 0
        total_hotdogs_vendidos_count = 0
        ventas_por_hotdog = {hd.get_nombre(): 0 for hd in menu_disponible}
        fallos_por_hotdog = {}
        fallos_por_ingrediente = {}
        acompanantes_vendidos_total = 0

        print(f"\n--- INICIANDO SIMULACIÓN (Total Clientes: {num_clientes_dia}) ---")

        # 2. Iterar por cliente
        for i in range(1, num_clientes_dia + 1):
            num_hotdogs_cliente = random.randint(0, 5)
            
            # 3. Cliente cambió de opinión
            if num_hotdogs_cliente == 0:
                print(f"[Cliente {i}] cambió de opinión")
                clientes_cambio_opinion += 1
                continue

            # 4. y 5. Seleccionar hot dogs y acompañantes adicionales
            orden_hotdogs = [] # Lista de objetos HotDog
            requerimientos_orden = {}
            acompanantes_orden = 0
            
            for _ in range(num_hotdogs_cliente):
                # 4. Seleccionar hot dog
                hd_seleccionado = random.choice(menu_disponible)
                orden_hotdogs.append(hd_seleccionado)
                
                # 5. Acompañante adicional
                if random.choice([True, False]):
                    # Asumimos que "Acompañante" es una categoría
                    # (Esto es ambiguo en el PDF. Asumo que es CUALQUIER acompañante)
                    acomp_disponibles = self._gestor_ingredientes._ingredientes_por_categoria.get("Acompañante")
                    if acomp_disponibles:
                        acomp_extra = random.choice(acomp_disponibles)
                        # Agregamos el acompañante extra a los requerimientos
                        req_acomp = { acomp_extra.get_nombre(): 1 }
                        self._actualizar_requerimientos(requerimientos_orden, req_acomp)
                        acompanantes_orden += 1

                # Sumar requerimientos del hot dog (incluye su acompañante de combo si tiene)
                req_hd = hd_seleccionado.obtener_requerimientos()
                self._actualizar_requerimientos(requerimientos_orden, req_hd)
                
                # Contar acompañantes de combo [cite: 92]
                if hd_seleccionado._acompanante:
                    acompanantes_orden += 1

            # 6. Revisar inventario para la orden COMPLETA
            puede_comprar, ing_faltante = self._gestor_inventario.verificar_existencia_para_orden(requerimientos_orden)

            if puede_comprar:
                # 6a. Sí hay
                self._gestor_inventario.restar_de_inventario(requerimientos_orden)
                total_hotdogs_vendidos_count += num_hotdogs_cliente
                acompanantes_vendidos_total += acompanantes_orden
                
                nombres_hd_orden = [hd.get_nombre() for hd in orden_hotdogs]
                print(f"[Cliente {i}] compró: {', '.join(nombres_hd_orden)}")
                
                # Actualizar estadísticas de venta
                for hd_nombre in nombres_hd_orden:
                    ventas_por_hotdog[hd_nombre] += 1
            
            else:
                # 6b. No hay
                clientes_no_compraron += 1
                
                # Determinar cuál hot dog causó el fallo
                # (Simplificación: el primer hot dog que contenga el ingrediente faltante)
                hd_fallido_nombre = "N/A (Acompañante extra)"
                for hd in orden_hotdogs:
                    if ing_faltante in hd.obtener_requerimientos():
                        hd_fallido_nombre = hd.get_nombre()
                        break
                        
                print(f"[Cliente {i}] se marchó sin llevarse nada. No se pudo comprar '{hd_fallido_nombre}' (Faltó: {ing_faltante})")
                
                # Actualizar estadísticas de fallo
                fallos_por_hotdog[hd_fallido_nombre] = fallos_por_hotdog.get(hd_fallido_nombre, 0) + 1
                fallos_por_ingrediente[ing_faltante] = fallos_por_ingrediente.get(ing_faltante, 0) + 1

        print("--- SIMULACIÓN FINALIZADA ---")
        
        # Generar Reporte
        return self._generar_reporte(
            num_clientes_dia, 
            clientes_cambio_opinion, 
            clientes_no_compraron, 
            total_hotdogs_vendidos_count, 
            ventas_por_hotdog,
            fallos_por_hotdog,
            fallos_por_ingrediente,
            acompanantes_vendidos_total
        )
        
    def _actualizar_requerimientos(self, req_total, req_nuevo):
        """Ayudante para sumar diccionarios de requerimientos."""
        for item, cant in req_nuevo.items():
            req_total[item] = req_total.get(item, 0) + cant

    def _generar_reporte(self, *args):
        """Imprime el reporte al final del día y retorna el dict."""
        
        (total_clientes, clientes_opinion, clientes_no_compra, 
         total_hd_vendidos, ventas_hd, fallos_hd, fallos_ing, total_acomp) = args

        print("\n--- REPORTE DEL DÍA ---")
        
        print(f"Total de clientes: {total_clientes}")
        print(f"Clientes que cambiaron de opinión: {clientes_opinion}")
        print(f"Clientes que no pudieron comprar: {clientes_no_compra}")
        
        clientes_atendidos = total_clientes - clientes_opinion - clientes_no_compra
        if clientes_atendidos > 0:
            promedio_hd = total_hd_vendidos / clientes_atendidos
        else:
            promedio_hd = 0
        print(f"Promedio de hot dogs por cliente (atendido): {promedio_hd:.2f}")

        # Hot dog más vendido
        if ventas_hd:
            hd_mas_vendido = max(ventas_hd, key=ventas_hd.get)
            print(f"Hot dog más vendido: {hd_mas_vendido} ({ventas_hd[hd_mas_vendido]} unidades)")
        else:
            print("Hot dog más vendido: Ninguno (No hubo ventas)")

        print(f"Total acompañantes vendidos (combo + extra): {total_acomp}")

        print("\nHot dogs que causaron que el cliente se marchara:")
        if fallos_hd:
            for hd, count in fallos_hd.items():
                print(f"  - {hd}: {count} veces")
        else:
            print("  (Ninguno)")

        print("\nIngredientes que causaron que el cliente se marchara:")
        if fallos_ing:
            for ing, count in fallos_ing.items():
                print(f"  - {ing}: {count} veces")
        else:
            print("  (Ninguno)")
            
        # Retornar el reporte numérico para las estadísticas
        return {
            "total_clientes": total_clientes,
            "clientes_opinion": clientes_opinion,
            "clientes_no_compra": clientes_no_compra,
            "promedio_hd_cliente": promedio_hd,
            "total_acomp_vendidos": total_acomp
            # (Se pueden agregar más métricas si se desea graficar)
        }
