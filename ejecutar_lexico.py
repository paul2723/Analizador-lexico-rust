import sys
import os
from datetime import datetime
from lexer import construir_lexer


def analizar_archivo(ruta_archivo, nombre_apellido):
    if not os.path.isfile(ruta_archivo):
        print(f"Error: no se encontro el archivo '{ruta_archivo}'")
        sys.exit(1)

    with open(ruta_archivo, 'r', encoding='utf-8') as f:
        codigo_fuente = f.read()

    lexer = construir_lexer()
    lexer.input(codigo_fuente)

    tokens_reconocidos = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens_reconocidos.append(tok)

    # Carpeta de logs (relativa a este script)
    carpeta_logs = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
    os.makedirs(carpeta_logs, exist_ok=True)

    # Formato de fecha-hora pedido: dia-mes-anio-horaHminuto (ej. 14-06-2026-14h32)
    ahora = datetime.now()
    fecha_hora = ahora.strftime('%d-%m-%Y-%Hh%M')
    nombre_log = f"lexico-{nombre_apellido}-{fecha_hora}.txt"
    ruta_log = os.path.join(carpeta_logs, nombre_log)

    with open(ruta_log, 'w', encoding='utf-8') as log:
        log.write("=" * 70 + "\n")
        log.write("LOG DE ANALISIS LEXICO\n")
        log.write("=" * 70 + "\n")
        log.write(f"Desarrollador      : {nombre_apellido}\n")
        log.write(f"Archivo analizado  : {ruta_archivo}\n")
        log.write(f"Fecha y hora       : {ahora.strftime('%d-%m-%Y %H:%M:%S')}\n")
        log.write(f"Total de tokens    : {len(tokens_reconocidos)}\n")
        log.write(f"Total de errores   : {len(lexer.errores)}\n")
        log.write("=" * 70 + "\n\n")

        log.write("--- TOKENS RECONOCIDOS ---\n")
        log.write(f"{'LINEA':<8}{'TOKEN':<22}{'VALOR':<30}\n")
        log.write("-" * 60 + "\n")
        for tok in tokens_reconocidos:
            log.write(f"{tok.lineno:<8}{tok.type:<22}{str(tok.value):<30}\n")

        log.write("\n--- ERRORES LEXICOS ---\n")
        if lexer.errores:
            log.write(f"{'LINEA':<8}{'MENSAJE'}\n")
            log.write("-" * 60 + "\n")
            for err in lexer.errores:
                log.write(f"{err['linea']:<8}{err['mensaje']}\n")
        else:
            log.write("No se encontraron errores lexicos.\n")

    print(f"Analisis completado.")
    print(f"Tokens reconocidos : {len(tokens_reconocidos)}")
    print(f"Errores encontrados: {len(lexer.errores)}")
    print(f"Log generado en    : {ruta_log}")
    return ruta_log


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Uso: python ejecutar_lexico.py <archivo.rs> <NombreApellido>")
        print("Ejemplo: python ejecutar_lexico.py algoritmos/algoritmo1.rs JuanPerez")
        sys.exit(1)

    archivo = sys.argv[1]
    nombre = sys.argv[2]
    analizar_archivo(archivo, nombre)
