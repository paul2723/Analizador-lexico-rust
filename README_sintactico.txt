ANALIZADOR SINTACTICO DE RUST CON PLY

Archivos principales:
- lexer.py: analizador lexico existente.
- parser.py: analizador sintactico construido con ply.yacc.
- ejecutar_sintactico.py: ejecuta el analisis sobre archivos .rs y genera logs.
- algoritmo1.rs, algoritmo2.rs, algoritmo3.rs: archivos de prueba por integrante.
- logs/: carpeta donde se guardan resultados lexicos y sintacticos.

Comandos de prueba:
python ejecutar_sintactico.py algoritmo1.rs CristhianHerrera
python ejecutar_sintactico.py algoritmo2.rs PaulAlcivar
python ejecutar_sintactico.py algoritmo3.rs GustavoMoscoso

Nota:
algoritmo3.rs incluye intencionalmente el simbolo '$' para demostrar que el lexer
lo reporta como error y que el parser puede registrar el problema sintactico derivado.
