import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from comunes.VistaConfirm import VistaConfirm  # Importar la clase desde el módulo
from .Calculadora import Calculadora
from comunes.VistaLoad import VistaLoad


class ApliCuentas(ttk.Frame):
    """Clase ApliCuentas corregida y limpia.

    Comportamiento:
    - Si master es None -> crea un Tk() propio (owns_root = True) y ejecuta mainloop si se llama run().
    - Si master es un Tk o Toplevel -> usa esa ventana (se comporta embebida o como ventana principal externa).
    - Si master es un Frame (por ejemplo container de AppPrincipal) -> crea un Toplevel independiente
      para que la aplicación se abra en su propia ventana.

    En todos los casos, el Frame principal de la aplicación (self) se crea dentro de una ventana
    (self.top) y contiene el canvas + scrollbar + interior en el que están los widgets.
    """

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
                self.top.title("Cuentas")
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

        # Datos y estado
        self.datos = {
            "Mes": "", "Efectivo actual": "", "Obs Efect": "",
            "Nombre Cuenta de ahorro 1": "", "Nombre Cuenta de ahorro 2": "", "Nombre Cuenta de ahorro 3": "","Nombre Cuenta de ahorro 4": "",
            "Valor Actual Cuenta1": "", "Valor Actual Cuenta2": "", "Valor Actual Cuenta3": "", "Valor Actual Cuenta4": "",
            "Consignaciones Mes CA1": "", "Consignaciones Mes CA2": "", "Consignaciones Mes CA3": "", "Consignaciones Mes CA4": "",
            "Suma ConsignacionesXMes": "","Obs Cuentas de ahorro": "",
            "Acumulado Consignaciones Anterior": "", "Nuevo Acumulado Consignaciones": "", 
            "Otra moneda": "", "Obs OMon": "", 
            "Inversion 1?": "", "Entidad 1?": "", "Obs Inv1": "", 
            "Inversion 2?": "", "Entidad 2?": "", "Obs Inv2": "",
            "Inversion 3?": "", "Entidad 3?": "", "Obs Inv3": "", 
            "Inversion 4?": "", "Entidad 4?": "", "Obs Inv4": "",
            "Inversion 5?": "", "Entidad 5?": "", "Obs Inv5": "",
            "Inversion 6?": "", "Entidad 6?": "", "Obs Inv6": "",
            "Apertura inversiones en Mes": "","Acumulado Inversiones Anterior": "", "Nuevo Acumulado Inversiones": "", "Obs Inversiones":"",
            "Compras?": "", "Obs Compras": "", "Gastos?": "", "Obs Gastos": "",
            "Prestamo1": "", "Prestamo2": "", "Prestamo3": "", "Prestamo4": "",
            "nameP1":"", "nameP2":"","nameP3":"","nameP4":"",
            "Obs Pres1":"","Obs Pres2":"","Obs Pres3":"","Obs Pres4":"",
            "Total Prestamos": "", "Obs Prestamos": "", "Acum Consigna+Inversiones": "",
            "Observaciones Adicionales": ""
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
        self.crear_accesos()

        # instancia de load con callback
        try:
            vista_load_master = self.top if isinstance(self.top, (tk.Tk, tk.Toplevel)) else self.winfo_toplevel()
            self.vista_load = VistaLoad(master=vista_load_master, callback=self.recibir_lineas)
        except Exception:
            self.vista_load = None

        # Inicializa variable vacia
        self.url_user = ""
        self.lineas_recibidas = []  # Variable para almacenar las líneas

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
    def crear_accesos(self):
        row = 1

        # Paquete de Mes
        row += 2
        self.crear_entrada_simple(row, "Mes")
        row += 1
        
        # Paquete de Efectivo
        tk.Label(self.interior, text="EFECTIVO", bg="lightblue").grid(row=row, column=0, columnspan=10, sticky="we", pady=(8,2))
        row += 1
        self.crear_entrada_simple(row, "Efectivo actual")
        row += 1
        self.create_entry(row, "Obs Efect") 
        row += 1
        
        # Paquete de Cuentas de Ahorro
        tk.Label(self.interior, text="CUENTAS", bg="lightblue").grid(row=row, column=0, columnspan=10, sticky="we", pady=(8,2))
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
        self.create_suma_consignaciones_entry(row, "Suma ConsignacionesXMes", "Sumar", self.boton_calcular_consignacionesxmes)
        row += 1

        self.create_entry(row, "Obs Cuentas de ahorro")  
        row += 1
        self.crear_entrada_simple(row, "Acumulado Consignaciones Anterior")
        row += 1
        self.create_suma_consignaciones_entry(row, "Nuevo Acumulado Consignaciones", "Calcular", self.boton_calcular_Acumconsignaciones)
        row += 1
        
        # Paquete de DIVISIAS
        tk.Label(self.interior, text="OTRAS MONEDAS", bg="lightblue").grid(row=row, column=0, columnspan=10, sticky="we", pady=(8,2))
        row += 1
        self.crear_entrada_simple(row, "Otra moneda")
        row += 1
        self.create_entry(row, "Obs OMon")
        row += 1

        # Paquete de Inversiones
        tk.Label(self.interior, text="INVERSIONES", bg="lightblue").grid(row=row, column=0, columnspan=10, sticky="we", pady=(8,2))
        row += 1
        self.create_entries_triple(row, "Inversion 1?", "Obs Inv1", "Entidad 1?")
        row += 1
        self.create_entries_triple(row, "Inversion 2?", "Obs Inv2", "Entidad 2?")
        row += 1
        self.create_entries_triple(row, "Inversion 3?", "Obs Inv3", "Entidad 3?")
        row += 1
        self.create_entries_triple(row, "Inversion 4?", "Obs Inv4", "Entidad 4?")
        row += 1
        self.create_entries_triple(row, "Inversion 5?", "Obs Inv5", "Entidad 5?")
        row += 1
        self.create_entries_triple(row, "Inversion 6?", "Obs Inv6", "Entidad 6?")
        row += 1
        self.create_entry(row, "Obs Inversiones")
        row += 1
        self.crear_entrada_simple(row, "Apertura inversiones en Mes")
        row += 1
        self.crear_entrada_simple(row, "Acumulado Inversiones Anterior")
        row += 1
        self.create_suma_consignaciones_entry(row, "Nuevo Acumulado Inversiones", "Calcular", self.boton_calcular_Acuminverisones)
        row += 1

        # Paquete de Gastos
        tk.Label(self.interior, text="GASTOS", bg="lightblue").grid(row=row, column=0, columnspan=10, sticky="we", pady=(8,2))
        row += 1
        self.crear_entrada_simple(row, "Compras?")
        row += 1
        self.create_entry(row, "Obs Compras")
        row += 1
        self.crear_entrada_simple(row, "Gastos?")
        row += 1
        self.create_entry(row, "Obs Gastos")
        row += 1

        # Paquete de Prestamos
        tk.Label(self.interior, text="PRESTAMOS", bg="lightblue").grid(row=row, column=0, columnspan=10, sticky="we", pady=(8,2))
        row += 1
        self.create_entries_triple(row, "Prestamo1","nameP1", "Obs Pres1")
        row += 1
        self.create_entries_triple(row, "Prestamo2", "nameP2", "Obs Pres2")
        row += 1
        self.create_entries_triple(row, "Prestamo3", "nameP3", "Obs Pres3")
        row += 1
        self.create_entries_triple(row, "Prestamo4", "nameP4", "Obs Pres4")
        row += 1

        self.create_suma_prestamos_entry(row, "Total Prestamos", "Sumar", self.boton_sumar_prestamos)
        row += 1
        
        tk.Label(self.interior, text="OBSERVACIONES GENERALES", bg="lightblue").grid(row=row, column=0, columnspan=10, sticky="we", pady=(8,2))
        row += 1
        self.crear_entrada_total(row, "Observaciones Adicionales")
        row += 1

        self.create_suma_consignaciones_entry(row, "Acum Consigna+Inversiones", "Calcular", self.boton_sumar_acumulado)
        row += 1

        confirm_button = tk.Button(self.interior, text="Confirmar Datos", command=self.evento_boton_confirmar_datos)
        confirm_button.grid(row=row, column=0, columnspan=2, pady=10)
        row += 1

        # Ajuste de columnas para que se expandan correctamente
        #for c in range(6):
         #   self.interior.grid_columnconfigure(c, weight=1)

    # FUNCIONES AUXILIARES
    def crear_entrada_simple(self, row, label):
        tk.Label(self.interior, text=label).grid(row=row, column=0, sticky="w", padx=4, pady=2)
        entry = tk.Entry(self.interior)
        entry.insert(0, "0")
        entry.grid(row=row, column=1, sticky="we", padx=4, pady=2)
        self.entries[label] = entry

    def crear_entrada_combox(self, row, label, tipo="entry", opciones=None):
        tk.Label(self.interior, text=label).grid(row=row, column=0, sticky="w")
        combo = ttk.Combobox(self.interior, values=opciones or [], state="readonly")
        if opciones:
            try:
                combo.current(0)  # Seleccionar primer valor por defecto
            except Exception:
                pass
        combo.grid(row=row, column=1, sticky="we")
        self.entries[label] = combo

    def crear_entrada_total(self, row, label):
        entry = tk.Entry(self.interior)
        entry.insert(0, "vacio")
        entry.grid(row=row, column=0, columnspan=6, sticky="we", padx=4, pady=2)
        self.entries[label] = entry

    def create_entry(self, row, label):
        tk.Label(self.interior, text=label).grid(row=row, column=0, sticky="w", padx=4, pady=2)
        entry = tk.Entry(self.interior)
        entry.insert(0, "vacio")
        entry.grid(row=row, column=1, columnspan=5, sticky="we", padx=4, pady=2)
        self.entries[label] = entry

    def create_suma_consignaciones_entry(self, row, label_text, button_text, command_callback):
        tk.Label(self.interior, text=label_text).grid(row=row, column=0, sticky="w", padx=4, pady=2)
        entry = tk.Entry(self.interior)
        entry.insert(0, "0")
        entry.grid(row=row, column=1, sticky="we", padx=4, pady=2)
        self.entries[label_text] = entry
        tk.Button(self.interior, text=button_text, command=command_callback).grid(row=row, column=2, sticky="we", padx=5)

    def create_suma_prestamos_entry(self, row, label_text, button_text, command_callback):
        tk.Label(self.interior, text=label_text).grid(row=row, column=0, sticky="w", padx=4, pady=2)
        entry = tk.Entry(self.interior)
        entry.insert(0, "0")
        entry.grid(row=row, column=1, sticky="we", padx=4, pady=2)
        self.entries[label_text] = entry
        tk.Button(self.interior, text=button_text, command=command_callback).grid(row=row, column=2, sticky="we", padx=5)

    def create_entries_pair(self, row, label1, label2, bg_color="#ffffff"):
        tk.Label(self.interior, text=label1, bg=bg_color).grid(row=row, column=0, sticky="w", padx=4, pady=2)
        e1 = tk.Entry(self.interior, bg=bg_color)
        e1.insert(0, "0")
        e1.grid(row=row, column=1, sticky="we", padx=4, pady=2)
        self.entries[label1] = e1

        tk.Label(self.interior, text=label2, bg=bg_color).grid(row=row, column=2, sticky="w", padx=4, pady=2)
        e2 = tk.Entry(self.interior, bg=bg_color)
        e2.insert(0, "0")
        e2.grid(row=row, column=3, sticky="we", padx=4, pady=2)
        self.entries[label2] = e2

    def create_entries_triple(self, row, label1, label2, label3):
        tk.Label(self.interior, text=label1).grid(row=row, column=0, sticky="w", padx=4, pady=2)
        e1 = tk.Entry(self.interior)
        e1.insert(0, "0")
        e1.grid(row=row, column=1, sticky="we", padx=4, pady=2)
        self.entries[label1] = e1
        
        tk.Label(self.interior, text=label2).grid(row=row, column=2, sticky="w", padx=4, pady=2)
        e2 = tk.Entry(self.interior)
        e2.insert(0, "0")
        e2.grid(row=row, column=3, sticky="we", padx=4, pady=2)
        self.entries[label2] = e2
        
        tk.Label(self.interior, text=label3).grid(row=row, column=4, sticky="w", padx=4, pady=2)
        e3 = tk.Entry(self.interior)
        e3.insert(0, "0")
        e3.grid(row=row, column=5, sticky="we", padx=4, pady=2)
        self.entries[label3] = e3

    # ---------------------------
    # LECTURA Y CÁLCULOS
    # ---------------------------
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
        if "Suma ConsignacionesXMes" in self.entries:
            self.entries["Suma ConsignacionesXMes"].delete(0, tk.END)
            self.entries["Suma ConsignacionesXMes"].insert(0, str(sumaConsig))

    def boton_calcular_Acumconsignaciones(self):
        print("Clicked calculo de acumulado consignacionesXaño")
        self.get_datos_window()
        try:
           anterior = float(self.datos.get("Acumulado Consignaciones Anterior", 0) or 0)
           x_mes = float(self.datos.get("Suma ConsignacionesXMes", 0) or 0)

           nuevo = anterior + x_mes

           print(f"AcumConsignacionesNew: {nuevo}")

           # Guardar en el diccionario
           self.datos["Nuevo Acumulado Consignaciones"] = str(nuevo)

           # Mostrar el resultado en la ventana
           if "Nuevo Acumulado Consignaciones" in self.entries:
              self.entries["Nuevo Acumulado Consignaciones"].delete(0, tk.END)
              self.entries["Nuevo Acumulado Consignaciones"].insert(0, str(nuevo))

        except ValueError:
           print("Error: uno de los valores no es numérico.")

    def boton_calcular_Acuminverisones(self):
        print("Clicked calculo de acumulado incersionesXaño")
        self.get_datos_window()
        try:
           anterior = float(self.datos.get("Acumulado Inversiones Anterior", 0) or 0)
           x_mes = float(self.datos.get("Apertura inversiones en Mes", 0) or 0)

           nuevo = anterior + x_mes

           print(f"AcumInverionesNew: {nuevo}")

           # Guardar en el diccionario
           self.datos["Nuevo Acumulado Inversiones"] = str(nuevo)

           # Mostrar el resultado en la ventana
           if "Nuevo Acumulado Consignaciones" in self.entries:
              self.entries["Nuevo Acumulado Inversiones"].delete(0, tk.END)
              self.entries["Nuevo Acumulado Inversiones"].insert(0, str(nuevo))

        except ValueError:
           print("Error: uno de los valores no es numérico.")

    def boton_sumar_prestamos(self):
        print("Clicked Suma de prestamos")
        self.get_datos_window()

        calculadora = Calculadora()

        sumaPrestamos = calculadora.sumaPrestamos(
            self.datos['Prestamo1'],
            self.datos['Prestamo2'],
            self.datos['Prestamo3'],
            self.datos['Prestamo4'],
        )

        print(f"Suma de prestamo: {sumaPrestamos}")

        if "Total Prestamos" in self.entries:
            self.entries["Total Prestamos"].delete(0, tk.END)
            self.entries["Total Prestamos"].insert(0, str(sumaPrestamos))

    def boton_sumar_acumulado(self):
        print("Clicked Suma de acumulado")
        self.get_datos_window()

        calculadora = Calculadora()

        acumTotal = calculadora.AcumTotal(
            self.datos['Nuevo Acumulado Consignaciones'],
            self.datos['Nuevo Acumulado Inversiones']
        )

        print(f"Acumulado total: {acumTotal}")

        if "Acum Consigna+Inversiones" in self.entries:
            self.entries["Acum Consigna+Inversiones"].delete(0, tk.END)
            self.entries["Acum Consigna+Inversiones"].insert(0, str(acumTotal))

    def evento_boton_confirmar_datos(self):
        print("Clicked Confirmar Datos")
        self.get_datos_window()
        calculadora = Calculadora()
        print(self.datos['Efectivo actual'])
         
        activos = calculadora.activos(self.datos['Efectivo actual'], 
                                    self.datos['Valor Actual Cuenta1'], 
                                    self.datos['Valor Actual Cuenta2'], 
                                    self.datos['Valor Actual Cuenta3'], 
                                    self.datos['Valor Actual Cuenta4'], 
                                    self.datos['Inversion 1?'], 
                                    self.datos['Inversion 2?'], 
                                    self.datos['Inversion 3?'],
                                    self.datos['Inversion 4?'],
                                    self.datos['Inversion 5?'],
                                    self.datos['Inversion 6?'],
                                    self.datos['Otra moneda'])

        str_total_ac = str(activos)

        patrimonio = calculadora.patrimonio(str_total_ac, self.datos['Total Prestamos'])

        print(f"Resultado: {activos}")
        print(f"Patrimonio: {patrimonio}") 
        

        Datos = f"""
        Mes: {self.datos['Mes']} 
        ******************************* 
        Efectivo: {self.datos['Efectivo actual']}
        ObsEfectivo: {self.datos['Obs Efect']}
        ******************************* 
        Nombre Cuenta de ahorro1: {self.datos['Nombre Cuenta de ahorro 1']}
        Valor Actual Cuenta1: {self.datos['Valor Actual Cuenta1']}
        ConsignacionesXMesC1: {self.datos['Consignaciones Mes CA1']}
        --------
        Nombre Cuenta de ahorro2: {self.datos['Nombre Cuenta de ahorro 2']}
        Valor Actual Cuenta2: {self.datos['Valor Actual Cuenta2']} 
        ConsignacionesXMesC2: {self.datos['Consignaciones Mes CA2']}
        --------
        Nombre Cuenta de ahorro3: {self.datos['Nombre Cuenta de ahorro 3']}
        Valor Actual Cuenta3: {self.datos['Valor Actual Cuenta3']} 
        ConsignacionesXMesC3: {self.datos['Consignaciones Mes CA3']}
        --------
        Nombre Cuenta de ahorro4: {self.datos['Nombre Cuenta de ahorro 4']}
        Valor Actual Cuenta4: {self.datos['Valor Actual Cuenta4']} 
        ConsignacionesXMesC4: {self.datos['Consignaciones Mes CA4']}
        --------
        Suma ConsignacionesXMes: {self.datos['Suma ConsignacionesXMes']}
        ObsCuentaAhorro: {self.datos['Obs Cuentas de ahorro']}
        Acumulado Consignaciones Anterior: {self.datos['Acumulado Consignaciones Anterior']}
        Nuevo Acumulado Consignaciones: {self.datos['Nuevo Acumulado Consignaciones']}
        ******************************* 
        Otra Moneda: {self.datos['Otra moneda']}
        ObsOM: {self.datos['Obs OMon']}
        ************************************* 
        Inversion1: {self.datos['Inversion 1?']}
        Entidad1: {self.datos['Entidad 1?']}
        ObsInv1: {self.datos['Obs Inv1']}
        -------
        Inversion2: {self.datos['Inversion 2?']}
        Entidad2: {self.datos['Entidad 2?']}
        ObsInv2: {self.datos['Obs Inv2']}
        -------
        Inversion3: {self.datos['Inversion 3?']}
        Entidad3: {self.datos['Entidad 3?']}
        ObsInv3: {self.datos['Obs Inv3']}
        -------
        Inversion4: {self.datos['Inversion 4?']}
        Entidad4: {self.datos['Entidad 4?']}
        ObsInv4: {self.datos['Obs Inv4']}
        -------
        Inversion5: {self.datos['Inversion 5?']}
        Entidad5: {self.datos['Entidad 5?']}
        ObsInv5: {self.datos['Obs Inv5']}
        -------
        Inversion6: {self.datos['Inversion 6?']}
        Entidad6: {self.datos['Entidad 6?']}
        ObsInv6: {self.datos['Obs Inv6']}
        -------
        ObsInversiones: {self.datos['Obs Inversiones']}
        AperturaInversiones: {self.datos['Apertura inversiones en Mes']}
        Acumulado Inversiones Anterior: {self.datos['Acumulado Inversiones Anterior']}
        Nuevo Acumulado Inversiones: {self.datos['Nuevo Acumulado Inversiones']}
        **************************************
        Compras: {self.datos['Compras?']}
        ObsCompra: {self.datos['Obs Compras']}
        Gastos: {self.datos['Gastos?']}
        ObsGastos: {self.datos['Obs Gastos']}
        **************************************
        Prestamo1: {self.datos['Prestamo1']}
        NamePres1: {self.datos['nameP1']}
        ObsPres1: {self.datos['Obs Pres1']}
        -------
        Prestamo2: {self.datos['Prestamo2']}
        NamePres2: {self.datos['nameP2']}
        ObsPres2: {self.datos['Obs Pres2']}
        -------
        Prestamo3: {self.datos['Prestamo3']}
        NamePres3: {self.datos['nameP3']}
        ObsPres3: {self.datos['Obs Pres3']}
        -------
        Prestamo4: {self.datos['Prestamo4']}
        NamePres4: {self.datos['nameP4']}
        ObsPres4: {self.datos['Obs Pres4']}
        -------
        Total Prestamos: {self.datos['Total Prestamos']} 
        ***************************************
        Activos: {activos}
        Pasivos: {self.datos['Total Prestamos']}
        Patrimonio: {patrimonio}
        ******************************* 
        Observaciones: {self.datos['Observaciones Adicionales']}
        Acum Consigna+Inversiones: {self.datos['Acum Consigna+Inversiones']}
        """
        # clic “Confirmar” crea nueva ventana totalmente nueva sin instancia.
        ventana = VistaConfirm(self.top)
        ventana.set_label2_text(Datos)
        ventana.mostrar()
        # tamaño ventana (solo si somos dueños)
        if self._owns_root:
            try:
                self.top.geometry("900x900")
            except Exception:
                pass

    # VENTANA CARGA (VistaLoad)
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
        self.lineas_recibidas = lineas

        # Diccionario: clave = label del Entry, valor = índice en self.lineas_recibidas
        mapa_actualizacion = {
            "Mes": 1,
            "Efectivo actual": 3, 
            "Obs Efect": 4,

            "Nombre Cuenta de ahorro 1": 6,
            "Valor Actual Cuenta1": 7,
            "Consignaciones Mes CA1": 8, 

            "Nombre Cuenta de ahorro 2": 10,
            "Valor Actual Cuenta2": 11,
            "Consignaciones Mes CA2": 12,
            
            "Nombre Cuenta de ahorro 3": 14,
            "Valor Actual Cuenta3": 15, 
            "Consignaciones Mes CA3": 16,
            
            "Nombre Cuenta de ahorro 4": 18,
            "Valor Actual Cuenta4": 19, 
            "Consignaciones Mes CA4": 20,
            
            "Suma ConsignacionesXMes": 22,
            "Obs Cuentas de ahorro": 23,
            "Acumulado Consignaciones Anterior": 24,
            "Nuevo Acumulado Consignaciones": 25, 

            "Otra moneda": 27,
            "Obs OMon": 28,

            "Inversion 1?": 30,
            "Entidad 1?": 31,
            "Obs Inv1": 32,

            "Inversion 2?": 34,
            "Entidad 2?": 35,
            "Obs Inv2": 36,

            "Inversion 3?": 38,
            "Entidad 3?": 39,
            "Obs Inv3": 40,

            "Inversion 4?": 42,
            "Entidad 4?": 43,
            "Obs Inv4": 44,

            "Inversion 5?": 46,
            "Entidad 5?": 47,
            "Obs Inv5": 48,

            "Inversion 6?": 50,
            "Entidad 6?": 51,
            "Obs Inv6": 52,

            "Obs Inversiones": 54,
            "Apertura inversiones en Mes": 55,
            "Acumulado Inversiones Anterior": 56,
            "Nuevo Acumulado Inversiones": 57, 

            "Compras?": 59,
            "Obs Compras": 60,
            "Gastos?": 61,
            "Obs Gastos": 62,

            "Prestamo1": 64,
            "nameP1": 65,
            "Obs Pres1": 66,

            "Prestamo2": 68,
            "nameP2": 69,
            "Obs Pres2": 70,

            "Prestamo3": 72,
            "nameP3": 73,
            "Obs Pres3": 74,

            "Prestamo4": 76,
            "nameP4": 77,
            "Obs Pres4": 78,

            "Total Prestamos": 80,
            
            "Observaciones Adicionales": 86,
            "Acum Consigna+Inversiones": 87
        }

        for label, posicion in mapa_actualizacion.items():
            self.actualizar_interfaz(label, posicion)
        
    def actualizar_interfaz(self, label, posicion):
        if posicion >= len(self.lineas_recibidas):
            print(f"Posición {posicion} fuera de rango en lineas_recibidas")
            return

        linea = self.lineas_recibidas[posicion]
        if ":" in linea:
            valor = linea.split(":", 1)[1].strip()
        else:
            valor = linea.strip()

        if label in self.entries:
            entry = self.entries[label]
            entry.delete(0, tk.END)
            entry.insert(0, valor)
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
    app = ApliCuentas(None)
    app.run()
