Nombre: Cristobal Andrés Pino Poblete
Rol: 202104597-k
RUT: 21.125.616-8

Instrucciones: guardar los archivos "calculadora.py", "problemas.txt" y "desarrollos.txt" todos en la misma carpeta donde se ejecutará el archivo de la calculadora (revisar directorio a la hora de ejecutar en VS Code).

Notas sobre el programa: 
-El archivo "calculadora.py" puede resolver correctamente todos los tipos de operaciones, incluyendo algo de recursión en paréntesis. El orden de prioridad al resolver operaciones que elegí sigue como: CUPÓN -> parentesis -> multiplicación/división -> suma/resta. ANS es transformado automaticamente en cada operación y su valor se actualiza al final de la resolución de una linea de problema.

-También es capaz de escribir los resultados en "desarrollos.txt" de las lineas resueltas por bloque de problema. Punto importante: debe haber 2  saltos de línea después de cada bloque de problema para que funcione correctamente la escritura de resultados, en caso de faltar uno al final no va a escribir los resultados del último bloque de problemas.
Ejemplo de como tener el archivo "problemas.txt": **ultimo bloque de problema** -> salto de linea -> salto de linea

-La detección de errores puede detectar casos en CUPON, parentesis y la división por 0, además de casos como escribir mal ANS ("ASN" o "ANS65"). También es capaz de transformar resultados negativos en 0, y en caso de existir un numero negativo en la linea se considerará como error de syntax. Alguna linea que contenga solo un entero/ANS/cupón se considera como error de syntax. Cualquier error detectado es escrito e informado en "desarrollos.txt" en el formato indicado.

Adjunto en el archivo zip mi archivo "problemas.txt" y "desarrollos.txt" para probar el correcto funcionamiento de la calculadora.
Usé todos los casos de pruebas que estaban en AULA y el PDF y agruegué solo un bloque extra para probar unos casos de errores.