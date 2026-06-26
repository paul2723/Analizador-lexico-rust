# ANALIZADOR SINTACTICO PARA UN SUBCONJUNTO DE RUST - PLY (yacc)
# Compatible con lexer.py del proyecto.

import ply.yacc as yacc
from lexer import tokens, construir_lexer

# Lista global donde p_error guarda los errores detectados.
errores_sintacticos = []

# Precedencia de operadores para expresiones.
precedence = (
    ('left', 'OR_LOGICO'),
    ('left', 'AND_LOGICO'),
    ('left', 'OR_BIT', 'XOR_BIT', 'AMPERSAND'),
    ('left', 'IGUAL_IGUAL', 'DIFERENTE'),
    ('left', 'MENOR', 'MAYOR', 'MENOR_IGUAL', 'MAYOR_IGUAL'),
    ('left', 'SHIFT_IZQ', 'SHIFT_DER'),
    ('left', 'MAS', 'MENOS'),
    ('left', 'MULTIPLICACION', 'DIVISION', 'MODULO'),
    ('right', 'NOT_LOGICO', 'UMENOS', 'REFERENCIA'),
    ('left', 'AS'),
)

# ================================================================
# APORTE 1 - Herrera Nieto Cristhian
# Responsabilidad: estructura general del programa, funciones,
# bloques, condicionales y ciclos principales.
# ================================================================

def p_programa(p):
    'programa : elementos_opt'
    p[0] = ('programa', p[1])


def p_elementos_opt(p):
    '''elementos_opt : elementos
                     | vacio'''
    p[0] = p[1]


def p_elementos(p):
    '''elementos : elementos elemento
                 | elemento'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]


def p_elemento(p):
    '''elemento : funcion
                | estructura
                | enumeracion
                | implementacion
                | sentencia'''
    p[0] = p[1]


def p_visibilidad_opt(p):
    '''visibilidad_opt : PUB
                       | vacio'''
    p[0] = p[1]


def p_funcion(p):
    'funcion : visibilidad_opt FN IDENTIFICADOR PARENTESIS_IZQ parametros_opt PARENTESIS_DER retorno_opt bloque'
    p[0] = ('funcion', p[3], p[5], p[7], p[8])


def p_parametros_opt(p):
    '''parametros_opt : parametros
                      | vacio'''
    p[0] = p[1]


def p_parametros(p):
    '''parametros : parametros COMA parametro
                  | parametro'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]


def p_parametro(p):
    '''parametro : IDENTIFICADOR DOS_PUNTOS tipo
                 | AMPERSAND IDENTIFICADOR DOS_PUNTOS tipo'''
    if len(p) == 4:
        p[0] = ('parametro', p[1], p[3])
    else:
        p[0] = ('parametro_ref', p[2], p[4])


def p_retorno_opt(p):
    '''retorno_opt : FLECHA tipo
                   | vacio'''
    p[0] = p[2] if len(p) == 3 else None


def p_bloque(p):
    'bloque : LLAVE_IZQ sentencias_opt LLAVE_DER'
    p[0] = ('bloque', p[2])


def p_sentencias_opt(p):
    '''sentencias_opt : sentencias
                      | vacio'''
    p[0] = p[1]


def p_sentencias(p):
    '''sentencias : sentencias sentencia
                  | sentencia'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]


def p_sentencia(p):
    '''sentencia : declaracion_variable PUNTO_COMA
                 | asignacion PUNTO_COMA
                 | expresion PUNTO_COMA
                 | retorno PUNTO_COMA
                 | BREAK PUNTO_COMA
                 | CONTINUE PUNTO_COMA
                 | condicional
                 | ciclo_while
                 | ciclo_for
                 | ciclo_loop
                 | seleccion_match
                 | estructura
                 | enumeracion
                 | implementacion'''
    p[0] = ('sentencia', p[1])


def p_condicional(p):
    'condicional : IF expresion bloque sino_opt'
    p[0] = ('if', p[2], p[3], p[4])


def p_sino_opt(p):
    '''sino_opt : ELSE bloque
                | ELSE condicional
                | vacio'''
    if len(p) == 3:
        p[0] = p[2]
    else:
        p[0] = None


def p_ciclo_while(p):
    'ciclo_while : WHILE expresion bloque'
    p[0] = ('while', p[2], p[3])


def p_ciclo_for(p):
    'ciclo_for : FOR IDENTIFICADOR IN expresion bloque'
    p[0] = ('for', p[2], p[4], p[5])


def p_ciclo_loop(p):
    'ciclo_loop : LOOP bloque'
    p[0] = ('loop', p[2])
