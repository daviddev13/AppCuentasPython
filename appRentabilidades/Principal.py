import tkinter as tk
from tkinter import messagebox

from comunes.VistaConfirm import VistaConfirm  # Importar la clase desde el módulo
from .Calculadora import Calculadora
from comunes.VistaLoad import VistaLoad

class ApliRenta(tk.Frame):
#class VistaPrincipal:
    def __init__(self, master):
        super().__init__(master)  # Inicializa el Frame con master
        tk.Label(self, text="Hola desde App2").pack(pady=20)
        
        self.datos = {
            "Mes": "",
            "Inversion1" : "",
            "Inversion2" : "",
            "Inversion3" : "",
            "Inversion4" : "",
            "Inversion5" : "",
            "Inversion6" : "",
            "Inversion7" : "",
            "Inversion8" : "",
            "Inversion9" : "",
            "Inversion10" : "",
            "LugarInverison1" : "",
            "LugarInverison2" : "",
            "LugarInverison3": "",
            "LugarInverison4": "",
            "LugarInverison5" : "",
            "LugarInverison6": "",
            "LugarInverison7": "",
            "LugarInverison8" : "",
            "LugarInverison9": "",
            "LugarInverison10": "",
            "GananciaInv1": "",
            "GananciaInv2": "",
            "GananciaInv3": "",
            "GananciaInv4": "",
            "GananciaInv5": "",
            "GananciaInv6": "",
            "GananciaInv7": "",
            "GananciaInv8": "",
            "GananciaInv9": "",
            "GananciaInv10": "",
            "Proximo1" : "",
            "Proximo2" : "",
            "Proximo3": "",
            "Proximo4": "",
            "Proximo5" : "",
            "Proximo6": "",
            "Proximo7": "",
            "Proximo8" : "",
            "Proximo9": "",
            "Proximo10": "",
            "Obs1" : "",
            "Obs2" : "",
            "Obs3" : "",
            "Obs4" : "",
            "Obs5" : "",
            "Obs6" : "",
            "Obs7" : "",
            "Obs8" : "",
            "Obs9" : "",
            "Obs10" : "",
            "Inversor1": "",
            "ValorInversor1": "",
            "Inversor2": "",
            "ValorInversor2": "",
            "Inversor3": "",
            "ValorInversor3": "",
            "Inversor4": "",
            "ValorInversor4": ""
        }

        self.root = tk.Tk()

        # Titulo de la app
        self.root.title("Rentabilidades")

        # Barra de navegación
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        # Submenú "Archivo"
        app_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=app_menu)
        app_menu.add_command(label="Cargar Archivo", command=self.boton_load_save)

        # Diccionario para guardar los Entries antes de crearlos
        self.entries = {} 
        self.create_widgets()

        # instancia de load con callback
        self.vista_load = VistaLoad(master=self.root, callback=self.recibir_lineas)

        # Inicializa variable vacia
        self.url_user = ""
        self.lineas_recibidas = [] # Variable para almacenar las líneas
        
    def create_widgets(self):
        row = 1

        # Paquete de Mes
        self.create_entry(row, "Mes")
        row += 1

        # Paquete de Inversiones
        tk.Label(self.root, text="INVERSIONES").grid(row=row, column=0, columnspan=3)
        row += 1
        self.create_entries_triple(row, "Inversion1", "LugarInverison1","GananciaInv1", "Proximo1")
        row += 1
        self.create_entries_uno(row, "Obs1")
        row += 1
        self.create_entries_triple(row, "Inversion2", "LugarInverison2","GananciaInv2", "Proximo2")
        row += 1
        self.create_entries_uno(row, "Obs2")
        row += 1
        self.create_entries_triple(row, "Inversion3", "LugarInverison3","GananciaInv3", "Proximo3")
        row += 1
        self.create_entries_uno(row, "Obs3")
        row += 1
        self.create_entries_triple(row, "Inversion4", "LugarInverison4","GananciaInv4", "Proximo4")
        row += 1
        self.create_entries_uno(row, "Obs4")
        row += 1
        self.create_entries_triple(row, "Inversion5", "LugarInverison5","GananciaInv5", "Proximo5")
        row += 1
        self.create_entries_uno(row, "Obs5")
        row += 1
        self.create_entries_triple(row, "Inversion6", "LugarInverison6","GananciaInv6", "Proximo6")
        row += 1
        self.create_entries_uno(row, "Obs6")
        row += 1
        self.create_entries_triple(row, "Inversion7", "LugarInverison7","GananciaInv7", "Proximo7")
        row += 1
        self.create_entries_uno(row, "Obs7")
        row += 1
        self.create_entries_triple(row, "Inversion8", "LugarInverison8","GananciaInv8", "Proximo8")
        row += 1
        self.create_entries_uno(row, "Obs8")
        row += 1
        self.create_entries_triple(row, "Inversion9", "LugarInverison9","GananciaInv9", "Proximo9")
        row += 1
        self.create_entries_uno(row, "Obs9")
        row += 1
        self.create_entries_triple(row, "Inversion10", "LugarInverison10","GananciaInv10", "Proximo10")
        row += 1
        self.create_entries_uno(row, "Obs10")
        row += 1

        # Paquete de INVERSORES
        tk.Label(self.root, text="INVERSORES").grid(row=row, column=0, columnspan=3)
        row += 1
        self.create_entries_pair(row, "Inversor1", "ValorInversor1")
        row += 1
        self.create_entries_pair(row, "Inversor2", "ValorInversor2")
        row += 1
        self.create_entries_pair(row, "Inversor3", "ValorInversor3")
        row += 1
        self.create_entries_pair(row, "Inversor4", "ValorInversor4")
        row += 1

        confirm_button = tk.Button(self.root, text="Confirmar Datos", command=self.evento_boton_confirmar_datos)
        confirm_button.grid(row=row, column=0, columnspan=2, pady=10)
        row += 1
    
    def create_entries_uno(self, row, campo1, bg_color="#ffffff"):
        tk.Label(self.root, text=campo1, bg=bg_color).grid(row=row, column=0, sticky="w")
        entry1 = tk.Entry(self.root, bg=bg_color)
        entry1.insert(0, "0")
        entry1.grid(row=row, column=1, columnspan=6, sticky="we")
        self.entries[campo1] = entry1

    def create_entries_pair(self, row, label1, label2, bg_color="#ffffff"):
        tk.Label(self.root, text=label1, bg=bg_color).grid(row=row, column=0, sticky="w")
        entry1 = tk.Entry(self.root, bg=bg_color)
        entry1.insert(0, "0")
        entry1.grid(row=row, column=1, sticky="we")
        self.entries[label1] = entry1

        tk.Label(self.root, text=label2, bg=bg_color).grid(row=row, column=2, sticky="w")
        entry2 = tk.Entry(self.root, bg=bg_color)
        entry2.insert(0, "0")
        entry2.grid(row=row, column=3, sticky="we")
        self.entries[label2] = entry2
    
    def create_entries_triple(self, row, campo1, campo2, campo3, campo4):
        # Labels y entradas
        tk.Label(self.root, text=campo1).grid(row=row, column=0, sticky="w")
        entry1 = tk.Entry(self.root)
        entry1.insert(0, "0")
        entry1.grid(row=row, column=1, sticky="we")
        self.entries[campo1] = entry1

        tk.Label(self.root, text=campo2).grid(row=row, column=2, sticky="w")
        entry2 = tk.Entry(self.root)
        entry2.insert(0, "0")
        entry2.grid(row=row, column=3, sticky="we")
        self.entries[campo2] = entry2

        tk.Label(self.root, text=campo3).grid(row=row, column=4, sticky="w")
        entry3 = tk.Entry(self.root)
        entry3.insert(0, "0")
        entry3.grid(row=row, column=5, sticky="we")
        self.entries[campo3] = entry3

        tk.Label(self.root, text=campo4).grid(row=row, column=6, sticky="w")
        entry4 = tk.Entry(self.root, state="readonly")
        entry4.grid(row=row, column=7, sticky="we")
        self.entries[campo4] = entry4

        # Botón para sumar
        btn = tk.Button(self.root, text="Sumar", command=lambda: self.sumar_campos(campo1, campo3, campo4))
        btn.grid(row=row, column=8)

    def sumar_campos(self, campo1, campo3, campo_total):
        try:
            v1 = float(self.entries[campo1].get())
        except ValueError:
            v1 = 0
        try:
            v3 = float(self.entries[campo3].get())
        except ValueError:
            v3 = 0
        total = v1 + v3

        # Hacer editable temporalmente para modificar el campo de solo lectura
        entry_total = self.entries[campo_total]
        entry_total.config(state="normal")
        entry_total.delete(0, tk.END)
        entry_total.insert(0, f"{total:.2f}")
        entry_total.config(state="readonly")

    
    def create_entry(self, row, label):
        """Crea un Entry y lo guarda en el diccionario"""
        tk.Label(self.root, text=label).grid(row=row, column=0, sticky="w")
        entry = tk.Entry(self.root)
        entry.insert(0, "0")  # Establecer el valor inicial 0
        entry.grid(row=row, column=1, columnspan=3, sticky="we")
        self.entries[label] = entry  # Guardar el Entry en un diccionario

    def get_datos_window(self):
        for key in self.datos.keys():
            self.datos[key] = self.entries[key].get() if self.entries[key].get() else "vacio"
        print("Datos obtenidos:", self.datos)
        self.url_user = self.datos
        print("Datos:", self.url_user)

    def evento_boton_confirmar_datos(self):
        print("Clicked Confirmar Datos")
        self.get_datos_window()
        # calcular TOTAL
        # Instanciar la clase Calculadora
        calculadora = Calculadora()
        # print(self.datos['Efectivo actual'])
         
        # Llamar al método calcular
        totales1 = calculadora.calcular(self.datos['Inversion1'], 
                                    self.datos['Inversion2'], 
                                    self.datos['Inversion3'], 
                                    self.datos['Inversion4'], 
                                    self.datos['Inversion5'], 
                                    self.datos['Inversion6'], 
                                    self.datos['Inversion7'], 
                                    self.datos['Inversion8'], 
                                    self.datos['Inversion9'], 
                                    self.datos['Inversion10'], 
                                    self.datos['GananciaInv1'],
                                    self.datos['GananciaInv2'],
                                    self.datos['GananciaInv3'],
                                    self.datos['GananciaInv4'],
                                    self.datos['GananciaInv5'],
                                    self.datos['GananciaInv6'],
                                    self.datos['GananciaInv7'],
                                    self.datos['GananciaInv8'],
                                    self.datos['GananciaInv9'],
                                    self.datos['GananciaInv10'],
                                    self.datos['ValorInversor1'],
                                    self.datos['ValorInversor2'],
                                    self.datos['ValorInversor3'],
                                    self.datos['ValorInversor4']
                                    )

        # Llamar al método patrimonio
        # patrimonio = calculadora.patrimonio(str_total_ac, self.datos['Deudas?'])

        # Mostrar el resultado 
        print(f"Totalgan: {totales1}")

        # # Preparar los datos
        Datos = f"""
        Mes: {self.datos['Mes']}
        ******************************* 
        Inversion1: {self.datos['Inversion1']}
        Lugar1: {self.datos['LugarInverison1']}
        Ganancia1: {self.datos['GananciaInv1']}
        Proximo1: {self.datos['Proximo1']}
        Observaciones1: {self.datos['Obs1']}
        ******************************* 
        Inversion2: {self.datos['Inversion2']}
        Lugar2: {self.datos['LugarInverison2']}
        Ganancia2: {self.datos['GananciaInv2']}
        Proximo2: {self.datos['Proximo2']}
        Observaciones2: {self.datos['Obs2']}
        ****************************** 
        Inversion3: {self.datos['Inversion3']}
        Lugar3: {self.datos['LugarInverison3']}
        Ganancia3: {self.datos['GananciaInv3']}
        Proximo3: {self.datos['Proximo3']}
        Observaciones3: {self.datos['Obs3']}       
        ******************************* 
        Inversion4: {self.datos['Inversion4']}
        Lugar4: {self.datos['LugarInverison4']}
        Ganancia4: {self.datos['GananciaInv4']}
        Proximo4: {self.datos['Proximo4']}
        Observaciones4: {self.datos['Obs4']} 
        ******************************* 
        Inversion5: {self.datos['Inversion5']}
        Lugar5: {self.datos['LugarInverison5']}
        Ganancia5: {self.datos['GananciaInv5']}
        Proximo5: {self.datos['Proximo5']}
        Observaciones5: {self.datos['Obs5']}
        ****************************** 
        Inversion6: {self.datos['Inversion6']}
        Lugar6: {self.datos['LugarInverison6']}
        Ganancia6: {self.datos['GananciaInv6']}
        Proximo6: {self.datos['Proximo6']}
        Observaciones6: {self.datos['Obs6']}       
        ******************************* 
        Inversion7: {self.datos['Inversion7']}
        Lugar7: {self.datos['LugarInverison7']}
        Ganancia7: {self.datos['GananciaInv7']}
        Proximo7: {self.datos['Proximo7']}
        Observaciones7: {self.datos['Obs7']} 
        ******************************* 
        Inversion8: {self.datos['Inversion8']}
        Lugar8: {self.datos['LugarInverison8']}
        Ganancia8: {self.datos['GananciaInv8']}
        Proximo8: {self.datos['Proximo8']}
        Observaciones8: {self.datos['Obs8']} 
        ******************************* 
        Inversion9: {self.datos['Inversion9']}
        Lugar9: {self.datos['LugarInverison9']}
        Ganancia9: {self.datos['GananciaInv9']}
        Proximo9: {self.datos['Proximo9']}
        Observaciones9: {self.datos['Obs9']} 
        ******************************* 
        Inversion10: {self.datos['Inversion10']}
        Lugar10: {self.datos['LugarInverison10']}
        Ganancia10: {self.datos['GananciaInv10']}
        Proximo10: {self.datos['Proximo10']}
        Observaciones10: {self.datos['Obs10']} 
        ******************************* 
        Total Invertido: {totales1[0]}
        Total Ganancia: {totales1[1]}
        ******************************* 
        {self.datos['Inversor1']}
        Inversion {self.datos['Inversor1']}: {self.datos['ValorInversor1']}
        Porcentaje {self.datos['Inversor1']}: {totales1[2]}
        Ganancia {self.datos['Inversor1']}: {totales1[3]}
        {self.datos['Inversor2']}
        Inversion {self.datos['Inversor2']}: {self.datos['ValorInversor2']}
        Porcentaje {self.datos['Inversor2']}: {totales1[4]}
        Ganancia {self.datos['Inversor2']}: {totales1[5]}
        {self.datos['Inversor3']}
        Inversion {self.datos['Inversor3']}: {self.datos['ValorInversor3']}
        Porcentaje {self.datos['Inversor3']}: {totales1[6]}
        Ganancia {self.datos['Inversor3']}: {totales1[7]}
        {self.datos['Inversor4']}
        Inversion {self.datos['Inversor4']}: {self.datos['ValorInversor4']}
        Porcentaje {self.datos['Inversor4']}: {totales1[8]}
        Ganancia {self.datos['Inversor4']}: {totales1[9]}
        """
        # clic “Confirmar” crea nueva ventana totalmente nueva sin instancia.
        ventana = VistaConfirm(self.root)
        ventana.set_label2_text(Datos)
        ventana.mostrar()

    def boton_load_save(self):
        print("Load Save clicked!")
        # Hace visible ventana de carga
        # antes de mostrar ventana, verifica si sigue existiendo:
        try:
            if not self.vista_load or not self.vista_load.winfo_exists():
                self.vista_load = VistaLoad(self)
            self.vista_load.mostrar()
        except Exception as e:
            print("Error al cargar la vista de archivo:", e)
    
    def recibir_lineas(self, lineas):
        print("Líneas recibidas desde VistaLoad:")
        #for linea in lineas: 
        self.lineas_recibidas = lineas
        # Diccionario: clave = label del Entry, valor = índice en self.lineas_recibidas
        mapa_actualizacion = {
            "Mes": 1,   

            "Inversion1" : 3,
            "LugarInverison1" : 4,
            "GananciaInv1": 5,
            
            "Obs1":7,

            "Inversion2" : 9,
            "LugarInverison2" : 10,
            "GananciaInv2": 11,
            
            "Obs2":13,

            "Inversion3" : 15,
            "LugarInverison3": 16,
            "GananciaInv3": 17,

            "Obs3":19,

            "Inversion4" : 21,
            "LugarInverison4": 22,
            "GananciaInv4": 23,

            "Obs4":25,

            "Inversion5" : 27,
            "LugarInverison5" : 28,
            "GananciaInv5": 29,

            "Obs5":31,

            "Inversion6" : 33,
            "LugarInverison6": 34,
            "GananciaInv6": 35,

            "Obs6":37,

            "Inversion7" : 39,
            "LugarInverison7": 40,
            "GananciaInv7": 41,

            "Obs7":43,

            "Inversion8" : 45,
            "LugarInverison8" : 46,
            "GananciaInv8": 47,

            "Obs8":49,

            "Inversion9" : 51,
            "LugarInverison9": 52,
            "GananciaInv9": 53,

            "Obs9":55,

            "Inversion10" : 57,
            "LugarInverison10": 58,
            "GananciaInv10": 59,

            "Obs10":61,

            "Inversor1": 66,
            "ValorInversor1": 67,
            "Inversor2": 70,
            "ValorInversor2": 71,
            "Inversor3": 74,
            "ValorInversor3": 75,
            "Inversor4": 78,
            "ValorInversor4": 79
        }
        # Recorres el diccionario y actualizas cada entrada
        for label, posicion in mapa_actualizacion.items():
            # Llama a una función para mostrar los datos
            self.actualizar_interfaz(label, posicion)
        #self.actualizar_interfaz(mi_label, posicion) 
        
    def actualizar_interfaz(self, label, posicion):
        #print( self.lineas_recibidas[posicion])
        #print(f"Claves en self.entries: {list(self.entries.keys())}")

        # entries iguales o menores a datos recibidos
        if posicion >= len(self.lineas_recibidas):
            print(f"Posición {posicion} fuera de rango en lineas_recibidas")
            return

        linea = self.lineas_recibidas[posicion]
        #print(f"Línea recibida: {linea}")

        #si tiene puntos tomar despues de puntos
        if ":" in linea:
            valor = linea.split(":")[1].strip()
        else:
            valor = linea.strip()

        # Verificar si el Entry existe en el diccionario
        if label in self.entries:
            entry = self.entries[label]
            entry.delete(0, tk.END)# Borrar el contenido actual
            entry.insert(0, valor)# Insertar el nuevo valor
            #print(f"Actualizado Entry '{label}' con el valor: {valor}")
        else:
            print(f"Error: No se encontró el Entry con el label '{label}'.")
   
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = VistaPrincipal()
    app.run()