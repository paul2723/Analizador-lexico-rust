// algoritmo1.rs
// Algoritmo de prueba - Cristhian Herrera
// Cubre: palabras reservadas, identificadores, comentarios de linea y bloque

/*
 * Funcion que calcula el factorial de un numero usando recursividad.
 * Sirve para probar: fn, let, mut, if, else, return, identificadores.
 */
fn factorial(n: u32) -> u32 {
    if n == 0 {
        return 1;
    } else {
        return n * factorial(n - 1);
    }
}

fn main() {
    let mut contador: i32 = 0;
    let limite = 5;

    while contador < limite {
        let resultado = factorial(contador as u32);
        println!("Factorial de {} es {}", contador, resultado);
        contador += 1;
    }
}