import tkinter as tk
import os
from tkinter import messagebox
from tkinter import filedialog

class VistaLoad(tk.Toplevel):
    def __init__(self, master=None, callback=None):
        super().__init__(master)  # Usar el constructor de Toplevel    
        print("Clase vista load creada")
        self.title("Cargar Archivo .txt")
        self.geometry("400x200") 
        
        # función de retorno
        self.callback = callback  
        
        # Ocultar la ventana secundaria hasta que sea necesario
        self.withdraw() 

        # Variable para almacenar los datos
        self.datos = None
        self.urlArchivo = None

        # Widgets de la ventana
        self.entry = tk.Entry(self, width=40)
        self.entry.pack(pady=10)

        self.button2 = tk.Button(self, text="Buscar", command=self.buscar_url_archivo)
        self.button2.pack(pady=5)

        self.button1 = tk.Button(self, text="Cargar", command=self.get_archivo)
        self.button1.pack(pady=5)

    def mostrar(self):
        """Hace visible la ventana"""
        self.deiconify()  
    
    def ocultar(self):
        """Oculta la ventana sin cerrarla"""
        self.withdraw()  

    def buscar_url_archivo(self):
        print("Buscando archivo...")
        ruta_archivo = filedialog.askopenfilename(
        title="Seleccionar archivo .txt",
        filetypes=(("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*"))
        )
        if ruta_archivo:
            self.entry.delete(0, tk.END)         # Limpia el campo
            self.entry.insert(0, ruta_archivo)   # Inserta la ruta del archivo
            self.urlArchivo = ruta_archivo       # Guarda la URL si la necesitas
            print("Archivo seleccionado:", ruta_archivo)

    def get_archivo(self):   
        url = self.get_entry_text()  # Corrección aquí
        print("URL:", url)
        lineas = []
        try:
            with open(url, "r", encoding="utf-8") as reader:
                for linea in reader:
                    lineas.append(linea.strip())
            if self.callback:
                self.callback(lineas)  # Llama a la función del principal
                self.withdraw()  # Oculta la ventana luego de cargar
        except IOError:
            messagebox.showerror("Error", "Error al obtener archivo")
        # print("Agarrando txt desde vistaLoad:", lineas)
        return lineas 

    def get_entry_text(self):
        return self.entry.get()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana raíz principal (opcional)
    
    app = VistaLoad()  # Crear instancia de VistaSave
    app.mostrar()  # Mostrar la ventana secundaria (opcional para pruebas)
    
    root.mainloop()