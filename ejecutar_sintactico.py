# EJECUTOR DEL ANALIZADOR SINTACTICO DE RUST
# Genera logs de prueba por integrante, parecido a ejecutar_lexico.py.
# Incluye revision linea por linea para indicar si cada linea esta correcta
# o si contiene errores lexicos/sintacticos.

import sys
import os
from datetime import datetime
from parser import analizar_sintactico


def obtener_estado_lineas(codigo_fuente, errores_lexicos, errores_sintacticos):
    """
    Revisa el codigo fuente linea por linea y marca cada linea como:
    - CORRECTA
    - ERROR LEXICO
    - ERROR SINTACTICO
    - ERROR LEXICO Y SINTACTICO

    Nota:
    En algunos errores sintacticos, el parser puede reportar el error en la linea
    donde encuentra el token inesperado, no siempre en la linea exacta donde empezo
    el problema. Por ejemplo, si falta un punto y coma en la linea 2, el error puede
    aparecer en la linea 3 porque ahi el parser detecta que algo no encaja.
    """

    lineas = codigo_fuente.splitlines()

    errores_por_linea = {}

    # Registrar errores lexicos por linea
    for err in errores_lexicos:
        linea = err.get('linea')
        if linea is None:
            continue

        if linea not in errores_por_linea:
            errores_por_linea[linea] = {
                'lexicos': [],
                'sintacticos': []
            }

        errores_por_linea[linea]['lexicos'].append(err.get('mensaje'))

    # Registrar errores sintacticos por linea
    for err in errores_sintacticos:
        linea = err.get('linea')
        if linea is None:
            continue

        if linea not in errores_por_linea:
            errores_por_linea[linea] = {
                'lexicos': [],
                'sintacticos': []
            }

        errores_por_linea[linea]['sintacticos'].append(err.get('mensaje'))

    revision = []

    for numero_linea, contenido in enumerate(lineas, start=1):
        datos_error = errores_por_linea.get(
            numero_linea,
            {
                'lexicos': [],
                'sintacticos': []
            }
        )

        tiene_lexico = len(datos_error['lexicos']) > 0
        tiene_sintactico = len(datos_error['sintacticos']) > 0

        if tiene_lexico and tiene_sintactico:
            estado = "ERROR LEXICO Y SINTACTICO"
        elif tiene_lexico:
            estado = "ERROR LEXICO"
        elif tiene_sintactico:
            estado = "ERROR SINTACTICO"
        else:
            estado = "CORRECTA"

        mensajes = []

        for mensaje in datos_error['lexicos']:
            mensajes.append(f"Lexico: {mensaje}")

        for mensaje in datos_error['sintacticos']:
            mensajes.append(f"Sintactico: {mensaje}")

        revision.append({
            'linea': numero_linea,
            'estado': estado,
            'codigo': contenido,
            'mensajes': mensajes
        })

    return revision


