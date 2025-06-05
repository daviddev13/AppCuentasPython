import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

class SaveController:
    ventana_confirm = None
    ventana_save = None

    def __init__(self):
        print("Clase control save creada")
        # Variable para almacenar los datos
        self.datosCont = None
        self.urlCont = None
    
    def set_datos(self, datos, urlArchivo):
        """Guarda los datos en una variable"""
        self.datosCont = datos
        self.urlCont = urlArchivo
        print(f"Datos almacenados en Controller: {self.datosCont, self.urlCont}")
        
    def event_button_save_new(self, datos, urlArchivo): 
        """Guarda los datos en un archivo"""
        print("Saving Data")

        # Llamar a set_datos y verificar tipos 
        SaveController.set_datos(self, datos, urlArchivo) 
         
        print(f"Datos a guardar: {self.datosCont}") 
        print(f"Datos de url a guardar: {self.urlCont} (tipo: {type(self.urlCont)})") 
        # Verifica el tipo 
         
        #url_user = self.urlCont 
        url_user = f"{self.urlCont}"
        # Agregar comillas alrededor del valor
        datosfinal = f'"{self.datosCont}"' 

        if not isinstance(url_user, str): # Si no es una cadena, convertir o manejar el error 
            print(f"Error: url_user es de tipo {type(url_user)}, se esperaba str.") 
            return 
        if self.datosCont is None: 
            print("No hay datos para guardar") 
            return 
        try: 
            Guardar.guardar_en_archivo(datosfinal, url_user) 
            messagebox.showinfo("Guardado", "Datos guardados correctamente.") 
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar el archivo: {e}")

class Guardar:
    @staticmethod
    def guardar_en_archivo(datos, url):
        with open(url, 'w') as file:
            file.write(datos)
        print(f"Datos guardados en {url}")

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    
    # Instanciar el controlador
    controlador = SaveController()
    controlador.set_datos("Datos de prueba")
    
    # Simular el evento de guardar
    controlador.event_button_save_new()

    root.mainloop()

  
