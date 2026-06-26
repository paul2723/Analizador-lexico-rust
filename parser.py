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

# ================================================================
# APORTE 3 - Moscoso Ramos Gustavo
# Responsabilidad: asignaciones, operadores, expresiones,
# return y manejo de errores sintacticos.
# ================================================================

def p_asignacion(p):
    'asignacion : asignable operador_asignacion expresion'
    p[0] = ('asignacion', p[1], p[2], p[3])


def p_asignable(p):
    '''asignable : IDENTIFICADOR
                 | acceso_miembro'''
    p[0] = p[1]


def p_operador_asignacion(p):
    '''operador_asignacion : ASIGNACION
                           | MAS_IGUAL
                           | MENOS_IGUAL
                           | MULT_IGUAL
                           | DIV_IGUAL
                           | MOD_IGUAL'''
    p[0] = p[1]


def p_retorno(p):
    '''retorno : RETURN expresion
               | RETURN'''
    p[0] = ('return', p[2]) if len(p) == 3 else ('return', None)


def p_seleccion_match(p):
    'seleccion_match : MATCH expresion LLAVE_IZQ brazos_match_opt LLAVE_DER'
    p[0] = ('match', p[2], p[4])


def p_brazos_match_opt(p):
    '''brazos_match_opt : brazos_match
                        | vacio'''
    p[0] = p[1]


def p_brazos_match(p):
    '''brazos_match : brazos_match brazo_match
                    | brazo_match'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]


def p_brazo_match(p):
    '''brazo_match : patron FLECHA_GRUESA expresion coma_opt
                   | patron FLECHA_GRUESA bloque coma_opt'''
    p[0] = ('brazo', p[1], p[3])


def p_patron(p):
    '''patron : IDENTIFICADOR
              | NUMERO_ENTERO
              | TRUE
              | FALSE
              | CARACTER_LITERAL
              | CADENA'''
    p[0] = ('patron', p[1])


def p_expresion_binaria(p):
    '''expresion : expresion MAS expresion
                 | expresion MENOS expresion
                 | expresion MULTIPLICACION expresion
                 | expresion DIVISION expresion
                 | expresion MODULO expresion
                 | expresion IGUAL_IGUAL expresion
                 | expresion DIFERENTE expresion
                 | expresion MENOR expresion
                 | expresion MAYOR expresion
                 | expresion MENOR_IGUAL expresion
                 | expresion MAYOR_IGUAL expresion
                 | expresion AND_LOGICO expresion
                 | expresion OR_LOGICO expresion
                 | expresion OR_BIT expresion
                 | expresion XOR_BIT expresion
                 | expresion AMPERSAND expresion
                 | expresion SHIFT_IZQ expresion
                 | expresion SHIFT_DER expresion'''
    p[0] = ('binaria', p[2], p[1], p[3])


def p_expresion_cast(p):
    'expresion : expresion AS tipo'
    p[0] = ('cast', p[1], p[3])


def p_expresion_rango(p):
    'expresion : expresion PUNTO PUNTO expresion'
    p[0] = ('rango', p[1], p[4])


def p_expresion_unaria(p):
    '''expresion : NOT_LOGICO expresion
                 | MENOS expresion %prec UMENOS
                 | AMPERSAND expresion %prec REFERENCIA
                 | AMPERSAND MUT expresion %prec REFERENCIA'''
    if len(p) == 3:
        p[0] = ('unaria', p[1], p[2])
    else:
        p[0] = ('referencia_mut', p[3])


def p_expresion_grupo(p):
    'expresion : PARENTESIS_IZQ expresion PARENTESIS_DER'
    p[0] = p[2]


def p_expresion_tupla(p):
    'expresion : PARENTESIS_IZQ argumentos COMA PARENTESIS_DER'
    p[0] = ('tupla', p[2])


def p_expresion_array(p):
    'expresion : CORCHETE_IZQ argumentos_opt CORCHETE_DER'
    p[0] = ('array', p[2])


def p_expresion_acceso_indice(p):
    'expresion : expresion CORCHETE_IZQ expresion CORCHETE_DER'
    p[0] = ('indice', p[1], p[3])


def p_expresion_llamada_metodo(p):
    'expresion : acceso_miembro PARENTESIS_IZQ argumentos_opt PARENTESIS_DER'
    p[0] = ('metodo', p[1], p[3])


def p_acceso_miembro(p):
    'acceso_miembro : expresion PUNTO IDENTIFICADOR'
    p[0] = ('acceso', p[1], p[3])


def p_expresion_base(p):
    '''expresion : NUMERO_ENTERO
                 | NUMERO_FLOTANTE
                 | CADENA
                 | CARACTER_LITERAL
                 | TRUE
                 | FALSE
                 | IDENTIFICADOR
                 | ruta
                 | llamada_funcion
                 | llamada_macro'''
    p[0] = ('expr', p[1])


def p_vacio(p):
    'vacio :'
    p[0] = []


def p_error(p):
    if p:
        mensaje = (
            f"Error sintactico: token inesperado '{p.value}' "
            f"de tipo {p.type} en la linea {p.lineno}."
        )
        errores_sintacticos.append({
            'linea': p.lineno,
            'token': p.type,
            'valor': p.value,
            'mensaje': mensaje,
        })
        # Se descarta el token inesperado para intentar continuar.
        parser.errok()
    else:
        mensaje = 'Error sintactico: fin de archivo inesperado. Falta cerrar una estructura o completar una sentencia.'
        errores_sintacticos.append({
            'linea': 'EOF',
            'token': 'EOF',
            'valor': '',
            'mensaje': mensaje,
        })


def construir_parser():
    return yacc.yacc(start='programa', debug=False, write_tables=False, errorlog=yacc.NullLogger())


parser = construir_parser()


def analizar_sintactico(codigo_fuente):
    """Ejecuta el analisis sintactico sobre codigo Rust.

    Retorna un diccionario con:
    - valido: True si no hay errores lexicos ni sintacticos.
    - ast: arbol sintactico abstracto simplificado.
    - errores_lexicos: errores generados por lexer.py.
    - errores_sintacticos: errores generados por parser.py.
    """
    global errores_sintacticos
    errores_sintacticos = []

    lexer = construir_lexer()
    resultado = parser.parse(codigo_fuente, lexer=lexer)

    return {
        'valido': len(lexer.errores) == 0 and len(errores_sintacticos) == 0,
        'ast': resultado,
        'errores_lexicos': lexer.errores,
        'errores_sintacticos': errores_sintacticos,
    }