def analizar_archivo_sintactico(ruta_archivo, nombre_apellido):
    if not os.path.isfile(ruta_archivo):
        print(f"Error: no se encontro el archivo '{ruta_archivo}'")
        sys.exit(1)

    with open(ruta_archivo, 'r', encoding='utf-8') as f:
        codigo_fuente = f.read()

    resultado = analizar_sintactico(codigo_fuente)

    carpeta_logs = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
    os.makedirs(carpeta_logs, exist_ok=True)

    ahora = datetime.now()
    fecha_hora = ahora.strftime('%d-%m-%Y-%Hh%M')
    nombre_log = f"sintactico-{nombre_apellido}-{fecha_hora}.txt"
    ruta_log = os.path.join(carpeta_logs, nombre_log)

    errores_lexicos = resultado['errores_lexicos']
    errores_sintacticos = resultado['errores_sintacticos']

    revision_lineas = obtener_estado_lineas(
        codigo_fuente,
        errores_lexicos,
        errores_sintacticos
    )

    with open(ruta_log, 'w', encoding='utf-8') as log:
        log.write("=" * 72 + "\n")
        log.write("LOG DE ANALISIS SINTACTICO\n")
        log.write("=" * 72 + "\n")
        log.write(f"Desarrollador      : {nombre_apellido}\n")
        log.write(f"Archivo analizado  : {ruta_archivo}\n")
        log.write(f"Fecha y hora       : {ahora.strftime('%d-%m-%Y %H:%M:%S')}\n")
        log.write(f"Resultado          : {'ACEPTADO' if resultado['valido'] else 'RECHAZADO'}\n")
        log.write(f"Errores lexicos    : {len(errores_lexicos)}\n")
        log.write(f"Errores sintacticos: {len(errores_sintacticos)}\n")
        log.write("=" * 72 + "\n\n")

        log.write("--- REGLAS SINTACTICAS VALIDADAS ---\n")
        log.write("El parser valida un subconjunto de Rust con funciones, bloques,\n")
        log.write("declaraciones let, mutabilidad, tipos, estructuras, condicionales,\n")
        log.write("ciclos, expresiones, operadores, llamadas a funciones y macros.\n\n")

        log.write("--- RESULTADO GENERAL ---\n")
        if resultado['valido']:
            log.write("El archivo cumple con la gramatica definida para el subconjunto de Rust.\n")
        else:
            log.write("El archivo NO cumple completamente con la gramatica definida.\n")
            log.write("Revise los errores listados a continuacion.\n")

        # ============================================================
        # NUEVA SECCION: REVISION LINEA POR LINEA
        # ============================================================
        log.write("\n--- REVISION LINEA POR LINEA ---\n")
        log.write("Esta seccion muestra cada linea del archivo y su estado.\n")
        log.write("Si una linea aparece como CORRECTA, no se detectaron errores asociados a esa linea.\n")
        log.write("Si aparece como ERROR SINTACTICO, la estructura no cumple la gramatica definida.\n")
        log.write("Si aparece como ERROR LEXICO, contiene simbolos o tokens no reconocidos.\n\n")

        log.write(f"{'LINEA':<8}{'ESTADO':<28}{'CODIGO'}\n")
        log.write("-" * 100 + "\n")

        for item in revision_lineas:
            log.write(
                f"{str(item['linea']):<8}"
                f"{item['estado']:<28}"
                f"{item['codigo']}\n"
            )

            if item['mensajes']:
                for mensaje in item['mensajes']:
                    log.write(f"{'':<8}{'Detalle:':<28}{mensaje}\n")

        log.write("\n--- ERRORES LEXICOS HEREDADOS DEL LEXER ---\n")
        if errores_lexicos:
            log.write(f"{'LINEA':<8}{'MENSAJE'}\n")
            log.write("-" * 60 + "\n")
            for err in errores_lexicos:
                log.write(f"{str(err.get('linea')):<8}{err.get('mensaje')}\n")
        else:
            log.write("No se encontraron errores lexicos.\n")

        log.write("\n--- ERRORES SINTACTICOS ---\n")
        if errores_sintacticos:
            log.write(f"{'LINEA':<8}{'TOKEN':<22}{'VALOR':<25}{'MENSAJE'}\n")
            log.write("-" * 90 + "\n")
            for err in errores_sintacticos:
                log.write(
                    f"{str(err.get('linea')):<8}"
                    f"{str(err.get('token')):<22}"
                    f"{str(err.get('valor')):<25}"
                    f"{err.get('mensaje')}\n"
                )
        else:
            log.write("No se encontraron errores sintacticos.\n")

    print("Analisis sintactico completado.")
    print(f"Resultado          : {'ACEPTADO' if resultado['valido'] else 'RECHAZADO'}")
    print(f"Errores lexicos    : {len(errores_lexicos)}")
    print(f"Errores sintacticos: {len(errores_sintacticos)}")
    print(f"Log generado en    : {ruta_log}")
    return ruta_log


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Uso: python ejecutar_sintactico.py <archivo.rs> <NombreApellido>")
        print("Ejemplo: python ejecutar_sintactico.py algoritmo1.rs CristhianHerrera")
        sys.exit(1)

    archivo = sys.argv[1]
    nombre = sys.argv[2]
    analizar_archivo_sintactico(archivo, nombre)