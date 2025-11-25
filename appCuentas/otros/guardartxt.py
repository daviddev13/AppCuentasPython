import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

class Guardar:
    @staticmethod
    def guardar_en_archivo(datos, url):
        with open(url, 'w') as file:
            file.write(datos)
        print(f"Datos guardados en {url}")

class Save:
    datos_prueba = "Esto es un texto de prueba para guardar en el archivo."
    url_prueba = "/home/fercho/Escritorio/appcuentasPython/77888.txt"
    try: 
        Guardar.guardar_en_archivo(datos_prueba, url_prueba) 
        messagebox.showinfo("Guardado", "Datos guardados correctamente.") 
    except Exception as e:
        messagebox.showerror("Error", f"Error al guardar el archivo: {e}")


if __name__ == "__main__":
    app.run()

  
