// algoritmo3.rs
// Algoritmo de prueba - Integrante 3
// Cubre: operadores aritmeticos, logicos, comparacion, bits
// Incluye intencionalmente un caracter invalido para probar deteccion de errores lexicos.

fn evaluar(a: i32, b: i32) -> bool {
    let suma = a + b;
    let resta = a - b;
    let producto = a * b;
    let division = a / b;
    let modulo = a % b;

    let es_igual = a == b;
    let es_diferente = a != b;
    let es_mayor = a > b;
    let es_menor_igual = a <= b;

    let resultado_logico = (a > 0) && (b > 0) || (a == 0);

    let desplazado = a << 2;
    let combinado = a & b;

    return es_igual && resultado_logico;
}

fn main() {
    let x = 10;
    let y = 3;
    let r = evaluar(x, y);

    // La siguiente linea contiene un caracter no valido en Rust ('$')
    let z = x $ y;
}
