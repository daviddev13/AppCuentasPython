import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from .SaveController import SaveController  # Importar la clase desde el módulo

class VistaSave(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)  # Usar el constructor de Toplevel    
        print("Clase vista save creada")
        self.title("Guardar")
        self.geometry("400x200") 
        
        # Ocultar la ventana secundaria hasta que sea necesario
        self.withdraw() 

        # Variable para almacenar los datos
        self.datos = None
        self.urlArchivo = None

        # Widgets de la ventana
        self.entry = tk.Entry(self, width=40)
        self.entry.pack(pady=10)

        self.button = tk.Button(self, text="Seleccionar Archivo", command=self.buscar_archivo)
        self.button.pack(pady=5)

        self.button1 = tk.Button(self, text="Guardar", command=self.guardar_datos)
        self.button1.pack(pady=5)
        
        self.save_controller = SaveController() 

    def set_datos(self, data):
        """Guarda los datos en una variable"""
        self.datos = data
        texto_entry = self.get_entry_text()
        print(f"Texto en entry antes de asignar: '{texto_entry}'")  # Verifica si está vacío
        self.urlArchivo = texto_entry
        print(f"Datos almacenados en VistaSave: {self.datos, self.urlArchivo}")

    def mostrar(self):
        """Hace visible la ventana"""
        self.deiconify()  
    
    def ocultar(self):
        """Oculta la ventana sin cerrarla"""
        self.withdraw()  

    def buscar_archivo(self):
        archivo = filedialog.asksaveasfilename(title="Seleccionar archivo para guardar")
        if archivo:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, archivo)
            print("Está agarrando URL:", self.get_entry_text())  # Verifica si la URL se está asignando correctamente
            self.set_datos(self.datos)  # Llamar correctamente a set_datos con el argumento

    def guardar_datos(self):
        self.save_controller.url_user = self.get_entry_text()  
        self.save_controller.event_button_save_new(self.datos, self.urlArchivo)
        self.ocultar()  # Oculta la ventana luego de cargar

    def get_entry_text(self):
        return self.entry.get()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana raíz principal (opcional)
    
    app = VistaSave()  # Crear instancia de VistaSave
    app.mostrar()  # Mostrar la ventana secundaria (opcional para pruebas)
    
    root.mainloop()
