import tkinter as tk
from tkinter import messagebox
from VistaConfirm import VistaConfirm  # Importar la clase desde el módulo

class VistaPrincipal:
    def __init__(self):
        self.datos = {
            "Mes": "", "Efectivo": "", "Cahorro": "", "Cahorro2": "",
            "Cahorro3": "", "OtraMoneda": "", "Prestamo": "", "Prestamo2": "",
            "Consumos": "", "Gastos": "", "Deudas": "", "Entidades": "", "Obser": "",
            "ObsEfect": "", "ConsigxMes": "", "ConsigC2xMes": "", "ConsigC3xMes": "",
            "AcumCons": "", "AcumInv": "", "ApertInv": "", "ObsCuentaAhorro": "",
            "ObOM": "", "ob_inv1": "", "ob_inv2": "", "ob_compra": "",
            "ob_gastos": "", "Ob_deudas": "", "UrlUser": ""
        }
        self.root = tk.Tk()
        self.root.title("Vista Principal")
        self.root.geometry("400x300")
        self.create_widgets()

        # Crear una instancia de VistaConfirm
        self.vista_confirm = VistaConfirm() 
        # Inicializa variable vacia
        self.url_user = ""
    
    def create_widgets(self):
        self.entries = {}
        row = 0
        for key in self.datos.keys():
            tk.Label(self.root, text=key).grid(row=row, column=0)
            entry = tk.Entry(self.root)
            entry.grid(row=row, column=1)
            self.entries[key] = entry
            row += 1
        
        confirm_button = tk.Button(self.root, text="Confirmar Datos", command=self.evento_boton_confirmar_datos)
        confirm_button.grid(row=row, column=0, columnspan=2)

    def get_datos_window(self):
        for key in self.datos.keys():
            self.datos[key] = self.entries[key].get() if self.entries[key].get() else "vacio"
        #print("Datos obtenidos:", self.datos)
        self.url_user = self.datos
        print("Datos:", self.url_user)
  
    def evento_boton_confirmar_datos(self):
        self.get_datos_window()
        # messagebox.showinfo("Confirmación", "Datos confirmados correctamente")
        # Lleva datos a vista confirm 
        self.vista_confirm.set_label2_text(self.url_user)  
        # Hace visible la ventana
        self.vista_confirm.mostrar()  

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = PrincipalController()
    app.run()
