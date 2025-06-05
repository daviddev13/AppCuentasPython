import tkinter as tk
from tkinter import ttk
from appCuentas.Principal import ApliCuentas
from appRentabilidades.Principal import ApliRenta

class AppPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Aplicación XXXX")
        self.geometry("500x200")

        # Contenedor para los botones y mensajes
        self.barra_botones = ttk.Frame(self)
        self.barra_botones.pack(side="top", fill="x", pady=10)

        # Frame primera aplicación
        frame_app1 = ttk.Frame(self.barra_botones)
        frame_app1.pack(side="top", fill="x", pady=5)

        label_app1 = tk.Label(frame_app1, text="1. Aplicación para llevar cuenta del patrimonio", font=("Arial", 10))
        label_app1.pack()

        #Boton Aplicacion1
        app1_button = tk.Button(self.barra_botones, text="Aplicacion Cuentas", command=self.cargar_app1)
        app1_button.pack(pady=5)

        # Frame egunda aplicación
        frame_app2 = ttk.Frame(self.barra_botones)
        frame_app2.pack(side="top", fill="x", pady=5)

        label_app2 = tk.Label(frame_app2, text="2. Aplicación para calcular rentabilidades mes a mes", font=("Arial", 10))
        label_app2.pack()

        #Boton Aplicacion2
        app1_button = tk.Button(self.barra_botones, text="Aplicacion Rentabilidades", command=self.cargar_app2)
        app1_button.pack(pady=5)

        # Contenedor para mostrar apps
        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.app_actual = None
        # self.cargar_app1()  # Por defecto se carga App1

        # ⬇️ Aquí colocas el mensaje inicial
        self.placeholder = tk.Label(
            self.container,
            text="Selecciona una aplicación desde el menú",
            font=("Arial", 14)
        )
        self.placeholder.pack(expand=True)

    def cargar_app1(self):
        self._limpiar_actual()
        self.app_actual = ApliCuentas(self.container)
        self.app_actual.pack(fill="both", expand=True)

    def cargar_app2(self):
        self._limpiar_actual()
        self.app_actual = ApliRenta(self.container)
        self.app_actual.pack(fill="both", expand=True)

    def _limpiar_actual(self):
        if self.app_actual:
            self.app_actual.destroy()
            self.app_actual = None
        if hasattr(self, 'placeholder') and self.placeholder.winfo_exists():
            self.placeholder.destroy()
if __name__ == "__main__":
    app = AppPrincipal()
    app.mainloop()
