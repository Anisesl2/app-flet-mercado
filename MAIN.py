import flet as ft
import yfinance as yf
import time
import threading

def main(page: ft.Page):
    page.title = "Top 10 S&P 500"
    page.theme_mode = "dark"
    page.padding = 20
    page.window_width = 450
    page.window_height = 600

    # --- EL CHIVATO VISUAL (Arreglado sin iconos) ---
    # Usamos un carácter de círculo macizo (●) en lugar de un icono
    led_estado = ft.Text("●", size=18, color="grey")
    texto_estado = ft.Text("Iniciando conexión...", size=14, color="grey")
    panel_estado = ft.Row([led_estado, texto_estado])

    # Cabecera
    page.add(
        ft.Text("🚀 MERCADO EN DIRECTO PROGRAMADO POR RAUL.R", size=24, weight="bold"),
        panel_estado, 
        ft.Divider(height=20, color="white24")
    )

    empresas = ["NVDA", "GOOGL", "AAPL", "MSFT", "AMZN", "AVGO", "META", "TSLA", "BRK-B", "LLY"]
    filas_ui = {}
    
    lista_columna = ft.Column(spacing=15, scroll="auto")

    # Estructura visual inicial
    for simbolo in empresas:
        txt_simbolo = ft.Text(f"{simbolo}", size=18, weight="bold", width=80)
        txt_precio = ft.Text("Cargando...", size=18, width=120)
        txt_porcentaje = ft.Text("", size=18, weight="bold")

        fila = ft.Row([txt_simbolo, txt_precio, txt_porcentaje])
        lista_columna.controls.append(fila)

        filas_ui[simbolo] = {
            "precio": txt_precio, 
            "porcentaje": txt_porcentaje
        }

    page.add(lista_columna)

    def actualizar_datos_fondo():
        tickers_str = " ".join(empresas)
        
        while True:
            try:
                # 1. AVISO VISUAL: Empezando a descargar
                led_estado.color = "yellow"
                texto_estado.value = "Descargando datos..."
                page.update()
                
                # Descargamos los datos
                datos = yf.download(tickers_str, period="2d", progress=False)
                
                if len(datos) >= 2:
                    for simbolo in empresas:
                        try:
                            precio_hoy = float(datos['Close'][simbolo].iloc[1])
                            precio_ayer = float(datos['Close'][simbolo].iloc[0])
                            porcentaje = ((precio_hoy - precio_ayer) / precio_ayer) * 100
                            
                            filas_ui[simbolo]["precio"].value = f"${precio_hoy:.2f}"
                            
                            if porcentaje >= 0:
                                filas_ui[simbolo]["porcentaje"].value = f"▲ +{porcentaje:.2f}%"
                                filas_ui[simbolo]["porcentaje"].color = "green"
                            else:
                                filas_ui[simbolo]["porcentaje"].value = f"▼ {porcentaje:.2f}%"
                                filas_ui[simbolo]["porcentaje"].color = "red"
                                
                        except Exception as e:
                            pass 
                    
                    # 2. AVISO VISUAL: Terminado con éxito (Ponemos la hora exacta)
                    hora_actual = time.strftime("%H:%M:%S")
                    led_estado.color = "green"
                    texto_estado.value = f"Actualizado a las {hora_actual}"
                    page.update()
                    
            except Exception as e:
                # 3. AVISO VISUAL: Si falla la conexión a internet
                led_estado.color = "red"
                texto_estado.value = "Error de red. Reintentando..."
                page.update()
            
            # Pausa de 3 segundos
            time.sleep(3)

    threading.Thread(target=actualizar_datos_fondo, daemon=True).start()

ft.app(target=main)
# En lugar de solo: ft.app(target=main)
# Usa esto para que sea compatible con web:
if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER)