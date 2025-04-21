import tkinter as tk
from tkinter import messagebox

from VistaConfirm import VistaConfirm  # Importar la clase desde el módulo
from Calculadora import Calculadora
from VistaLoad import VistaLoad

class VistaPrincipal:
    def __init__(self): 
        
        self.datos = {
            "Numero de Mes": "", "Efectivo actual": "", "Obs Efect": "",
            "Cuenta de ahorro 1 actual": "", "Cuenta de ahorro 2 actual": "", 
            "Cuenta de ahorro 3 actual": "", "Consignaciones Mes CA1": "", 
            "Consignaciones Mes CA2": "", "Consignaciones Mes CA3": "",
            "Obs Cuentas de ahorro": "", "Acumulado Consignaciones": "", 
            "Otra moneda": "", "Obs OMon": "", "Apertura inversiones en el mes": "",
            "Inversion 1?": "", "Obs Inv1": "", "Inversion 2?": "", "Obs Inv 2": "",
            "Acumulado Inversiones": "", 
            "Compras?": "", "Obs Compras": "", "Gastos?": "", "Obs Gastos": "",
            "Deudas?": "", "Obs Deudas": "", "Entidades manejadas en mes?": "",
            "Observaciones Adicionales": ""
        }
        self.root = tk.Tk()
        self.root.title("Vista Principal")
        cargar_button = tk.Button(self.root, text="Cargar Archivo", command=self.boton_load_save)
        cargar_button.grid(row=0, column=0, columnspan=2, pady=10)
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
        self.create_entry(row, "Numero de Mes")
        row += 1
        
        # Paquete de Efectivo
        tk.Label(self.root, text="Efectivo").grid(row=row, column=0, columnspan=2)
        row += 1
        self.create_entries_pair(row, "Efectivo actual", "Obs Efect")
        row += 1
        
        # Paquete de Cuentas de Ahorro
        tk.Label(self.root, text="Cuentas de Ahorro").grid(row=row, column=0, columnspan=3)
        row += 1
        self.create_entries_triple(row, "Cuenta de ahorro 1 actual", "Cuenta de ahorro 2 actual", "Cuenta de ahorro 3 actual")
        row += 1
        self.create_entries_triple(row, "Consignaciones Mes CA1", "Consignaciones Mes CA2", "Consignaciones Mes CA3")
        row += 1
        self.create_entry(row, "Obs Cuentas de ahorro")
        row += 1
        self.create_entry(row, "Acumulado Consignaciones")
        row += 1
        
        # Paquete de Inversiones
        tk.Label(self.root, text="Inversiones").grid(row=row, column=0, columnspan=2)
        row += 1
        self.create_entries_pair(row, "Otra moneda", "Obs OMon")
        row += 1
        self.create_entry(row, "Apertura inversiones en el mes")
        row += 1
        self.create_entries_pair(row, "Inversion 1?", "Obs Inv1")
        row += 1
        self.create_entries_pair(row, "Inversion 2?", "Obs Inv 2")
        row += 1
        self.create_entry(row, "Acumulado Inversiones")
        row += 1
        
        # Paquete de Gastos
        tk.Label(self.root, text="Gastos").grid(row=row, column=0, columnspan=2)
        row += 1
        self.create_entries_pair(row, "Compras?", "Obs Compras")
        row += 1
        self.create_entries_pair(row, "Gastos?", "Obs Gastos")
        row += 1
        self.create_entries_pair(row, "Deudas?", "Obs Deudas")
        row += 1
        
        # Paquete de Entidades y Observaciones
        self.create_entry(row, "Entidades manejadas en mes?")
        row += 1
        self.create_entry(row, "Observaciones Adicionales")
        row += 1

        # Paquete de suma de consignaciones
        tk.Label(self.root, text="Suma de Consignaciones:").grid(row=row, column=0, sticky="w")
        self.label_resultado_suma_consig = tk.Label(self.root, text="0")
        self.label_resultado_suma_consig.grid(row=row, column=1, sticky="w")
        row += 1
        
        confirm_button = tk.Button(self.root, text="Confirmar Datos", command=self.evento_boton_confirmar_datos)
        confirm_button.grid(row=row, column=0, columnspan=2, pady=10)
        row += 1

        suma_consig_button = tk.Button(self.root, text="Suma de Consignaciones", command=self.boton_calcular_consignacionesxmes)
        suma_consig_button.grid(row=row, column=0, columnspan=2, pady=10)
        row += 1
    
    def create_entries_pair(self, row, label1, label2):
        tk.Label(self.root, text=label1).grid(row=row, column=0, sticky="w")
        entry1 = tk.Entry(self.root)
        entry1.insert(0, "0")  # Establecer el valor inicial 0
        entry1.grid(row=row, column=1, sticky="we")
        self.entries[label1] = entry1
        
        tk.Label(self.root, text=label2).grid(row=row, column=2, sticky="w")
        entry2 = tk.Entry(self.root)
        entry2.insert(0, "0")  # Establecer el valor inicial 0
        entry2.grid(row=row, column=3, sticky="we")
        self.entries[label2] = entry2
    
    def create_entries_triple(self, row, label1, label2, label3):
        tk.Label(self.root, text=label1).grid(row=row, column=0, sticky="w")
        entry1 = tk.Entry(self.root)
        entry1.insert(0, "0")  # Establecer el valor inicial 0
        entry1.grid(row=row, column=1, sticky="we")
        self.entries[label1] = entry1
        
        tk.Label(self.root, text=label2).grid(row=row, column=2, sticky="w")
        entry2 = tk.Entry(self.root)
        entry2.insert(0, "0")  # Establecer el valor inicial 0
        entry2.grid(row=row, column=3, sticky="we")
        self.entries[label2] = entry2
        
        tk.Label(self.root, text=label3).grid(row=row, column=4, sticky="w")
        entry3 = tk.Entry(self.root)
        entry3.insert(0, "0")  # Establecer el valor inicial 0
        entry3.grid(row=row, column=5, sticky="we")
        self.entries[label3] = entry3
    
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
        #print("Datos obtenidos:", self.datos)
        self.url_user = self.datos
        print("Datos:", self.url_user)

    def boton_calcular_consignacionesxmes(self):
        print("Clicked Suma de consignacionesXmes")
        self.get_datos_window()

        # Instanciar la clase Calculadora
        calculadora = Calculadora()
        print(self.datos['Consignaciones Mes CA1'])

        # Calcular la suma
        sumaConsig = calculadora.sumaConsig(
            self.datos['Consignaciones Mes CA1'],
            self.datos['Consignaciones Mes CA2'],
            self.datos['Consignaciones Mes CA3']
        )

        print(f"Resultado: {sumaConsig}")

        # Mostrar el resultado en la ventana
        self.label_resultado_suma_consig.config(text=f"Suma: {sumaConsig}")

    def evento_boton_confirmar_datos(self):
        print("Clicked Confirmar Datos")
        self.get_datos_window()
        # calcular patrimonio y activos 
        # Instanciar la clase Calculadora
        calculadora = Calculadora()
        print(self.datos['Efectivo actual'])
         
        # Llamar al método activos
        activos = calculadora.activos(self.datos['Efectivo actual'], 
                                    self.datos['Cuenta de ahorro 1 actual'], 
                                    self.datos['Cuenta de ahorro 2 actual'], 
                                    self.datos['Cuenta de ahorro 3 actual'], 
                                    self.datos['Inversion 1?'], 
                                    self.datos['Inversion 2?'], 
                                    self.datos['Otra moneda'])

        # Convertir el resultado a string (opcional en Python)
        str_total_ac = str(activos)

        # Llamar al método patrimonio
        patrimonio = calculadora.patrimonio(str_total_ac, self.datos['Deudas?'])

        # Mostrar el resultado (equivalente a System.out.println)
        print(f"Resultado: {activos}")
        print(f"Patrimonio: {patrimonio}") 
        

        # # Preparar los datos
        Datos = f"""
        Mes: {self.datos['Numero de Mes']} 
        ******************************* 
        Efectivo: {self.datos['Efectivo actual']}
        ObsEfectivo: {self.datos['Obs Efect']}
        ******************************* 
        Cuenta de ahorro: {self.datos['Cuenta de ahorro 1 actual']}
        Cuenta de ahorro2: {self.datos['Cuenta de ahorro 2 actual']} 
        Cuenta de ahorro3: {self.datos['Cuenta de ahorro 3 actual']} 
        ConsignacionesXMesC1: {self.datos['Consignaciones Mes CA1']}
        ConsignacionesXMesC2: {self.datos['Consignaciones Mes CA2']}
        ConsignacionesXMesC3: {self.datos['Consignaciones Mes CA3']}
        ObsCuentaAhorro: {self.datos['Obs Cuentas de ahorro']}
        ******************************* 
        Otra Moneda: {self.datos['Otra moneda']}
        ObsOM: {self.datos['Obs OMon']}
        ******************************* 
        AperturaInversiones: {self.datos['Apertura inversiones en el mes']}
        Inversion: {self.datos['Inversion 1?']}
        ObsInv1: {self.datos['Obs Inv1']}
        Inversion2: {self.datos['Inversion 2?']}
        ObsInv2: {self.datos['Obs Inv 2']}
        ******************************* 
        Compras: {self.datos['Compras?']}
        ObsCompra: {self.datos['Obs Compras']}
        Gastos: {self.datos['Gastos?']}
        ObsGastos: {self.datos['Obs Gastos']}
        Deudas: {self.datos['Deudas?']} 
        ObsDeudas: {self.datos['Obs Deudas']}
        ******************************* 
        Activos: {activos}
        Pasivos: {self.datos['Deudas?']}
        Patrimonio: {patrimonio}
        ******************************* 
        AcumConsignaciones: {self.datos['Acumulado Consignaciones']}
        AcumInversiones: {self.datos['Acumulado Inversiones']}
        Observaciones: {self.datos['Observaciones Adicionales']}
        Entidades: {self.datos['Entidades manejadas en mes?']}
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
            "Numero de Mes": 1,
            "Efectivo actual": 3, 
            "Obs Efect": 4,
            "Cuenta de ahorro 1 actual": 6, 
            "Cuenta de ahorro 2 actual": 7, 
            "Cuenta de ahorro 3 actual": 8, 
            "Consignaciones Mes CA1": 9, 
            "Consignaciones Mes CA2": 10, 
            "Consignaciones Mes CA3": 11,
            "Obs Cuentas de ahorro": 12,
            "Acumulado Consignaciones": 34, 
            "Otra moneda": 14,
            "Obs OMon": 15,
            "Apertura inversiones en el mes": 17,
            "Inversion 1?": 18,
            "Obs Inv1": 19,
            "Inversion 2?": 20,
            "Obs Inv 2": 21,
            "Acumulado Inversiones": 35, 
            "Compras?": 23,
            "Obs Compras": 24,
            "Gastos?": 25,
            "Obs Gastos": 26,
            "Deudas?": 27,
            "Obs Deudas": 28,
            "Entidades manejadas en mes?": 37,
            "Observaciones Adicionales": 36
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


# messagebox.showinfo("Confirmación", "Datos confirmados correctamente")

        # Si tienes otro método como AcumuladoConsig
        #acum = calculadora.acumulado_consig(ConsigxMes, ConsigC2xMes)

        # Y si también tienes AcumuladoInver
        # acum2 = calculadora.acumulado_inver(ApertInv)
            #print(f"Acumulado Consignaciones: {acum}")

#metodo ventana con instancias
 # Crear una instancia de VistaConfirm (asumiendo que ya tienes esta clase)
        #self.vista_confirm = VistaConfirm() 
# Comprobar si la ventana fue cerrada o no existe
        #if self.vista_confirm is None or not self.vista_confirm.winfo_exists():
         #   from VistaConfirm import VistaConfirm  # o importa al inicio
          #  self.vista_confirm = VistaConfirm(self.root)  # reemplaza 'self.root' por tu ventana principal si tiene otro nombre
        # Lleva datos a vista confirm 
        #self.vista_confirm.set_label2_text(Datos)  
        # Hace visible ventana confirmacion
        #self.vista_confirm.mostrar()