import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from comunes.VistaConfirm import VistaConfirm  # Importar la clase desde el módulo
from .Calculadora import Calculadora
from comunes.VistaLoad import VistaLoad

class ApliRenta(ttk.Frame):
#class VistaPrincipal:
    def __init__(self, master=None):
         # Determinar la ventana superior (self.top) y si esta clase creó el root
        self._owns_root = False
        if master is None:
            # Ejecutar como app independiente
            self.top = tk.Tk()
            self._owns_root = True
            parent_for_frame = self.top
        else:
            # Si el master es una ventana (Tk o Toplevel) -> usamos esa ventana
            if isinstance(master, (tk.Tk, tk.Toplevel)):
                self.top = master
                parent_for_frame = self.top
            else:
                # Si el master es un Frame (embedding) -> creamos un Toplevel para que abra en ventana separada
                self.top = tk.Toplevel()
                parent_for_frame = self.top

        # Inicializar el Frame dentro de la ventana real
        super().__init__(parent_for_frame)
        # Mostrar el frame en la ventana que corresponde
        self.pack(fill="both", expand=True)

        # Configuración básica de la ventana
        try:
            # Título/geometry solo si tenemos una ventana real
            if isinstance(self.top, (tk.Tk, tk.Toplevel)):
                self.top.title("Rentabilidades")
                # Si creamos el root, damos tamaño por defecto; si el usuario pasó un Toplevel/Tk se respeta o se reajusta
                if self._owns_root:
                    self.top.geometry("1600x1200")
                else:
                    # si el top proviene de caller, no forzamos un tamaño grande, solo un mínimo
                    try:
                        self.top.minsize(2000, 900)
                    except Exception:
                        pass
        except Exception:
            pass

        # Crear barra de menú SOLO si esta clase creó su propio root (para no pisar menús en apps integradas)
        # Crear menú si estamos en una ventana real (Tk o Toplevel)
        if isinstance(self.top, (tk.Tk, tk.Toplevel)):
            try:
                menubar = tk.Menu(self.top)
                self.top.config(menu=menubar)
                app_menu = tk.Menu(menubar, tearoff=0)
                menubar.add_cascade(label="Archivo", menu=app_menu)
                app_menu.add_command(label="Cargar Archivo", command=self.boton_load_save)
            except Exception:
                pass

        
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

        # ---------- SCROLLABLE AREA (canvas + interior) ----------
        contenedor = tk.Frame(self)
        contenedor.pack(fill="both", expand=True)

        # Canvas que contendrá el interior desplazable
        self.canvas = tk.Canvas(contenedor)
        self.canvas.pack(side="left", fill="both", expand=True)

        # Scrollbar vertical
        scrollbar = ttk.Scrollbar(contenedor, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")
        
        # Crear y configurar estilo para scrollbar más grueso
        style = ttk.Style()
        
        # Configurar estilo personalizado
        style.configure("Custom.Vertical.TScrollbar",
                arrowsize=20,
                width=35,
                background="#6C8EBF",  # Color del deslizador
                troughcolor="#F5F5F5",  # Color del canal
                borderwidth=0,
                relief="flat")
        
        # Aplicar el estilo
        scrollbar.configure(style="Custom.Vertical.TScrollbar")

        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Frame interior donde pondrás los widgets (este es el que se desplaza)
        self.interior = tk.Frame(self.canvas)
        self.interior_id = self.canvas.create_window((0, 0), window=self.interior, anchor="nw")

        # Cuando cambie el tamaño del interior actualizamos la scrollregion
        self.interior.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Ajustar el ancho del interior cuando cambie el canvas (para que grid se comporte)
        def _on_canvas_configure(event):
            canvas_width = event.width
            try:
                self.canvas.itemconfigure(self.interior_id, width=canvas_width)
            except Exception:
                pass
        self.canvas.bind("<Configure>", _on_canvas_configure)

        # Soporte de rueda del ratón para el scroll (Windows/macOS/Linux)
        self._bind_mousewheel()

        # Variables y creación de widgets
        self.entries = {}
        self.create_widgets()

        # instancia de load con callback
        try:
            vista_load_master = self.top if isinstance(self.top, (tk.Tk, tk.Toplevel)) else self.winfo_toplevel()
            self.vista_load = VistaLoad(master=vista_load_master, callback=self.recibir_lineas)
        except Exception:
            self.vista_load = None

        # Inicializa variable vacia
        self.url_user = ""
        self.lineas_recibidas = [] # Variable para almacenar las líneas
    
    # Manejo de la rueda del ratón (soporte multiplataforma)
    def _bind_mousewheel(self):
        # Vincular cuando el cursor entra al canvas para que la rueda funcione
        self.canvas.bind("<Enter>", lambda e: self.canvas.focus_set())
        # Windows / macOS
        self.canvas.bind("<MouseWheel>", self._on_mousewheel_windows_mac)
        # Linux (scroll up / down)
        self.canvas.bind("<Button-4>", self._on_mousewheel_linux)
        self.canvas.bind("<Button-5>", self._on_mousewheel_linux)

    def _on_mousewheel_windows_mac(self, event):
        try:
            delta = int(-1 * (event.delta / 120))
        except Exception:
            delta = 0
        self.canvas.yview_scroll(delta, "units")

    def _on_mousewheel_linux(self, event):
        if event.num == 4:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            self.canvas.yview_scroll(1, "units")
    
    # CREACIÓN DEL FORMULARIO
    def create_widgets(self):
        row = 0  # Comenzar en 0, no en 1

        # Paquete de Mes
        self.create_entry(row, "Mes")
        row += 1

        # Paquete de Inversiones
        tk.Label(self.interior, text="INVERSIONES").grid(row=row, column=0, columnspan=3)
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
        tk.Label(self.interior, text="INVERSORES").grid(row=row, column=0, columnspan=3)
        row += 1
        self.create_entries_pair(row, "Inversor1", "ValorInversor1")
        row += 1
        self.create_entries_pair(row, "Inversor2", "ValorInversor2")
        row += 1
        self.create_entries_pair(row, "Inversor3", "ValorInversor3")
        row += 1
        self.create_entries_pair(row, "Inversor4", "ValorInversor4")
        row += 1

        confirm_button = tk.Button(self.interior, text="Confirmar Datos", command=self.evento_boton_confirmar_datos)
        confirm_button.grid(row=row, column=0, columnspan=2, pady=10)
        row += 1
    
    def create_entries_uno(self, row, campo1, bg_color="#ffffff"):
        tk.Label(self.interior, text=campo1, bg=bg_color).grid(row=row, column=0, sticky="w")
        entry1 = tk.Entry(self.interior, bg=bg_color)
        entry1.insert(0, "0")
        entry1.grid(row=row, column=1, columnspan=6, sticky="we")
        self.entries[campo1] = entry1

    def create_entries_pair(self, row, label1, label2, bg_color="#ffffff"):
        tk.Label(self.interior, text=label1, bg=bg_color).grid(row=row, column=0, sticky="w")
        entry1 = tk.Entry(self.interior, bg=bg_color)
        entry1.insert(0, "0")
        entry1.grid(row=row, column=1, sticky="we")
        self.entries[label1] = entry1

        tk.Label(self.interior, text=label2, bg=bg_color).grid(row=row, column=2, sticky="w")
        entry2 = tk.Entry(self.interior, bg=bg_color)
        entry2.insert(0, "0")
        entry2.grid(row=row, column=3, sticky="we")
        self.entries[label2] = entry2

    def create_entries_triple(self, row, campo1, campo2, campo3, campo4):
        # Labels y entradas
        tk.Label(self.interior, text=campo1).grid(row=row, column=0, sticky="w")
        entry1 = tk.Entry(self.interior)
        entry1.insert(0, "0")
        entry1.grid(row=row, column=1, sticky="we")
        self.entries[campo1] = entry1

        tk.Label(self.interior, text=campo2).grid(row=row, column=2, sticky="w")
        entry2 = tk.Entry(self.interior)
        entry2.insert(0, "0")
        entry2.grid(row=row, column=3, sticky="we")
        self.entries[campo2] = entry2

        tk.Label(self.interior, text=campo3).grid(row=row, column=4, sticky="w")
        entry3 = tk.Entry(self.interior)
        entry3.insert(0, "0")
        entry3.grid(row=row, column=5, sticky="we")
        self.entries[campo3] = entry3

        tk.Label(self.interior, text=campo4).grid(row=row, column=6, sticky="w")
        entry4 = tk.Entry(self.interior, state="readonly")
        entry4.grid(row=row, column=7, sticky="we")
        self.entries[campo4] = entry4

        # Botón para sumar
        btn = tk.Button(self.interior, text="Sumar", command=lambda: self.sumar_campos(campo1, campo3, campo4))
        btn.grid(row=row, column=8)

    def create_entry(self, row, label):
        """Crea un Entry y lo guarda en el diccionario"""
        tk.Label(self.interior, text=label).grid(row=row, column=0, sticky="w")
        entry = tk.Entry(self.interior)
        entry.insert(0, "0")  # Establecer el valor inicial 0
        entry.grid(row=row, column=1, columnspan=3, sticky="we")
        self.entries[label] = entry  # Guardar el Entry en un diccionario

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
        Valor Próximo {self.datos['Inversor1']}: {totales1[4]}
        Restante después {self.datos['Inversor1']}: {totales1[5]}
        
        {self.datos['Inversor2']}
        Inversion {self.datos['Inversor2']}: {self.datos['ValorInversor2']}
        Porcentaje {self.datos['Inversor2']}: {totales1[6]}
        Ganancia {self.datos['Inversor2']}: {totales1[7]}
        Valor Próximo {self.datos['Inversor2']}: {totales1[8]}
        Restante después {self.datos['Inversor2']}: {totales1[9]}
        
        {self.datos['Inversor3']}
        Inversion {self.datos['Inversor3']}: {self.datos['ValorInversor3']}
        Porcentaje {self.datos['Inversor3']}: {totales1[10]}
        Ganancia {self.datos['Inversor3']}: {totales1[11]}
        Valor Próximo {self.datos['Inversor3']}: {totales1[12]}
        Restante después {self.datos['Inversor3']}: {totales1[13]}
        
        {self.datos['Inversor4']}
        Inversion {self.datos['Inversor4']}: {self.datos['ValorInversor4']}
        Porcentaje {self.datos['Inversor4']}: {totales1[14]}
        Ganancia {self.datos['Inversor4']}: {totales1[15]}
        Valor Próximo {self.datos['Inversor4']}: {totales1[16]}
        Restante después {self.datos['Inversor4']}: {totales1[17]}
        """
        # clic “Confirmar” crea nueva ventana totalmente nueva sin instancia.
        ventana = VistaConfirm(self.top)
        ventana.set_label2_text(Datos)
        ventana.mostrar()

    def boton_load_save(self):
        print("Load Save clicked!")

        # Asegurar que la ventana exista; si fue destruida la volvemos a crear
        try:
            if not hasattr(self, "vista_load") or self.vista_load is None or not self.vista_load.winfo_exists():
                master_for_load = self.top if isinstance(self.top, (tk.Tk, tk.Toplevel)) else self.winfo_toplevel()
                self.vista_load = VistaLoad(master=master_for_load, callback=self.recibir_lineas)
        except Exception as e:
            print("Error creando VistaLoad, lo intento de nuevo:", e)
            master_for_load = self.top if isinstance(self.top, (tk.Tk, tk.Toplevel)) else self.winfo_toplevel()
            self.vista_load = VistaLoad(master=master_for_load, callback=self.recibir_lineas)

        # Mostrar la ventana
        try:
            self.vista_load.mostrar()
        except Exception as e:
            print("Error mostrando VistaLoad:", e)
    
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
            "Inversor2": 73,
            "ValorInversor2": 74,
            "Inversor3": 80,
            "ValorInversor3": 81,
            "Inversor4": 87,
            "ValorInversor4": 88
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
   
       # EJECUCIÓN
    
    def run(self):
        # Si esta clase creó su propio root, ejecuta mainloop; si no, asume que el llamador lo hará
        if self._owns_root:
            try:
                self.top.mainloop()
            except Exception:
                pass

# Si ejecutas este archivo directamente, creamos la app (esto preserva tu estilo)
if __name__ == "__main__":
    app = ApliRenta(None)
    app.run()
