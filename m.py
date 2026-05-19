
import csv
import random
import time
from itertools import product
from functools import reduce


NOMBRES_M = [
    "Alejandro","Matias","Sebastian","Diego","Andres","Felipe","Nicolas",
    "Rodrigo","Emilio","Tomas","Javier","Ricardo","Fernando","Carlos","Pablo",
    "Gustavo","Mauricio","Cristian","Fabian","Leonardo","Marcelo","Hugo",
    "Ignacio","Patricio","Hernan","Raul","Oscar","Ivan","Marco","Adrian",
]
NOMBRES_F = [
    "Valentina","Camila","Isabella","Sofia","Gabriela","Renata","Antonella",
    "Lucia","Elena","Maria","Ana","Paula","Daniela","Carolina","Andrea",
    "Monica","Patricia","Natalia","Claudia","Valeria","Fernanda","Lorena",
    "Beatriz","Cecilia","Diana","Gloria","Helena","Irene","Julia","Laura",
]
APELLIDOS = [
    "Garcia","Rodriguez","Gonzalez","Fernandez","Lopez","Martinez","Sanchez",
    "Perez","Torres","Ramirez","Flores","Vargas","Castillo","Morales","Reyes",
    "Herrera","Medina","Aguilar","Guerrero","Mendoza","Ruiz","Diaz","Cruz",
    "Ortiz","Ramos","Chavez","Romero","Delgado","Vega","Munoz","Rios",
    "Salinas","Fuentes","Alvarez","Soto","Mora","Rojas","Espinoza","Pena",
    "Jimenez","Silva","Cabrera","Navarro","Paredes","Cano","Molina","Campos",
]
CARRERAS = [
    "Sistemas",
    "Industrial",
    "Civil",
    "Electrica",
    "Mecanica",
    "Quimica",
    "Biomedica",
    "Ambiental",
    "Electronica",
    "Computacion",
]
SEMESTRES = list(range(1, 11))  

def gen_nombre() -> str:
    sexo = random.choice(["M", "F"])
    nombre = random.choice(NOMBRES_M if sexo == "M" else NOMBRES_F)
    ap1   = random.choice(APELLIDOS)
    ap2   = random.choice(APELLIDOS)
    return f"{nombre} {ap1} {ap2}"


def gen_dni() -> str:
    return str(random.randint(10_000_000, 99_999_999))


def gen_notas(n: int = 4) -> list[int]:
    """
    ✔ MAP: genera n notas con distribución gaussiana truncada
    para que los datos sean más realistas (más estudiantes en rango medio).
    """
    def nota_gaussiana() -> int:
        return max(0, min(20, int(random.gauss(13.5, 3.8))))
    return list(map(lambda _: nota_gaussiana(), range(n))) 


def gen_estudiante(idx: int) -> dict:
    notas = gen_notas(4)
    return {
        "id":        idx,
        "nombre":    gen_nombre(),
        "dni":       gen_dni(),
        "carrera":   random.choice(CARRERAS),
        "semestre":  random.choice(SEMESTRES),
        "nota1":     notas[0],
        "nota2":     notas[1],
        "nota3":     notas[2],
        "nota4":     notas[3],
    }


def log_progreso(actual: int, total: int, inicio: float):
    porcentaje = actual / total * 100
    elapsed    = time.time() - inicio
    velocidad  = actual / elapsed if elapsed > 0 else 0
    restante   = (total - actual) / velocidad if velocidad > 0 else 0
    print(
        f"\r  [{porcentaje:5.1f}%] {actual:>9,} / {total:,} filas"
        f"  |  {velocidad:,.0f} reg/s"
        f"  |  ETA: {restante:.0f}s   ",
        end="",
        flush=True,
    )



def generar_csv(ruta: str, total: int = 1_000_000, chunk: int = 10_000):
    """
    ✔ Generador lazy (yield) + escritura por lotes.
    No carga todo en memoria: funcional y eficiente.
    """
    encabezado = ["id","nombre","dni","carrera","semestre",
                  "nota1","nota2","nota3","nota4"]

    inicio = time.time()
    print(f"\n  Generando {total:,} registros → {ruta}")
    print(f"  Chunk size: {chunk:,} filas\n")

    with open(ruta, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=encabezado)
        writer.writeheader()

        escritos = 0
        while escritos < total:
            cantidad = min(chunk, total - escritos)

            chunk_datos = list(map(
                lambda i: gen_estudiante(escritos + i + 1),
                range(cantidad)
            ))

            writer.writerows(chunk_datos)
            escritos += cantidad
            log_progreso(escritos, total, inicio)

    duracion = time.time() - inicio
    tam_mb   = os.path.getsize(ruta) / 1_048_576
    print(f"\n\n  ✔ Listo en {duracion:.1f}s  |  {tam_mb:.1f} MB  |  {ruta}\n")


if __name__ == "__main__":
    import os

    print("=" * 60)
    print("  GENERADOR DE DATOS — ESTUDIANTES UNIVERSITARIOS")
    print("=" * 60)

    opciones = {
        "1": ("10,000 registros  (~0.5 MB)",  10_000,    "estudiantes_10k.csv"),
        "2": ("100,000 registros (~5 MB)",    100_000,   "estudiantes_100k.csv"),
        "3": ("500,000 registros (~28 MB)",   500_000,   "estudiantes_500k.csv"),
        "4": ("1,000,000 registros (~55 MB)", 1_000_000, "estudiantes_1M.csv"),
        "5": ("Personalizado",                None,      None),
    }

    print("\n  ¿Cuántos registros quieres generar?\n")
    for k, (desc, _, _) in opciones.items():
        print(f"    [{k}] {desc}")

    opcion = input("\n  Opción: ").strip()

    if opcion not in opciones:
        print("  Opción inválida. Generando 10,000 por defecto.")
        opcion = "1"

    if opcion == "5":
        n    = int(input("  Cantidad de registros: ").replace(",", "").strip())
        ruta = input("  Nombre del archivo (ej: mis_datos.csv): ").strip()
        if not ruta.endswith(".csv"):
            ruta += ".csv"
    else:
        _, n, ruta = opciones[opcion]

    generar_csv(ruta, total=n)
    print(f"  Ahora puedes cargarlo en AnalizadorFP con 'Cargar CSV'\n")