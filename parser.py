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

# ================================================================
# APORTE 2 - Alcivar Zavala Paul
# Responsabilidad: declaraciones, tipos de datos, estructuras,
# arreglos, tuplas, vectores y llamadas/rutas.
# ================================================================

def p_declaracion_variable(p):
    'declaracion_variable : LET mutabilidad_opt IDENTIFICADOR tipo_opt inicializacion_opt'
    p[0] = ('let', p[2], p[3], p[4], p[5])


def p_mutabilidad_opt(p):
    '''mutabilidad_opt : MUT
                       | vacio'''
    p[0] = True if p[1] == 'mut' else False


def p_tipo_opt(p):
    '''tipo_opt : DOS_PUNTOS tipo
                | vacio'''
    p[0] = p[2] if len(p) == 3 else None


def p_inicializacion_opt(p):
    '''inicializacion_opt : ASIGNACION expresion
                          | ASIGNACION struct_literal
                          | vacio'''
    p[0] = p[2] if len(p) == 3 else None


def p_tipo(p):
    '''tipo : tipo_primitivo
            | IDENTIFICADOR
            | AMPERSAND tipo
            | CORCHETE_IZQ tipo PUNTO_COMA NUMERO_ENTERO CORCHETE_DER
            | PARENTESIS_IZQ lista_tipos_opt PARENTESIS_DER
            | TIPO_VEC MENOR tipo MAYOR
            | TIPO_OPTION MENOR tipo MAYOR
            | TIPO_RESULT MENOR tipo COMA tipo MAYOR'''
    if len(p) == 2:
        p[0] = ('tipo', p[1])
    elif len(p) == 3:
        p[0] = ('referencia_tipo', p[2])
    elif len(p) == 4:
        p[0] = ('tupla_tipo', p[2])
    elif len(p) == 5:
        p[0] = ('generico', p[1], p[3])
    elif len(p) == 6:
        p[0] = ('array_tipo', p[2], p[4])
    else:
        p[0] = ('result_tipo', p[3], p[5])


def p_tipo_primitivo(p):
    '''tipo_primitivo : TIPO_I8
                      | TIPO_I16
                      | TIPO_I32
                      | TIPO_I64
                      | TIPO_I128
                      | TIPO_U8
                      | TIPO_U16
                      | TIPO_U32
                      | TIPO_U64
                      | TIPO_U128
                      | TIPO_F32
                      | TIPO_F64
                      | TIPO_BOOL
                      | TIPO_CHAR
                      | TIPO_STR
                      | TIPO_STRING
                      | TIPO_USIZE
                      | TIPO_ISIZE
                      | TIPO_VEC
                      | TIPO_OPTION
                      | TIPO_RESULT
                      | TIPO_HASHMAP'''
    p[0] = p[1]


def p_lista_tipos_opt(p):
    '''lista_tipos_opt : lista_tipos
                       | vacio'''
    p[0] = p[1]


def p_lista_tipos(p):
    '''lista_tipos : lista_tipos COMA tipo
                   | tipo'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]


def p_estructura(p):
    'estructura : STRUCT IDENTIFICADOR LLAVE_IZQ campos_struct_opt LLAVE_DER'
    p[0] = ('struct', p[2], p[4])


def p_campos_struct_opt(p):
    '''campos_struct_opt : campos_struct
                         | vacio'''
    p[0] = p[1]


def p_campos_struct(p):
    '''campos_struct : campos_struct campo_struct
                     | campo_struct'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]


def p_campo_struct(p):
    'campo_struct : IDENTIFICADOR DOS_PUNTOS tipo coma_opt'
    p[0] = ('campo', p[1], p[3])


def p_struct_literal(p):
    'struct_literal : IDENTIFICADOR LLAVE_IZQ pares_campo_opt LLAVE_DER'
    p[0] = ('struct_literal', p[1], p[3])


def p_pares_campo_opt(p):
    '''pares_campo_opt : pares_campo
                       | vacio'''
    p[0] = p[1]


def p_pares_campo(p):
    '''pares_campo : pares_campo par_campo
                   | par_campo'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]


def p_par_campo(p):
    'par_campo : IDENTIFICADOR DOS_PUNTOS expresion coma_opt'
    p[0] = ('par_campo', p[1], p[3])


def p_coma_opt(p):
    '''coma_opt : COMA
                | vacio'''
    p[0] = None


def p_enumeracion(p):
    'enumeracion : ENUM IDENTIFICADOR LLAVE_IZQ variantes_enum_opt LLAVE_DER'
    p[0] = ('enum', p[2], p[4])


def p_variantes_enum_opt(p):
    '''variantes_enum_opt : variantes_enum
                          | vacio'''
    p[0] = p[1]


def p_variantes_enum(p):
    '''variantes_enum : variantes_enum variante_enum
                      | variante_enum'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]


def p_variante_enum(p):
    '''variante_enum : IDENTIFICADOR coma_opt
                     | IDENTIFICADOR PARENTESIS_IZQ lista_tipos_opt PARENTESIS_DER coma_opt'''
    p[0] = ('variante', p[1])


def p_implementacion(p):
    'implementacion : IMPL IDENTIFICADOR LLAVE_IZQ sentencias_opt LLAVE_DER'
    p[0] = ('impl', p[2], p[4])


def p_llamada_funcion(p):
    '''llamada_funcion : IDENTIFICADOR PARENTESIS_IZQ argumentos_opt PARENTESIS_DER
                       | ruta PARENTESIS_IZQ argumentos_opt PARENTESIS_DER'''
    p[0] = ('llamada', p[1], p[3])


def p_llamada_macro(p):
    '''llamada_macro : IDENTIFICADOR NOT_LOGICO PARENTESIS_IZQ argumentos_opt PARENTESIS_DER
                     | IDENTIFICADOR NOT_LOGICO CORCHETE_IZQ argumentos_opt CORCHETE_DER'''
    p[0] = ('macro', p[1], p[4])


def p_ruta(p):
    '''ruta : base_ruta DOBLE_DOS_PUNTOS IDENTIFICADOR
            | ruta DOBLE_DOS_PUNTOS IDENTIFICADOR'''
    p[0] = ('ruta', p[1], p[3])


def p_base_ruta(p):
    '''base_ruta : IDENTIFICADOR
                 | tipo_primitivo
                 | SELF
                 | SELF_TYPE
                 | SUPER
                 | CRATE'''
    p[0] = p[1]


def p_argumentos_opt(p):
    '''argumentos_opt : argumentos
                      | vacio'''
    p[0] = p[1]


def p_argumentos(p):
    '''argumentos : argumentos COMA expresion
                  | expresion'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]
