import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from comunes.VistaConfirm import VistaConfirm  # Importar la clase desde el módulo
from .Calculadora import Calculadora
from comunes.VistaLoad import VistaLoad

#class VistaPrincipal:
class ApliCuentas(tk.Frame):
    def __init__(self, master):
        super().__init__(master)  # Inicializa el Frame con master

        #anuncio en ventana inicial no tiene root
        #tk.Label(self, text="Hola desde App1").pack(pady=20)
        
        self.datos = {
            "Mes": "", "Efectivo actual": "", "Obs Efect": "",
            "Nombre Cuenta de ahorro 1": "", "Nombre Cuenta de ahorro 2": "", "Nombre Cuenta de ahorro 3": "","Nombre Cuenta de ahorro 4": "",
            "Valor Actual Cuenta1": "", "Valor Actual Cuenta2": "", "Valor Actual Cuenta3": "", "Valor Actual Cuenta4": "",
            "Consignaciones Mes CA1": "", "Consignaciones Mes CA2": "", "Consignaciones Mes CA3": "", "Consignaciones Mes CA4": "",
            "Suma ConsignacionesXMes": "","Obs Cuentas de ahorro": "", "Acumulado Consignaciones": "", 
            "Otra moneda": "", "Obs OMon": "", "Apertura inversiones en Mes": "",
            "Inversion 1?": "", "Entidad 1?": "", "Obs Inv1": "", 
            "Inversion 2?": "", "Entidad 2?": "", "Obs Inv2": "",
            "Inversion 3?": "", "Entidad 3?": "", "Obs Inv3": "", 
            "Inversion 4?": "", "Entidad 4?": "", "Obs Inv4": "",
            "Acumulado Inversiones": "", 
            "Compras?": "", "Obs Compras": "", "Gastos?": "", "Obs Gastos": "",
            "Prestamo1": "", "Prestamo2": "", "Prestamo3": "",
            "Total Prestamos": "", "Obs Prestamos": "", "Acum Consigna+Inversiones": "",
            "Observaciones Adicionales": ""
        }
        self.root = tk.Tk()

        # Titulo ventana
        self.root.title("Cuentas")
        # tamaño ventana
        self.root.geometry("900x900")

        # Barra de navegación
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        # Submenú "Archivo"
        app_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=app_menu)
        app_menu.add_command(label="Cargar Archivo", command=self.boton_load_save)

        # Variable para guardar entradas antes de crearlos
        self.entries = {} 
        self.crear_accesos()

        # instancia de load con callback
        self.vista_load = VistaLoad(master=self.root, callback=self.recibir_lineas)

        # Inicializa variable vacia
        self.url_user = ""
        self.lineas_recibidas = [] # Variable para almacenar las líneas
        
    def crear_accesos(self):
        row = 1

        # Paquete de Mes
        row += 2
        self.crear_entrada_simple(row, "Mes")
        row += 1
        
        # Paquete de Efectivo
        tk.Label(self.root, text="EFECTIVO").grid(row=row, column=0, columnspan=3)
        row += 1
        self.crear_entrada_simple(row, "Efectivo actual")
        row += 1
        self.create_entry(row, "Obs Efect") 
        row += 1
        
        # Paquete de Cuentas de Ahorro
        tk.Label(self.root, text="CUENTAS").grid(row=row, column=0, columnspan=4)
        row += 1
        self.create_entries_pair(row, "Nombre Cuenta de ahorro 1", "Nombre Cuenta de ahorro 2", "#e0f7fa")
        row += 1
        self.create_entries_pair(row, "Valor Actual Cuenta1", "Valor Actual Cuenta2", "#e0f7fa")
        row += 1
        self.create_entries_pair(row, "Consignaciones Mes CA1", "Consignaciones Mes CA2", "#e0f7fa")

        row += 1
        self.create_entries_pair(row, "Nombre Cuenta de ahorro 3", "Nombre Cuenta de ahorro 4", "#f1f8e9")
        row += 1
        self.create_entries_pair(row, "Valor Actual Cuenta3", "Valor Actual Cuenta4", "#f1f8e9")
        row += 1
        self.create_entries_pair(row, "Consignaciones Mes CA3", "Consignaciones Mes CA4", "#f1f8e9")
        row += 1

        # Paquete de suma de consignaciones
        self.create_suma_consignaciones_entry(row, "Suma ConsignacionesXMes", "Sumar", 
        self.boton_calcular_consignacionesxmes)
        row += 1

        self.create_entry(row, "Obs Cuentas de ahorro")  
        row += 1
        self.crear_entrada_simple(row, "Acumulado Consignaciones")
        row += 1
        
        # Paquete de DIVISIAS
        tk.Label(self.root, text="OTRAS MONEDAS").grid(row=row, column=0, columnspan=3)
        row += 1
        self.crear_entrada_simple(row, "Otra moneda")
        row += 1
        self.create_entry(row, "Obs OMon")
        row += 1

        # Paquete de Inversiones
        tk.Label(self.root, text="INVERSIONES").grid(row=row, column=0, columnspan=3)
        row += 1
        self.create_entry(row, "Apertura inversiones en Mes")
        row += 1
        self.create_entries_triple(row, "Inversion 1?", "Obs Inv1", "Entidad 1?")
        row += 1
        self.create_entries_triple(row, "Inversion 2?", "Obs Inv2", "Entidad 2?")
        row += 1
        self.create_entries_triple(row, "Inversion 3?", "Obs Inv3", "Entidad 3?")
        row += 1
        self.create_entries_triple(row, "Inversion 4?", "Obs Inv4", "Entidad 4?")
        row += 1
        self.crear_entrada_simple(row, "Acumulado Inversiones")
        row += 1

        # Paquete de Gastos
        tk.Label(self.root, text="GASTOS").grid(row=row, column=0, columnspan=3)
        row += 1
        self.crear_entrada_simple(row, "Compras?")
        row += 1
        self.create_entry(row, "Obs Compras")
        row += 1
        self.crear_entrada_simple(row, "Gastos?")
        row += 1
        self.create_entry(row, "Obs Gastos")
        row += 1
        self.create_entries_triple(row, "Prestamo1", "Prestamo2", "Prestamo3")
        row += 1
        self.create_suma_prestamos_entry(row, "Total Prestamos", "Sumar", 
        self.boton_sumar_prestamos)
        row += 1
        self.create_entry(row, "Obs Prestamos")
        row += 1
        
        # Paquete de Observaciones
        row += 1
        tk.Label(self.root, text="OBSERVACIONES GENERALES").grid(row=row, column=0, columnspan=3)
        row += 1
        self.crear_entrada_total(row, "Observaciones Adicionales")
        row += 1

        # Paquete acumulado consignaciones
        self.create_suma_consignaciones_entry(row, "Acum Consigna+Inversiones", "Calcular", 
        self.boton_sumar_acumulado)
        row += 1

        confirm_button = tk.Button(self.root, text="Confirmar Datos", command=self.evento_boton_confirmar_datos)
        confirm_button.grid(row=row, column=0, columnspan=2, pady=10)
        row += 1

    def crear_entrada_combox(self, row, label, tipo="entry", opciones=None):
        tk.Label(self.root, text=label).grid(row=row, column=0, sticky="w")
        combo = ttk.Combobox(self.root, values=opciones, state="readonly")
        combo.current(0)  # Seleccionar primer valor por defecto
        combo.grid(row=row, column=1, sticky="we")
        self.entries[label] = combo

    def crear_entrada_total(self, row, label):
        entry = tk.Entry(self.root)
        entry.insert(0, "vacio")  # Establecer el valor inicial 0
        entry.grid(row=row, column=0, columnspan=6, sticky="we")
        self.entries[label] = entry  # Guardar el Entry en un diccionario

    def crear_entrada_simple(self, row, label):
        tk.Label(self.root, text=label).grid(row=row, column=0, sticky="w")
        entry = tk.Entry(self.root)
        entry.insert(0, "0")  # Establecer el valor inicial 0
        entry.grid(row=row, column=1, columnspan=1, sticky="we")
        self.entries[label] = entry  # Guardar el Entry en un diccionario
    
    def create_entry(self, row, label):
        tk.Label(self.root, text=label).grid(row=row, column=0, sticky="w")
        entry = tk.Entry(self.root)
        entry.insert(0, "vacio")  # Establecer el valor inicial 0
        entry.grid(row=row, column=1, columnspan=5, sticky="we")
        self.entries[label] = entry  # Guardar el Entry en un diccionario

    def create_suma_consignaciones_entry(self, row, label_text, button_text, command_callback):
        # Label
        tk.Label(self.root, text=label_text).grid(row=row, column=0, sticky="w")
        
        # Entry (en vez de Label para mostrar el resultado)
        entry = tk.Entry(self.root)
        entry.insert(0, "0")  # Valor inicial
        entry.grid(row=row, column=1, sticky="we")
        self.entries[label_text] = entry  # Guardar el entry si necesitas acceder luego

        # Botón
        button = tk.Button(self.root, text=button_text, command=command_callback)
        button.grid(row=row, column=2, sticky="we", padx=5)
    
    def create_suma_prestamos_entry(self, row, label_text, button_text, command_callback):
        # Label
        tk.Label(self.root, text=label_text).grid(row=row, column=0, sticky="w")
        
        # Entry (en vez de Label para mostrar el resultado)
        entry = tk.Entry(self.root)
        entry.insert(0, "0")  # Valor inicial
        entry.grid(row=row, column=1, sticky="we")
        self.entries[label_text] = entry  # Guardar el entry si necesitas acceder luego

        # Botón
        button = tk.Button(self.root, text=button_text, command=command_callback)
        button.grid(row=row, column=2, sticky="we", padx=5)
   
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

    def get_datos_window(self):
        for key in self.datos.keys():
            try:
                widget = self.entries[key]
                valor = widget.get() if widget.get() else "vacio"
                self.datos[key] = valor
            except Exception as e:
                print(f"Error con la clave '{key}': {e}")
        
        print("Datos obtenidos:", self.datos)
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
            self.datos['Consignaciones Mes CA3'],
            self.datos['Consignaciones Mes CA4']
        )

        print(f"Suma de consignaciones: {sumaConsig}")

        # Mostrar el resultado en la ventana
        self.entries["Suma ConsignacionesXMes"].delete(0, tk.END)
        self.entries["Suma ConsignacionesXMes"].insert(0, str(sumaConsig))

    def boton_sumar_prestamos(self):
        print("Clicked Suma de prestamos")
        self.get_datos_window()

        # Instanciar la clase Calculadora
        calculadora = Calculadora()
        #print(self.datos['Consignaciones Mes CA1'])

        # Calcular la suma
        sumaPrestamos = calculadora.sumaPrestamos(
            self.datos['Prestamo1'],
            self.datos['Prestamo2'],
            self.datos['Prestamo3'],
        )

        print(f"Suma de prestamo: {sumaPrestamos}")

        # Mostrar el resultado en la ventana
        self.entries["Total Prestamos"].delete(0, tk.END)
        self.entries["Total Prestamos"].insert(0, str(sumaPrestamos))


    def boton_sumar_acumulado(self):
        print("Clicked Suma de acumulado")
        self.get_datos_window()

        # Instanciar la clase Calculadora
        calculadora = Calculadora()
        #print(self.datos['Consignaciones Mes CA1'])

        # Calcular acumTotal
        acumTotal = calculadora.AcumTotal(
            self.datos['Acumulado Consignaciones'],
            self.datos['Acumulado Inversiones']
        )

        print(f"Acumulado total: {acumTotal}")

        # Mostrar el resultado en la ventana
        self.entries["Acum Consigna+Inversiones"].delete(0, tk.END)
        self.entries["Acum Consigna+Inversiones"].insert(0, str(acumTotal))

    def evento_boton_confirmar_datos(self):
        print("Clicked Confirmar Datos")
        self.get_datos_window()
        # calcular patrimonio y activos 
        # Instanciar la clase Calculadora
        calculadora = Calculadora()
        print(self.datos['Efectivo actual'])
         
        # Llamar al método activos
        activos = calculadora.activos(self.datos['Efectivo actual'], 
                                    self.datos['Valor Actual Cuenta1'], 
                                    self.datos['Valor Actual Cuenta2'], 
                                    self.datos['Valor Actual Cuenta3'], 
                                    self.datos['Valor Actual Cuenta4'], 
                                    self.datos['Inversion 1?'], 
                                    self.datos['Inversion 2?'], 
                                    self.datos['Inversion 3?'],
                                    self.datos['Inversion 4?'],
                                    self.datos['Otra moneda'])

        # Convertir el resultado a string (opcional en Python)
        str_total_ac = str(activos)

        # Llamar al método patrimonio
        patrimonio = calculadora.patrimonio(str_total_ac, self.datos['Total Prestamos'])

        # Mostrar el resultado (equivalente a System.out.println)
        print(f"Resultado: {activos}")
        print(f"Patrimonio: {patrimonio}") 
        

        # # Preparar los datos
        Datos = f"""
        Mes: {self.datos['Mes']} 
        ******************************* 
        Efectivo: {self.datos['Efectivo actual']}
        ObsEfectivo: {self.datos['Obs Efect']}
        ******************************* 
        Nombre Cuenta de ahorro1: {self.datos['Nombre Cuenta de ahorro 1']}
        Valor Actual Cuenta1: {self.datos['Valor Actual Cuenta1']}
        ConsignacionesXMesC1: {self.datos['Consignaciones Mes CA1']}
        Nombre Cuenta de ahorro2: {self.datos['Nombre Cuenta de ahorro 2']}
        Valor Actual Cuenta2: {self.datos['Valor Actual Cuenta2']} 
        ConsignacionesXMesC2: {self.datos['Consignaciones Mes CA2']}
        Nombre Cuenta de ahorro3: {self.datos['Nombre Cuenta de ahorro 3']}
        Valor Actual Cuenta3: {self.datos['Valor Actual Cuenta3']} 
        ConsignacionesXMesC3: {self.datos['Consignaciones Mes CA3']}
        Nombre Cuenta de ahorro4: {self.datos['Nombre Cuenta de ahorro 4']}
        Valor Actual Cuenta4: {self.datos['Valor Actual Cuenta4']} 
        ConsignacionesXMesC4: {self.datos['Consignaciones Mes CA4']}
        Suma ConsignacionesXMes: {self.datos['Suma ConsignacionesXMes']}
        ObsCuentaAhorro: {self.datos['Obs Cuentas de ahorro']}
        ******************************* 
        Otra Moneda: {self.datos['Otra moneda']}
        ObsOM: {self.datos['Obs OMon']}
        ******************************* 
        AperturaInversiones: {self.datos['Apertura inversiones en Mes']}
        Inversion1: {self.datos['Inversion 1?']}
        Entidad1: {self.datos['Entidad 1?']}
        ObsInv1: {self.datos['Obs Inv1']}
        Inversion2: {self.datos['Inversion 2?']}
        Entidad2: {self.datos['Entidad 2?']}
        ObsInv2: {self.datos['Obs Inv2']}
        Inversion3: {self.datos['Inversion 3?']}
        Entidad3: {self.datos['Entidad 3?']}
        ObsInv3: {self.datos['Obs Inv3']}
        Inversion4: {self.datos['Inversion 4?']}
        Entidad4: {self.datos['Entidad 4?']}
        ObsInv4: {self.datos['Obs Inv4']}
        ******************************* 
        Compras: {self.datos['Compras?']}
        ObsCompra: {self.datos['Obs Compras']}
        Gastos: {self.datos['Gastos?']}
        ObsGastos: {self.datos['Obs Gastos']}
        Prestamo1: {self.datos['Prestamo1']}
        Prestamo2: {self.datos['Prestamo2']}
        Prestamo3: {self.datos['Prestamo3']}
        Total Prestamos: {self.datos['Total Prestamos']} 
        Obs Prestamos: {self.datos['Obs Prestamos']}
        ******************************* 
        Activos: {activos}
        Pasivos: {self.datos['Total Prestamos']}
        Patrimonio: {patrimonio}
        ******************************* 
        AcumConsignaciones: {self.datos['Acumulado Consignaciones']}
        AcumInversiones: {self.datos['Acumulado Inversiones']}
        Observaciones: {self.datos['Observaciones Adicionales']}
        Acum Consigna+Inversiones: {self.datos['Acum Consigna+Inversiones']}
        """
        # clic “Confirmar” crea nueva ventana totalmente nueva sin instancia.
        ventana = VistaConfirm(self.root)
        ventana.set_label2_text(Datos)
        ventana.mostrar()
            # tamaño ventana
        self.root.geometry("900x900")

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
            "Efectivo actual": 3, 
            "Obs Efect": 4,

            "Nombre Cuenta de ahorro 1": 6,
            "Valor Actual Cuenta1": 7,
            "Consignaciones Mes CA1": 8, 
            "Nombre Cuenta de ahorro 2": 9,
            "Valor Actual Cuenta2": 10,
            "Consignaciones Mes CA2": 11,
            "Nombre Cuenta de ahorro 3": 12,
            "Valor Actual Cuenta3": 13, 
            "Consignaciones Mes CA3": 14,
            "Nombre Cuenta de ahorro 4": 15,
            "Valor Actual Cuenta4": 16, 
            "Consignaciones Mes CA4": 17,
            "Suma ConsignacionesXMes": 18,
            "Obs Cuentas de ahorro": 19,

            "Otra moneda": 21,
            "Obs OMon": 22,

            "Apertura inversiones en Mes": 24,
            "Inversion 1?": 25,
            "Entidad 1?": 26,
            "Obs Inv1": 27,
            "Inversion 2?": 28,
            "Entidad 2?": 29,
            "Obs Inv2": 30,
            "Inversion 3?": 31,
            "Entidad 3?": 32,
            "Obs Inv3": 33,
            "Inversion 4?": 34,
            "Entidad 4?": 35,
            "Obs Inv4": 36,
            
            "Compras?": 38,
            "Obs Compras": 39,
            "Gastos?": 40,
            "Obs Gastos": 41,
            "Prestamo1": 42,
            "Prestamo2": 43,
            "Prestamo3": 44,
            "Total Prestamos": 45,
            "Obs Prestamos": 46,

            "Acumulado Consignaciones": 52, 
            "Acumulado Inversiones": 53, 
            "Observaciones Adicionales": 54,
            "Acum Consigna+Inversiones": 55
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
