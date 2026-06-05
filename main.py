import os
import flet as ft
import yfinance as yf
import time
import threading

def main(page: ft.Page):
    page.title = "Top 10 S&P 500 Programado por Raul.R"
    page.theme_mode = "dark"
    page.padding = 20
    # Ajustamos el tamaño para que sea responsivo en móvil
    page.window_width = 450
    page.window_height = 600

    # --- EL CHIVATO VISUAL ---
    led_estado = ft.Text("●", size=18, color="grey")
    texto_estado = ft.Text("Iniciando conexión...", size=14, color="grey")
    panel_estado = ft.Row([led_estado, texto_estado])

    # Cabecera
    page.add(
        ft.Text("🚀 SP500 TOP 10 Programado por Raul.R", size=24, weight="bold"),
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
                led_estado.color = "yellow"
                texto_estado.value = "Descargando..."
                page.update()
                
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
                        except:
                            pass 
                    
                    hora_actual = time.strftime("%H:%M:%S")
                    led_estado.color = "green"
                    texto_estado.value = f"Actualizado: {hora_actual}"
                    page.update()
            except:
                led_estado.color = "red"
                texto_estado.value = "Error de red."
                page.update()
            time.sleep(3)

    threading.Thread(target=actualizar_datos_fondo, daemon=True).start()

if __name__ == "__main__":
    # Railway inyecta el puerto en la variable de entorno PORT
    port = int(os.environ.get("PORT", 8080))
    ft.app(target=main, port=port, view=ft.AppView.WEB_BROWSER)
