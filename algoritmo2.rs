// algoritmo2.rs
// Algoritmo de prueba - Paul Alcivar Zavala
// Cubre: tipos de datos primitivos, literales, estructuras de datos, delimitadores

struct Persona {
    nombre: String,
    edad: u8,
    altura: f64,
    activo: bool,
}

fn main() {
    let nombre: String = String::from("Maria");
    let edad: u8 = 25;
    let altura: f64 = 1.68;
    let activo: bool = true;
    let inicial: char = 'M';

    let persona = Persona {
        nombre: nombre,
        edad: edad,
        altura: altura,
        activo: activo,
    };

    let numeros: Vec<i32> = vec![1, 2, 3, 4, 5];

    for n in &numeros {
        println!("Numero: {}", n);
    }

    let opcion: Option<i32> = Some(10);
}
