import tkinter as tk
from tkinter import messagebox
from .VistaSave import VistaSave  # Importar la clase desde el módulo

#ventana hija toplevel
class VistaConfirm(tk.Toplevel):
    def __init__(self, master): 
        # Usar el constructor de Toplevel crear ventana como hija de master o principal
        super().__init__(master) 
        print("Clase VistaConfirm creada")
        self.title("Confirmar Datos")
        self.geometry("800x900")
        
        # Ocultar la ventana secundaria hasta que sea necesario
        self.withdraw()

        # -------- CONTENEDOR PRINCIPAL con CANVAS + SCROLLBAR --------
        contenedor = tk.Frame(self)
        contenedor.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(contenedor)
        self.canvas.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(contenedor, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Frame interno donde pondrás los widgets
        self.interior = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.interior, anchor="nw")

        # Importante: actualizar el scroll cuando se agreguen widgets
        self.interior.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # -------------------- TUS WIDGETS AQUÍ --------------------
        self.label2 = tk.Label(self.interior, text="", wraplength=800, font=("Arial", 12))
        self.label2.pack(pady=20)
        
        self.button1 = tk.Button(self.interior, text="Guardar Datos", command=self.on_button_click)
        self.button1.pack(pady=10)

        # Crear una instancia de VistaSave
        self.vista_save = VistaSave() 
        # Inicializa variable vacia
        self.datosConfrimados = ""
    
    def set_label2_text(self, data):
        """Actualiza el texto del label"""
        self.label2.config(text=f"Datos confirmados: {data}")
        self.datosConfrimados = data

    def mostrar(self):
        """Hace visible la ventana"""
        self.deiconify()  # Mostrar la ventana secundaria
    
    def ocultar(self):
        """Oculta la ventana sin cerrarla"""
        self.withdraw()  # Oculta la ventana
    
    def on_button_click(self):
        print("Botón Guardar Datos presionado")
        self.vista_save.set_datos(self.datosConfrimados)  # Enviar datos a VistaSave y almacenarlos en la variable
        self.vista_save.mostrar()  # Mostrar la ventana de guardar
        self.ocultar()  # Oculta la ventana luego de cargar

if __name__ == "__main__":
    root = tk.Tk()
    #root.withdraw()  # Oculta la ventana raíz principal (opcional)
    
    app = VistaConfirm()  # Crear instancia de VistaConfirm
    #app.mostrar()  # Mostrar la ventana secundaria (opcional para pruebas)
    
    root.mainloop()
