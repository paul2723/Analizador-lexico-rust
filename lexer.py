# ANALIZADOR LEXICO PARA RUST - PLY (lex)
import ply.lex as lex
palabras_reservadas = {
    'fn': 'FN',
    'let': 'LET',
    'mut': 'MUT',
    'const': 'CONST',
    'static': 'STATIC',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',
    'loop': 'LOOP',
    'match': 'MATCH',
    'break': 'BREAK',
    'continue': 'CONTINUE',
    'return': 'RETURN',
    'struct': 'STRUCT',
    'enum': 'ENUM',
    'impl': 'IMPL',
    'trait': 'TRAIT',
    'pub': 'PUB',
    'use': 'USE',
    'mod': 'MOD',
    'self': 'SELF',
    'Self': 'SELF_TYPE',
    'super': 'SUPER',
    'crate': 'CRATE',
    'true': 'TRUE',
    'false': 'FALSE',
    'as': 'AS',
    'in': 'IN',
    'ref': 'REF',
    'move': 'MOVE',
    'where': 'WHERE',
    'unsafe': 'UNSAFE',
    'async': 'ASYNC',
    'await': 'AWAIT',
    'dyn': 'DYN',
    'type': 'TYPE',
}
 
# Tipos de datos primitivos de Rust (se tratan como palabras reservadas de tipo)
tipos_primitivos = {
    'i8': 'TIPO_I8', 'i16': 'TIPO_I16', 'i32': 'TIPO_I32', 'i64': 'TIPO_I64', 'i128': 'TIPO_I128',
    'u8': 'TIPO_U8', 'u16': 'TIPO_U16', 'u32': 'TIPO_U32', 'u64': 'TIPO_U64', 'u128': 'TIPO_U128',
    'f32': 'TIPO_F32', 'f64': 'TIPO_F64',
    'bool': 'TIPO_BOOL',
    'char': 'TIPO_CHAR',
    'str': 'TIPO_STR',
    'String': 'TIPO_STRING',
    'usize': 'TIPO_USIZE',
    'isize': 'TIPO_ISIZE',
    'Vec': 'TIPO_VEC',
    'Option': 'TIPO_OPTION',
    'Result': 'TIPO_RESULT',
    'HashMap': 'TIPO_HASHMAP',
}
 
tokens = [
    # Identificadores y literales
    'IDENTIFICADOR',
    'MACRO',
    'NUMERO_ENTERO',
    'NUMERO_FLOTANTE',
    'CADENA',
    'CARACTER_LITERAL',
 
    # Operadores aritmeticos
    'MAS', 'MENOS', 'MULTIPLICACION', 'DIVISION', 'MODULO',
 
    # Operadores de asignacion
    'ASIGNACION', 'MAS_IGUAL', 'MENOS_IGUAL', 'MULT_IGUAL', 'DIV_IGUAL', 'MOD_IGUAL',
 
    # Operadores de comparacion
    'IGUAL_IGUAL', 'DIFERENTE', 'MENOR', 'MAYOR', 'MENOR_IGUAL', 'MAYOR_IGUAL',
 
    # Operadores logicos
    'AND_LOGICO', 'OR_LOGICO', 'NOT_LOGICO',
 
    # Operadores a nivel de bits
    'OR_BIT', 'XOR_BIT', 'SHIFT_IZQ', 'SHIFT_DER',
 
    # Delimitadores
    'LLAVE_IZQ', 'LLAVE_DER',
    'PARENTESIS_IZQ', 'PARENTESIS_DER',
    'CORCHETE_IZQ', 'CORCHETE_DER',
    'PUNTO_COMA', 'DOS_PUNTOS', 'DOBLE_DOS_PUNTOS', 'COMA', 'PUNTO',
    'FLECHA', 'FLECHA_GRUESA', 'ARROBA', 'INTERROGACION', 'AMPERSAND',
] + list(palabras_reservadas.values()) + list(tipos_primitivos.values())


# Componentes a cargo: Tipos de datos (literales) y Delimitadores
 
# --- Literales (tipos de datos primitivos en su forma literal) ---
 
# Numero flotante: debe revisarse ANTES que el entero (mayor especificidad)
def t_NUMERO_FLOTANTE(t):
    r'\d+\.\d+([eE][+-]?\d+)?'
    t.value = float(t.value)
    return t
 
 
def t_NUMERO_ENTERO(t):
    r'\d+'
    t.value = int(t.value)
    return t
 
 
def t_CADENA(t):
    r'"([^"\\]|\\.)*"'
    t.value = t.value[1:-1]  # quitar comillas
    return t
 
 
def t_CARACTER_LITERAL(t):
    r"'([^'\\]|\\.)'"
    t.value = t.value[1:-1]
    return t
 
 
# --- Delimitadores ---
t_LLAVE_IZQ        = r'\{'
t_LLAVE_DER        = r'\}'
t_PARENTESIS_IZQ   = r'\('
t_PARENTESIS_DER   = r'\)'
t_CORCHETE_IZQ     = r'\['
t_CORCHETE_DER     = r'\]'
t_PUNTO_COMA       = r';'
t_DOBLE_DOS_PUNTOS = r'::'
t_DOS_PUNTOS       = r':'
t_COMA             = r','
t_PUNTO            = r'\.'
t_FLECHA           = r'->'
t_FLECHA_GRUESA    = r'=>'
t_ARROBA           = r'@'
t_INTERROGACION    = r'\?'

# Componentes a cargo: Operadores aritmeticos, asignacion, comparacion, logicos y a nivel de bits


# --- Operadores de asignacion compuesta (deben ir ANTES que los simples) ---
t_MAS_IGUAL      = r'\+='
t_MENOS_IGUAL    = r'-='
t_MULT_IGUAL     = r'\*='
t_DIV_IGUAL      = r'/='
t_MOD_IGUAL      = r'%='

# --- Operadores de comparacion (orden: largos antes que cortos) ---
t_IGUAL_IGUAL    = r'=='
t_DIFERENTE      = r'!='
t_MENOR_IGUAL    = r'<='
t_MAYOR_IGUAL    = r'>='

# --- Operadores logicos ---
t_AND_LOGICO     = r'&&'
t_OR_LOGICO      = r'\|\|'
t_NOT_LOGICO     = r'!'

# --- Operadores a nivel de bits (shift antes que comparacion simple) ---
t_SHIFT_IZQ      = r'<<'
t_SHIFT_DER      = r'>>'
t_AND_BIT        = r'&'
t_OR_BIT         = r'\|'
t_XOR_BIT        = r'\^'

# --- Operadores aritmeticos y de asignacion simple ---
t_MAS            = r'\+'
t_MENOS          = r'-'
t_MULTIPLICACION = r'\*'
t_DIVISION       = r'/'
t_MODULO         = r'%'
t_ASIGNACION     = r'='

# --- Comparacion simple (deben quedar despues de <=, >=, <<, >>) ---
t_MENOR          = r'<'
t_MAYOR          = r'>'

# --- Referencias (ampersand simple usado para &T, &mut T) ---
t_AMPERSAND_SIMPLE = r'&'
