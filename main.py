"""
ANALIZADOR DE ESTUDIANTES -- PROGRAMACION FUNCIONAL
Diseno: tonos frios / claros, estilo desktop app
Temas: Artico - Pizarra - Bruma - Acero - Noche
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import csv
import os
from functools import reduce
from itertools import groupby, islice
from operator import itemgetter
import math

# ================================================================
#   SISTEMA DE TEMAS -- tonos frios/claros + uno oscuro
# ================================================================

TEMAS = {
    "Artico": {
        "bg_raiz":      "#EEF2F7",
        "bg_panel":     "#FFFFFF",
        "bg_sidebar":   "#F4F7FB",
        "bg_tarjeta":   "#FFFFFF",
        "bg_input":     "#EEF2F7",
        "bg_header":    "#FFFFFF",
        "borde":        "#D1DCF0",
        "acento":       "#2B7FFF",
        "acento2":      "#E05C6A",
        "acento3":      "#1BAB7F",
        "warning":      "#E8960A",
        "texto":        "#1A2640",
        "texto_dim":    "#6B7FA3",
        "fila_par":     "#F7F9FD",
        "fila_impar":   "#FFFFFF",
        "sel":          "#D6E8FF",
        "aprobado":     "#1BAB7F",
        "desaprobado":  "#E05C6A",
        "excelente":    "#2B7FFF",
    },
    "Pizarra": {
        "bg_raiz":      "#E8EDF4",
        "bg_panel":     "#F2F5FA",
        "bg_sidebar":   "#E2E8F3",
        "bg_tarjeta":   "#FFFFFF",
        "bg_input":     "#DDE3EF",
        "bg_header":    "#F2F5FA",
        "borde":        "#C5CFDF",
        "acento":       "#3A5FC8",
        "acento2":      "#C94E6A",
        "acento3":      "#228B6A",
        "warning":      "#C97D0A",
        "texto":        "#1C2B45",
        "texto_dim":    "#5C6F8C",
        "fila_par":     "#EEF2F8",
        "fila_impar":   "#F8FAFB",
        "sel":          "#C5D7F7",
        "aprobado":     "#228B6A",
        "desaprobado":  "#C94E6A",
        "excelente":    "#3A5FC8",
    },
    "Bruma": {
        "bg_raiz":      "#ECF0F5",
        "bg_panel":     "#FAFBFD",
        "bg_sidebar":   "#E5EBF5",
        "bg_tarjeta":   "#FAFBFD",
        "bg_input":     "#E0E7F0",
        "bg_header":    "#FAFBFD",
        "borde":        "#C8D4E8",
        "acento":       "#5B8DEF",
        "acento2":      "#E0636F",
        "acento3":      "#2AA67A",
        "warning":      "#D4870C",
        "texto":        "#1E2E48",
        "texto_dim":    "#7284A0",
        "fila_par":     "#F0F4FA",
        "fila_impar":   "#FAFBFD",
        "sel":          "#C9DAFA",
        "aprobado":     "#2AA67A",
        "desaprobado":  "#E0636F",
        "excelente":    "#5B8DEF",
    },
    "Acero": {
        "bg_raiz":      "#DDE4EE",
        "bg_panel":     "#EEF2F8",
        "bg_sidebar":   "#D8DEE9",
        "bg_tarjeta":   "#F5F7FB",
        "bg_input":     "#D3D9E6",
        "bg_header":    "#EEF2F8",
        "borde":        "#B8C5D8",
        "acento":       "#2469CC",
        "acento2":      "#BB4055",
        "acento3":      "#1A8C62",
        "warning":      "#BB7A10",
        "texto":        "#162035",
        "texto_dim":    "#546078",
        "fila_par":     "#E5EBF4",
        "fila_impar":   "#EEF2F8",
        "sel":          "#BBCFED",
        "aprobado":     "#1A8C62",
        "desaprobado":  "#BB4055",
        "excelente":    "#2469CC",
    },
    "Noche": {
        "bg_raiz":      "#141921",
        "bg_panel":     "#1C2330",
        "bg_sidebar":   "#19202D",
        "bg_tarjeta":   "#222C3C",
        "bg_input":     "#2A3547",
        "bg_header":    "#1C2330",
        "borde":        "#2E3D54",
        "acento":       "#4C9BFF",
        "acento2":      "#FF6680",
        "acento3":      "#3DD9A4",
        "warning":      "#FFC56A",
        "texto":        "#D8E4F5",
        "texto_dim":    "#6E859E",
        "fila_par":     "#1F2B3C",
        "fila_impar":   "#222C3C",
        "sel":          "#2B4A7A",
        "aprobado":     "#3DD9A4",
        "desaprobado":  "#FF6680",
        "excelente":    "#4C9BFF",
    },
}

TEMA_ACTUAL = "Artico"

FUENTES = {
    "titulo":   ("Segoe UI", 15, "bold"),
    "subtit":   ("Segoe UI", 10, "bold"),
    "normal":   ("Segoe UI", 9),
    "small":    ("Segoe UI", 8),
    "mono":     ("Consolas", 9),
    "badge":    ("Segoe UI", 8, "bold"),
    "stat_val": ("Segoe UI", 16, "bold"),
    "stat_lbl": ("Segoe UI", 8),
}

# ----------------------------------------------------------------
# Datos de ejemplo
# ----------------------------------------------------------------

DATOS_DEFAULT = [
    {"nombre": "Ana Lopez",       "dni": "45123890", "carrera": "Sistemas",   "semestre": 5,  "notas": [18,17,20,19]},
    {"nombre": "Luis Perez",      "dni": "47234901", "carrera": "Industrial", "semestre": 3,  "notas": [10,12,11,9]},
    {"nombre": "Maria Torres",    "dni": "48345012", "carrera": "Civil",      "semestre": 7,  "notas": [14,15,13,16]},
    {"nombre": "Jose Ramirez",    "dni": "46456123", "carrera": "Sistemas",   "semestre": 2,  "notas": [20,19,18,20]},
    {"nombre": "Pedro Vargas",    "dni": "43567234", "carrera": "Electrica",  "semestre": 9,  "notas": [8,9,10,7]},
    {"nombre": "Lucia Flores",    "dni": "44678345", "carrera": "Sistemas",   "semestre": 4,  "notas": [17,16,18,17]},
    {"nombre": "Carlos Rios",     "dni": "49789456", "carrera": "Industrial", "semestre": 6,  "notas": [12,11,13,12]},
    {"nombre": "Sofia Castillo",  "dni": "41890567", "carrera": "Civil",      "semestre": 8,  "notas": [19,18,20,19]},
    {"nombre": "Miguel Morales",  "dni": "42901678", "carrera": "Electrica",  "semestre": 1,  "notas": [13,14,12,13]},
    {"nombre": "Elena Salinas",   "dni": "40012789", "carrera": "Sistemas",   "semestre": 10, "notas": [15,16,15,14]},
    {"nombre": "Diego Fuentes",   "dni": "48123890", "carrera": "Civil",      "semestre": 3,  "notas": [11,10,9,12]},
    {"nombre": "Valeria Soto",    "dni": "47234901", "carrera": "Industrial", "semestre": 5,  "notas": [18,19,17,20]},
    {"nombre": "Andres Mora",     "dni": "45345012", "carrera": "Electrica",  "semestre": 7,  "notas": [16,15,17,16]},
    {"nombre": "Camila Vega",     "dni": "46456123", "carrera": "Sistemas",   "semestre": 2,  "notas": [9,8,11,10]},
    {"nombre": "Fernando Cruz",   "dni": "44567234", "carrera": "Civil",      "semestre": 9,  "notas": [20,20,19,18]},
]

# ================================================================
#   BLOQUE 1 -- FUNCIONES PURAS
# ================================================================

def calcular_promedio(notas: list) -> float:
    """FUNCION PURA."""
    return sum(notas) / len(notas) if notas else 0.0

def determinar_estado(promedio: float) -> str:
    """FUNCION PURA."""
    if promedio >= 17:   return "Excelente"
    elif promedio >= 13: return "Aprobado"
    else:                return "Desaprobado"

def calcular_max(notas: list) -> float:
    """FUNCION PURA."""
    return max(notas) if notas else 0.0

def calcular_min(notas: list) -> float:
    """FUNCION PURA."""
    return min(notas) if notas else 0.0

# ================================================================
#   BLOQUE 2 -- COMPOSICION DE FUNCIONES
# ================================================================

def pipe(*fns):
    """COMPOSICION: encadena funciones de izquierda a derecha."""
    return lambda x: reduce(lambda v, f: f(v), fns, x)

def compose(*fns):
    """COMPOSICION: encadena de derecha a izquierda."""
    return lambda x: reduce(lambda v, f: f(v), reversed(fns), x)

enriquecer = lambda est: {
    **est,
    "promedio": calcular_promedio(est["notas"]),
    "estado":   determinar_estado(calcular_promedio(est["notas"])),
    "max":      calcular_max(est["notas"]),
    "min":      calcular_min(est["notas"]),
}

# ================================================================
#   BLOQUE 3 -- HOF + CLOSURES
# ================================================================

def filtrar_por_estado(estado: str):
    """HOF + CLOSURE."""
    return lambda e: e["estado"] == estado

def filtrar_por_carrera(carrera: str):
    """HOF + CLOSURE."""
    return lambda e: e["carrera"].lower() == carrera.lower()

def filtrar_por_semestre(sem: int):
    """HOF + CLOSURE."""
    return lambda e: e["semestre"] == sem

def filtrar_por_ranking(fraccion: float, lista_base: list):
    """
    HOF + CLOSURE: retorna predicado que acepta solo los estudiantes
    en el top (fraccion * 100)% del ranking de la lista_base dada.
    """
    ordenada   = sorted(lista_base, key=lambda e: e["promedio"], reverse=True)
    n_top      = max(1, math.ceil(len(ordenada) * fraccion))
    claves_top = set((e["nombre"], e["dni"]) for e in ordenada[:n_top])
    return lambda e: (e["nombre"], e["dni"]) in claves_top

def filtrar_primer_lugar(lista_base: list):
    """HOF + CLOSURE: solo el/la estudiante con mayor promedio."""
    if not lista_base:
        return lambda e: False
    max_prom = max(lista_base, key=lambda e: e["promedio"])["promedio"]
    return lambda e: e["promedio"] == max_prom

def ordenar_por(campo: str, desc: bool = True):
    """HOF."""
    return lambda lista: sorted(lista, key=lambda e: e[campo], reverse=desc)

def buscar_funcional(termino: str):
    """HOF + CLOSURE."""
    t = termino.lower().strip()
    return lambda e: (
        t in e["nombre"].lower()  or
        t in e["dni"]             or
        t in e["carrera"].lower() or
        t in e["estado"].lower()  or
        t in str(e["semestre"])
    )

def combinar_filtros(*predicados):
    """COMPOSICION DE PREDICADOS: AND logico de N filtros."""
    return lambda e: reduce(lambda acc, p: acc and p(e), predicados, True)

# ================================================================
#   BLOQUE 4 -- MAP / FILTER / REDUCE
# ================================================================

def aplicar_map(lista, fn):
    """MAP puro."""
    return list(map(fn, lista))

def aplicar_filter(lista, pred):
    """FILTER puro."""
    return list(filter(pred, lista))

def aplicar_reduce(lista, fn, ini=0):
    """REDUCE."""
    return reduce(fn, lista, ini)

# ================================================================
#   BLOQUE 5 -- ESTADISTICAS CON REDUCE + itertools
# ================================================================

def calcular_estadisticas(data: list) -> dict:
    """REDUCE + FILTER + MAP. Funcion pura."""
    if not data:
        return {}
    promedios = aplicar_map(data, lambda e: e["promedio"])
    total     = len(promedios)
    suma      = aplicar_reduce(promedios, lambda a, b: a + b, 0)
    prom_gral = suma / total
    maximo    = aplicar_reduce(promedios, lambda a, b: a if a > b else b, promedios[0])
    minimo    = aplicar_reduce(promedios, lambda a, b: a if a < b else b, promedios[0])
    return {
        "total":        total,
        "promedio":     round(prom_gral, 2),
        "maximo":       round(maximo, 2),
        "minimo":       round(minimo, 2),
        "excelentes":   len(aplicar_filter(data, filtrar_por_estado("Excelente"))),
        "aprobados":    len(aplicar_filter(data, filtrar_por_estado("Aprobado"))),
        "desaprobados": len(aplicar_filter(data, filtrar_por_estado("Desaprobado"))),
        "decimo_sup":   max(1, math.ceil(total * 0.10)),
        "quinto_sup":   max(1, math.ceil(total * 0.20)),
        "tercio_sup":   max(1, math.ceil(total * 0.33)),
    }

def agrupar_por_carrera(data: list) -> dict:
    """itertools.groupby."""
    ordenados = sorted(data, key=itemgetter("carrera"))
    return {
        carrera: list(grupo)
        for carrera, grupo in groupby(ordenados, key=itemgetter("carrera"))
    }

def top_n(lista, n=5):
    """itertools.islice."""
    return list(islice(iter(lista), n))

# ================================================================
#   BLOQUE 6 -- CARGA DE CSV
# ================================================================

def parsear_fila(fila: dict):
    """FUNCION PURA."""
    try:
        claves_notas = [k for k in fila if k.lower().startswith("nota")]
        notas = [float(fila[k]) for k in claves_notas if fila[k].strip()]
        if not notas:
            return None
        return {
            "nombre":   fila.get("nombre",   fila.get("Nombre",   "-")).strip(),
            "dni":      fila.get("dni",      fila.get("DNI",      "00000000")).strip(),
            "carrera":  fila.get("carrera",  fila.get("Carrera",  "-")).strip(),
            "semestre": int(fila.get("semestre", fila.get("Semestre", 1))),
            "notas":    notas,
        }
    except (ValueError, KeyError):
        return None

def cargar_csv(ruta: str) -> list:
    """MAP + FILTER."""
    with open(ruta, newline="", encoding="utf-8-sig") as f:
        filas = list(csv.DictReader(f))
    parseadas = aplicar_map(filas, parsear_fila)
    validas   = aplicar_filter(parseadas, lambda x: x is not None)
    return validas

def generar_csv_ejemplo(ruta: str, n: int = 200):
    """Genera CSV de ejemplo."""
    import random
    nombres   = ["Gabriel","Sofia","Lucas","Valentina","Diego","Camila","Andres",
                 "Maria","Felipe","Ana","Carlos","Elena","Luis","Paula","Tomas",
                 "Renata","Matias","Rodrigo","Antonella","Emilio","Marcelo","Irene"]
    apellidos = ["Torres","Vega","Rios","Fuentes","Mora","Cruz","Soto","Reyes",
                 "Herrera","Mendoza","Castillo","Vargas","Lopez","Perez","Garcia"]
    carreras  = ["Sistemas","Civil","Industrial","Electrica","Mecanica","Quimica","Ambiental"]
    with open(ruta, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["nombre","dni","carrera","semestre","nota1","nota2","nota3","nota4"])
        for i in range(n):
            nombre = f"{random.choice(nombres)} {random.choice(apellidos)}"
            dni    = str(random.randint(10_000_000, 99_999_999))
            car    = random.choice(carreras)
            sem    = random.randint(1, 10)
            notas  = [max(0, min(20, int(random.gauss(13.5, 3.8)))) for _ in range(4)]
            w.writerow([nombre, dni, car, sem] + notas)

# ================================================================
#   BLOQUE 7 -- ESTADO INMUTABLE
# ================================================================

FILTROS_RAPIDOS = [
    "Todos",
    "Excelentes",
    "Aprobados",
    "Desaprobados",
    "Ranking abajo",
    "Decimo superior",
    "Quinto superior",
    "Tercio superior",
    "Primeros lugares",
]

class EstadoApp:
    """Contenedor de estado con inmutabilidad funcional."""
    def __init__(self):
        self.datos_base:    list = aplicar_map(DATOS_DEFAULT, enriquecer)
        self.datos_activos: list = self.datos_base[:]
        self.ruta_csv:      str  = ""

    def cargar(self, ruta: str):
        crudos             = cargar_csv(ruta)
        self.datos_base    = aplicar_map(crudos, enriquecer)
        self.datos_activos = self.datos_base[:]
        self.ruta_csv      = ruta

    def reset(self):
        self.datos_base    = aplicar_map(DATOS_DEFAULT, enriquecer)
        self.datos_activos = self.datos_base[:]
        self.ruta_csv      = ""


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.estado     = EstadoApp()
        self._orden_inv = {}
        self._configurar_ventana()
        self._construir_ui()
        self._refrescar_tabla(self.estado.datos_base)
        self._actualizar_sidebar()


    def _t(self, k: str) -> str:
        return TEMAS[TEMA_ACTUAL][k]

    def _configurar_ventana(self):
        self.title("AnalizadorFP -- Programacion Funcional")
        self.geometry("1180x700")
        self.minsize(980, 580)
        self.configure(bg=self._t("bg_raiz"))

    def _aplicar_tema(self):
        global TEMA_ACTUAL
        TEMA_ACTUAL = self.var_tema.get()
        for w in self.winfo_children():
            w.destroy()
        self._construir_ui()
        self._refrescar_tabla(self.estado.datos_base)
        self._actualizar_sidebar()

 
    def _construir_ui(self):
        self._barra_titulo()
        self._cuerpo()
        self._barra_estado()

    def _barra_titulo(self):
        bar = tk.Frame(self, bg=self._t("bg_header"),
                       highlightbackground=self._t("borde"), highlightthickness=1)
        bar.pack(fill="x", side="top")

        izq = tk.Frame(bar, bg=self._t("bg_header"))
        izq.pack(side="left", padx=14, pady=9)
        tk.Label(izq, text="AnalizadorFP", font=FUENTES["titulo"],
                 bg=self._t("bg_header"), fg=self._t("texto")).pack(side="left")
        tk.Label(izq, text="   map - filter - reduce - compose - HOF - closure",
                 font=FUENTES["small"],
                 bg=self._t("bg_header"), fg=self._t("texto_dim")).pack(side="left", pady=2)

        der = tk.Frame(bar, bg=self._t("bg_header"))
        der.pack(side="right", padx=14, pady=9)

        tk.Label(der, text="Tema:", font=FUENTES["small"],
                 bg=self._t("bg_header"), fg=self._t("texto_dim")).pack(side="left", padx=(0,3))
        self.var_tema = tk.StringVar(value=TEMA_ACTUAL)
        ttk.Combobox(der, textvariable=self.var_tema, values=list(TEMAS.keys()),
                     font=FUENTES["small"], width=9, state="readonly").pack(side="left", padx=(0,10))
        self.var_tema.trace_add("write", lambda *_: self._aplicar_tema())

        for texto, cmd, col in [
            ("Cargar CSV",  self._cargar_csv,  "acento"),
            ("Ejemplo CSV", self._gen_ejemplo,  "acento3"),
            ("Exportar",    self._exportar,     "warning"),
            ("Restablecer", self._reset,        "acento2"),
        ]:
            self._btn(der, texto, cmd, col).pack(side="left", padx=3)

        self.lbl_fuente = tk.Label(der, text=" [ejemplo]", font=FUENTES["small"],
                                   bg=self._t("bg_header"), fg=self._t("texto_dim"))
        self.lbl_fuente.pack(side="left", padx=6)

    def _cuerpo(self):
        frame = tk.Frame(self, bg=self._t("bg_raiz"))
        frame.pack(fill="both", expand=True)
        self._sidebar(frame)
        self._panel_principal(frame)

    def _sidebar(self, padre):
        sb = tk.Frame(padre, bg=self._t("bg_sidebar"), width=215,
                      highlightbackground=self._t("borde"), highlightthickness=1)
        sb.pack(side="left", fill="y")
        sb.pack_propagate(False)

        def seccion(label, color):
            tk.Label(sb, text=label, font=FUENTES["badge"],
                     bg=self._t("bg_sidebar"), fg=color, anchor="w"
                     ).pack(fill="x", padx=14, pady=(14,2))
            tk.Frame(sb, bg=color, height=1).pack(fill="x", padx=14, pady=(0,6))

        seccion("ESTADISTICAS", self._t("acento"))
        self.frame_stats = tk.Frame(sb, bg=self._t("bg_sidebar"))
        self.frame_stats.pack(fill="x", padx=12)

        seccion("RANKING TOP 5", self._t("acento2"))
        self.frame_top = tk.Frame(sb, bg=self._t("bg_sidebar"))
        self.frame_top.pack(fill="x", padx=12)

        seccion("POR CARRERA", self._t("acento3"))
        self.frame_carrera = tk.Frame(sb, bg=self._t("bg_sidebar"))
        self.frame_carrera.pack(fill="x", padx=12)

    def _panel_principal(self, padre):
        panel = tk.Frame(padre, bg=self._t("bg_raiz"))
        panel.pack(side="left", fill="both", expand=True, padx=10, pady=8)
        self._barra_herramientas(panel)
        self._construir_tabla(panel)

    def _barra_herramientas(self, padre):
        bar = tk.Frame(padre, bg=self._t("bg_panel"),
                       highlightbackground=self._t("borde"), highlightthickness=1)
        bar.pack(fill="x", pady=(0, 6))

        # Buscador
        tk.Label(bar, text="Buscar:", font=FUENTES["normal"],
                 bg=self._t("bg_panel"), fg=self._t("texto_dim")
                 ).pack(side="left", padx=(8,2), pady=7)
        self.var_busqueda = tk.StringVar()
        self.var_busqueda.trace_add("write", self._on_busqueda)  # CLOSURE reactivo
        tk.Entry(bar, textvariable=self.var_busqueda,
                 font=FUENTES["normal"], bg=self._t("bg_input"), fg=self._t("texto"),
                 relief="flat", bd=1, insertbackground=self._t("acento"),
                 highlightbackground=self._t("borde"), highlightthickness=1
                 ).pack(side="left", fill="x", expand=True, ipady=4, padx=(0,8), pady=6)

        tk.Frame(bar, bg=self._t("borde"), width=1).pack(side="left", fill="y", padx=2)

        # Filtro rapido estado/ranking
        tk.Label(bar, text="Filtro:", font=FUENTES["small"],
                 bg=self._t("bg_panel"), fg=self._t("texto_dim")).pack(side="left", padx=(4,2))
        self.var_filtro_rapido = tk.StringVar(value="Todos")
        self.combo_filtro = ttk.Combobox(
            bar, textvariable=self.var_filtro_rapido,
            values=FILTROS_RAPIDOS,
            font=FUENTES["small"], width=16, state="readonly"
        )
        self.combo_filtro.pack(side="left", padx=(0,6), pady=5)
        self.combo_filtro.bind("<<ComboboxSelected>>", self._on_filtro_rapido)

        tk.Frame(bar, bg=self._t("borde"), width=1).pack(side="left", fill="y", padx=4)

        # Filtro carrera
        tk.Label(bar, text="Carrera:", font=FUENTES["small"],
                 bg=self._t("bg_panel"), fg=self._t("texto_dim")).pack(side="left")
        self.var_carrera = tk.StringVar(value="Todas")
        self.combo_carrera = ttk.Combobox(bar, textvariable=self.var_carrera,
                                          font=FUENTES["small"], width=12, state="readonly")
        self.combo_carrera.pack(side="left", padx=(3,8), pady=5)
        self.combo_carrera.bind("<<ComboboxSelected>>", self._on_filtro_carrera)

        # Filtro semestre
        tk.Label(bar, text="Semestre:", font=FUENTES["small"],
                 bg=self._t("bg_panel"), fg=self._t("texto_dim")).pack(side="left")
        self.var_semestre = tk.StringVar(value="Todos")
        self.combo_sem = ttk.Combobox(bar, textvariable=self.var_semestre,
                                      values=["Todos"]+[str(i) for i in range(1,11)],
                                      font=FUENTES["small"], width=6, state="readonly")
        self.combo_sem.pack(side="left", padx=(3,8), pady=5)
        self.combo_sem.bind("<<ComboboxSelected>>", self._on_filtro_semestre)

        # Boton limpiar todos
        self._btn(bar, "Limpiar", self._mostrar_todos, "acento2").pack(
            side="left", padx=(0,6), pady=5)

    def _construir_tabla(self, padre):
        frame = tk.Frame(padre, bg=self._t("bg_panel"),
                         highlightbackground=self._t("borde"), highlightthickness=1)
        frame.pack(fill="both", expand=True)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("FP.Treeview",
                        background=self._t("fila_impar"), foreground=self._t("texto"),
                        fieldbackground=self._t("fila_impar"), rowheight=24,
                        font=FUENTES["normal"], borderwidth=0)
        style.configure("FP.Treeview.Heading",
                        background=self._t("bg_input"), foreground=self._t("texto"),
                        font=FUENTES["badge"], relief="flat", borderwidth=0)
        style.map("FP.Treeview",
                  background=[("selected", self._t("sel"))],
                  foreground=[("selected", self._t("texto"))])
        style.layout("FP.Treeview", [("FP.Treeview.treearea", {"sticky": "nswe"})])

        cols = ("idx","nombre","dni","carrera","semestre","promedio","max","min","estado","ranking")
        self.tabla = ttk.Treeview(frame, columns=cols, show="headings", style="FP.Treeview")

        defs = [
            ("idx",      "#",         40, "center"),
            ("nombre",   "Nombre",   185, "w"),
            ("dni",      "DNI",       88, "center"),
            ("carrera",  "Carrera",  105, "center"),
            ("semestre", "Semestre",  65, "center"),
            ("promedio", "Promedio",  72, "center"),
            ("max",      "Max",       48, "center"),
            ("min",      "Min",       48, "center"),
            ("estado",   "Estado",    90, "center"),
            ("ranking",  "Posicion", 105, "center"),
        ]
        for col, encab, ancho, anc in defs:
            self.tabla.heading(col, text=encab, command=lambda c=col: self._ordenar_col(c))
            self.tabla.column(col, width=ancho, anchor=anc, minwidth=36)

        vsb = ttk.Scrollbar(frame, orient="vertical",   command=self.tabla.yview)
        hsb = ttk.Scrollbar(frame, orient="horizontal", command=self.tabla.xview)
        self.tabla.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.tabla.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        self.tabla.tag_configure("Excelente",
            foreground=self._t("excelente"), background=self._t("fila_par"))
        self.tabla.tag_configure("Aprobado",
            foreground=self._t("aprobado"), background=self._t("fila_impar"))
        self.tabla.tag_configure("Desaprobado",
            foreground=self._t("desaprobado"), background=self._t("fila_par"))

    def _barra_estado(self):
        bar = tk.Frame(self, bg=self._t("bg_header"),
                       highlightbackground=self._t("borde"), highlightthickness=1, height=26)
        bar.pack(fill="x", side="bottom")
        bar.pack_propagate(False)
        self.lbl_conteo = tk.Label(bar, text="", font=FUENTES["small"],
                                   bg=self._t("bg_header"), fg=self._t("texto_dim"))
        self.lbl_conteo.pack(side="left", padx=12)
        tk.Label(bar,
                 text="map - filter - reduce - compose - HOF - closure - groupby - islice",
                 font=FUENTES["small"],
                 bg=self._t("bg_header"), fg=self._t("borde")).pack(side="right", padx=12)

    # -- Helpers de posicion relativa (funcionales, puros) -------

    def _calcular_posicion(self, estudiante: dict, lista_base: list) -> str:
        """
        FUNCION PURA: calcula el badge de posicion relativa
        del estudiante dentro de lista_base.
        """
        if not lista_base:
            return ""
        total      = len(lista_base)
        ordenada   = sorted(lista_base, key=lambda e: e["promedio"], reverse=True)
        
        posiciones = {(e["nombre"], e["dni"]): i+1
                      for i, e in enumerate(ordenada)}
        clave      = (estudiante["nombre"], estudiante["dni"])
        pos        = posiciones.get(clave, total)
        pct        = pos / total

        badge = (
            "1er lugar"    if pos == 1    else
            "Decimo sup."  if pct <= 0.10 else
            "Quinto sup."  if pct <= 0.20 else
            "Tercio sup."  if pct <= 0.333 else
            f"#{pos}/{total}"
        )
        return badge

    def _refrescar_tabla(self, lista: list):
        """
        MAP: transforma lista -> filas de visualizacion.
        FIX: ya no llama a _actualizar_combo_carreras() para evitar
        que reasignar 'values' dispare <<ComboboxSelected>> y pise
        los filtros activos de carrera y semestre.
        """
        self.tabla.delete(*self.tabla.get_children())
        self.estado.datos_activos = lista

        filas = aplicar_map(
            list(enumerate(lista, 1)),
            lambda par: (
                par[0],
                par[1]["nombre"],
                par[1]["dni"],
                par[1]["carrera"],
                par[1]["semestre"],
                f"{par[1]['promedio']:.2f}",
                f"{par[1]['max']:.0f}",
                f"{par[1]['min']:.0f}",
                par[1]["estado"],
                self._calcular_posicion(par[1], lista),
            )
        )
        for fila in filas:
            self.tabla.insert("", "end", values=fila, tags=(fila[8],))

        n = len(lista)
        self.lbl_conteo.config(
            text=f"  {n:,} estudiante{'s' if n != 1 else ''} mostrado{'s' if n != 1 else ''}")
        # NOTA: _actualizar_combo_carreras se llama solo al cargar datos
        # nuevos o al restablecer, nunca durante el filtrado.

    def _actualizar_sidebar(self):
        """MAP + REDUCE + groupby."""
        for w in self.frame_stats.winfo_children():   w.destroy()
        for w in self.frame_top.winfo_children():     w.destroy()
        for w in self.frame_carrera.winfo_children(): w.destroy()

        stats = calcular_estadisticas(self.estado.datos_base)
        items = [
            ("Total alumnos",   f"{stats.get('total',0):,}",          self._t("texto")),
            ("Promedio gral.",  f"{stats.get('promedio',0):.2f}",      self._t("acento")),
            ("Nota mas alta",   str(stats.get("maximo", 0)),           self._t("acento3")),
            ("Nota mas baja",   str(stats.get("minimo", 0)),           self._t("acento2")),
            ("Excelentes",      f"{stats.get('excelentes',0):,}",      self._t("excelente")),
            ("Aprobados",       f"{stats.get('aprobados',0):,}",       self._t("aprobado")),
            ("Desaprobados",    f"{stats.get('desaprobados',0):,}",    self._t("desaprobado")),
            ("Decimo superior", f"top {stats.get('decimo_sup',0):,}",  self._t("warning")),
            ("Quinto superior", f"top {stats.get('quinto_sup',0):,}",  self._t("warning")),
            ("Tercio superior", f"top {stats.get('tercio_sup',0):,}",  self._t("warning")),
        ]
        list(map(lambda i: self._stat_fila(self.frame_stats, i[0], i[1], i[2]), items))

        top = top_n(ordenar_por("promedio")(self.estado.datos_base), 5)
        medallas = ["1.","2.","3.","4.","5."]
        list(map(
            lambda p: self._stat_fila(
                self.frame_top,
                f"{p[0]} {p[1]['nombre'].split()[0]}",
                f"{p[1]['promedio']:.2f}",
                self._t("warning")
            ),
            zip(medallas, top)
        ))

        grupos = agrupar_por_carrera(self.estado.datos_base)
        list(map(
            lambda item: self._stat_fila(
                self.frame_carrera, item[0], f"{len(item[1]):,}", self._t("acento3")
            ),
            grupos.items()
        ))

    def _stat_fila(self, padre, lbl, val, color):
        f = tk.Frame(padre, bg=self._t("bg_sidebar"))
        f.pack(fill="x", pady=1)
        tk.Label(f, text=lbl, font=FUENTES["small"],
                 bg=self._t("bg_sidebar"), fg=self._t("texto_dim"), anchor="w").pack(side="left")
        tk.Label(f, text=val, font=FUENTES["badge"],
                 bg=self._t("bg_sidebar"), fg=color, anchor="e").pack(side="right")

    def _actualizar_combo_carreras(self):
        """
        MAP + set: extrae carreras unicas y actualiza los valores del combo
        SIN disparar el evento <<ComboboxSelected>>.
        Se hace desvinculando temporalmente el binding antes de actualizar
        y revinculando despues, para que cambiar 'values' no pise el
        valor seleccionado ni dispare el handler de filtrado.
        """
        unicas = sorted(set(aplicar_map(self.estado.datos_base, lambda e: e["carrera"])))
        valor_actual = self.var_carrera.get()

        # Desvincular temporalmente para evitar el disparo del evento
        self.combo_carrera.unbind("<<ComboboxSelected>>")
        self.combo_carrera["values"] = ["Todas"] + unicas
        # Restaurar el valor que tenia el usuario (o "Todas" si ya no existe)
        nuevo_valor = valor_actual if valor_actual in (["Todas"] + unicas) else "Todas"
        self.var_carrera.set(nuevo_valor)
        # Revincular el handler
        self.combo_carrera.bind("<<ComboboxSelected>>", self._on_filtro_carrera)


    def _aplicar_filtros_combinados(self):
        """
        combinar_filtros: AND logico de TODOS los filtros activos:
          busqueda + filtro rapido (estado / ranking relativo) + carrera + semestre.
        Parte siempre de datos_base completo, sin mutar nada.
        """
        predicados = []

        # 1. Busqueda de texto
        t = self.var_busqueda.get()
        if t.strip():
            predicados.append(buscar_funcional(t))                  # HOF -> closure

        # 2. Filtro rapido: estado academico O ranking relativo
        fr = self.var_filtro_rapido.get()
        if fr == "Excelentes":
            predicados.append(filtrar_por_estado("Excelente"))      # HOF
        elif fr == "Aprobados":
            predicados.append(filtrar_por_estado("Aprobado"))
        elif fr == "Desaprobados":
            predicados.append(filtrar_por_estado("Desaprobado"))
        elif fr == "Ranking abajo":
            pass  # no agrega predicado; solo se ordenara al final
        elif fr == "Decimo superior":
            predicados.append(
                filtrar_por_ranking(0.10, self.estado.datos_base))  # HOF -> closure
        elif fr == "Quinto superior":
            predicados.append(
                filtrar_por_ranking(0.20, self.estado.datos_base))
        elif fr == "Tercio superior":
            predicados.append(
                filtrar_por_ranking(0.333, self.estado.datos_base))
        elif fr == "Primeros lugares":
            predicados.append(
                filtrar_primer_lugar(self.estado.datos_base))       # HOF -> closure

        # 3. Carrera
        c = self.var_carrera.get()
        if c != "Todas":
            predicados.append(filtrar_por_carrera(c))               # HOF -> closure

        # 4. Semestre
        s = self.var_semestre.get()
        if s != "Todos":
            predicados.append(filtrar_por_semestre(int(s)))         # HOF -> closure

        # COMPOSICION DE PREDICADOS + FILTER
        base_filtrada = (
            aplicar_filter(self.estado.datos_base, combinar_filtros(*predicados))
            if predicados
            else self.estado.datos_base[:]
        )

        # Si el filtro rapido es "Ranking abajo", ordenamos el resultado
        resultado = (
            ordenar_por("promedio")(base_filtrada)   # HOF
            if fr == "Ranking abajo"
            else base_filtrada
        )

        self._refrescar_tabla(resultado)

    # -- Handlers -- todos delegan a _aplicar_filtros_combinados --

    def _on_busqueda(self, *_):
        """HOF + CLOSURE + FILTER combinado."""
        self._aplicar_filtros_combinados()

    def _on_filtro_rapido(self, _=None):
        """Filtro rapido combinado con carrera y semestre."""
        self._aplicar_filtros_combinados()

    def _on_filtro_carrera(self, _=None):
        """HOF + FILTER combinado."""
        self._aplicar_filtros_combinados()

    def _on_filtro_semestre(self, _=None):
        """HOF + FILTER combinado."""
        self._aplicar_filtros_combinados()

    # -- Limpiar y mostrar todos ---------------------------------

    def _limpiar_filtros(self):
        self.var_busqueda.set("")
        self.var_filtro_rapido.set("Todos")
        self.var_carrera.set("Todas")
        self.var_semestre.set("Todos")

    def _mostrar_todos(self):
        self._limpiar_filtros()
        self._refrescar_tabla(self.estado.datos_base)

    # -- Ordenar columna -----------------------------------------

    def _ordenar_col(self, col: str):
        """HOF: ordenar_por alterna direccion."""
        inv = self._orden_inv.get(col, False)
        self._orden_inv[col] = not inv
        ordenado = ordenar_por(col, not inv)(self.estado.datos_activos)  # HOF
        self._refrescar_tabla(ordenado)


    def _cargar_csv(self):
        """PIPE: ruta -> parsear -> MAP(enriquecer) -> UI."""
        ruta = filedialog.askopenfilename(
            title="Seleccionar CSV de estudiantes",
            filetypes=[("CSV", "*.csv"), ("Todos", "*.*")])
        if not ruta:
            return
        try:
            self.estado.cargar(ruta)
            self._actualizar_combo_carreras()
            self._refrescar_tabla(self.estado.datos_base)
            self._actualizar_sidebar()
            nombre = os.path.basename(ruta)
            self.lbl_fuente.config(text=f" [{nombre}]", fg=self._t("acento3"))
            messagebox.showinfo("CSV cargado",
                f"Se cargaron {len(self.estado.datos_base):,} estudiantes\nArchivo: {nombre}")
        except Exception as e:
            messagebox.showerror("Error al cargar", str(e))

    def _exportar(self):
        """MAP: datos activos -> filas CSV."""
        if not self.estado.datos_activos:
            messagebox.showwarning("Sin datos", "No hay datos para exportar.")
            return
        ruta = filedialog.asksaveasfilename(
            defaultextension=".csv", filetypes=[("CSV","*.csv")], title="Guardar CSV")
        if not ruta:
            return
        cols  = ["nombre","dni","carrera","semestre","promedio","max","min","estado"]
        filas = aplicar_map(
            self.estado.datos_activos,
            lambda e: [e["nombre"], e["dni"], e["carrera"], e["semestre"],
                       f"{e['promedio']:.2f}", f"{e['max']:.0f}",
                       f"{e['min']:.0f}", e["estado"]]
        )
        with open(ruta, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(cols)
            w.writerows(filas)
        messagebox.showinfo("Exportado",
            f"Guardado: {os.path.basename(ruta)}\n{len(filas):,} registros.")

    def _gen_ejemplo(self):
        ruta = filedialog.asksaveasfilename(
            defaultextension=".csv", initialfile="ejemplo_200.csv",
            filetypes=[("CSV","*.csv")])
        if not ruta:
            return
        generar_csv_ejemplo(ruta, 200)
        messagebox.showinfo("CSV Generado",
            f"200 registros guardados en:\n{os.path.basename(ruta)}\n"
            "\nCargalo con 'Cargar CSV'")

    def _reset(self):
        self.estado.reset()
        self._limpiar_filtros()
        self._actualizar_combo_carreras()  
        self._refrescar_tabla(self.estado.datos_base)
        self._actualizar_sidebar()
        self.lbl_fuente.config(text=" [ejemplo]", fg=self._t("texto_dim"))

    def _btn(self, padre, texto, cmd, color_key) -> tk.Button:
        c   = self._t(color_key)
        osc = TEMA_ACTUAL == "Noche"
        return tk.Button(
            padre, text=texto, command=cmd, font=FUENTES["small"],
            bg=c, fg="#FFFFFF" if osc else "#1A2640",
            activebackground=self._t("acento"), activeforeground="#FFFFFF",
            relief="flat", bd=0, padx=9, pady=4, cursor="hand2",
        )

if __name__ == "__main__":
    app = App()
    app.mainloop()