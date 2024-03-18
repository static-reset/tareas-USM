import re

""" EBNF / ReGex: se han hecho expresiones de todo el EBNF en el documento, más unas expresiones especificas para ciertas funciones. """
digito = r"[1-9]"
digito_o_zero = digito+r"|0"
entero = r"("+digito+r"("+digito_o_zero+r")*|0)"
espacio = r"[ ]"
clave = r'ANS|CUPON\(('+espacio+r')*('+entero+r"|ANS)(("+espacio+r")*,("+espacio+r")*("+ entero+r"|ANS)("+espacio+r")*)?\)"
"""En el regex de los cupones, se incluye un lookahead que verifica que no incluya otro cupon dentro del parentesis para hacer match."""
cupon_nor = r"CUPON\(("+espacio+r')*(?!CUPON\(\))('+entero+r"|ANS)("+espacio+r")*\)"
cupon_spe = r"CUPON\(("+espacio+r')*(?!CUPON\(\))('+entero+r"|ANS)("+espacio+r")*,("+espacio+r")*(?!CUPON\(\))("+ entero+r"|ANS)("+espacio+r")*\)"
operador = r"("+espacio+r")*([+]|[-]|[*]|(\/\/))("+espacio+r")*"
operador_sumres = r"("+espacio+r")*([+]|[-])("+espacio+r")*"
operador_muldiv = r"("+espacio+r")*([*]|(\/\/))("+espacio+r")*"
operacion = r"("+clave+r"|"+entero+r")"+operador+r"("+ clave +r"|"+ entero+r")"
operacion_sumres = r"("+clave+r"|"+entero+r")"+operador_sumres+r"("+ clave +r"|"+ entero+r")"
operacion_muldiv = r"("+clave+r"|"+entero+r")"+operador_muldiv+r"("+ clave +r"|"+ entero+r")"
sentencia = operacion+r"("+operador+r"("+clave+r"|"+entero+r"))*"
parentesis = r"\("+operacion+r"\)"


results = {"ANS": 0}
""" Diccionario "results": solo se usa para almacenar el valor de una linea resuelta. """

## Funciones Complementarias ##

def cupon_normal(x):
    valX = 0
    if x.isdigit() is True:
        valX = int(x)
    else: 
        if x == "ANS":
          valX = results["ANS"]
    cupon = int(valX * 20/100)
    return str(cupon)
""" Función de CUPON estandar: recibe el valor en el parentesis del cupón y retorna el 20% de ese valor como un string. """

def cupon_extra(x,y):
    valX = 0
    valY = 0
    if x.isdigit() is True:
        valX = int(x)
    else: 
        if x == "ANS":
          valX = results["ANS"]
        if re.search(cupon_nor, x) != None or re.search(cupon_spe, x) != None:
            return
    if y.isdigit() is True:
        valY = int(y)
        if valY == 0:
            return
    else:
        if y == "ANS":
          valY = results["ANS"]
        if re.search(cupon_nor, y) != None or re.search(cupon_spe, y) != None:
            return
    cupon = int(valX * (valY/100))
    return str(cupon)
""" Función cupon extra: recibe los 2 valores del parentesis del cupón y retorna el y% del primer valor. """

def separacion(string):
    if re.search(cupon_spe, string) != None:
            datos_cupon = re.search(cupon_spe, string).group().strip("\nCUPON()").split()
            val1 = datos_cupon[0].strip(",")
            val2 = datos_cupon[1]
            resultado_operacion = re.sub(cupon_spe, cupon_extra(val1, val2), string, count = 1)
            string = resultado_operacion
            if re.search(cupon_spe, string) != None:
                return separacion(string)
    if re.search(cupon_nor, string) != None:
            datos_cupon = re.search(cupon_nor, string).group().strip("\nCUPON()").split()
            val = datos_cupon[0]
            resultado_operacion = re.sub(cupon_nor, cupon_normal(val), string, count = 1)
            string = resultado_operacion
            if re.search(cupon_nor, string) != None:
                return separacion(string)
    if re.search(parentesis, string) != None:
        datos_parentesis = re.search(parentesis, string).group().strip("()").split()
        val1 = datos_parentesis[0]
        simbolo = datos_parentesis[1]
        val2 = datos_parentesis[2]
        resultado_parentesis = re.sub(parentesis, resolver(val1, simbolo, val2), string, count = 1)
        string = resultado_parentesis
        if re.search(parentesis, string) != None:
            return separacion(string)
    if re.search(sentencia, string) != None:
        if re.search(operacion_muldiv, string) != None:
                datos_op = re.search(operacion_muldiv, string).group().strip("\n").split()
                val1 = datos_op[0]
                simbolo = datos_op[1]
                val2 = datos_op[2]
                if simbolo == "//" and val2 == "0":
                    results["ANS"] = "Error"
                    return
                resultado_operacion = re.sub(operacion_muldiv, resolver(val1, simbolo, val2), string, count = 1)
                string = resultado_operacion
                if re.search(operacion_muldiv, string) != None or re.search(parentesis, string) != None:
                    return separacion(string)
        if re.search(operacion_sumres, string) != None:
                datos_op = re.search(operacion_sumres, string).group().strip("\n").split()
                val1 = datos_op[0]
                simbolo = datos_op[1]
                val2 = datos_op[2]
                resultado_operacion = re.sub(operacion_sumres, resolver(val1, simbolo, val2), string, count = 1)
                string = resultado_operacion
                if re.search(operacion_sumres, string) != None or re.search(parentesis, string) != None:
                    return separacion(string)
    if string.strip("\n").isdigit() == False:
        results["ANS"] = "Error"
        return
    results["ANS"] = int(string)
    return results["ANS"]
""" Función separacion/reemplazo: esta función sirve como el principal metodo de analisis de syntax y recursión. Recibe el string de la linea actual.
Al encontrar un match de regex, se guarda en una variable el string del match y se aplica la función strip para remover caracteres
que no sean enteros u operadores y se aplica split para poder guardar en una lista los elementos de interés y posteriormente
almacenarlos en variables individuales. Se llama a la función de regex .sub(), la cual reemplazará el match de operación encontrado
con el resultado obtenido de las funciones cup o resolver (y se especifica que reemplaze solo 1 vez para evitar errores) y retorna
el string actualizado. Se reemplaza el string original con el string obtenido de sub y se consulta si existen más matches de la
operación actual, ya que en caso de que sí existan se llama recursivamente a la función y en caso contrario continua con las otras
operaciones y retorna un string del resultado obtenido de la linea."""


operaciones = {"+": (lambda x,y: x+y), "-": (lambda x,y: x-y), "*": (lambda x,y: x*y), "//": (lambda x,y: x//y)}
def resolver(a, op, b):
    valA = 0
    valB = 0
    if a.isdigit() is True:
        valA = int(a)
    else: 
        if a == "ANS":
          valA = results["ANS"]
    if b.isdigit() is True:
        valB = int(b)
    else:
        if b == "ANS":
          valB = results["ANS"]
    resultado = operaciones[op](valA,valB)
    if resultado <= 0:
        resultado = 0
        return str(resultado)
    else:
        return str(resultado)
""" Diccionario y función resolver: Este diccionario tiene como llaves a los operadores, y las claves serán funciones lambda
que retornan el resultado de la operación de la lleva. Cada función lambda recibe 2 argumentos. La función resolver recibe
3 argumentos: 2 valores (enteros o ANS) y un operador. """

## Codigo Principal ##

"""Con la función with se abre el archivo para leer las lineas de problemas, escribir en desarrollos y cerrarlo automaticamente
al llegar al final del archivo problemas. Al principio se crea un diccionario que almacenará los resultados de cada linea. En caso
de encontrar un error, se guardara el resultado de la linea como error, y al revisar el bloque de problema se reemplazaran los
resultados de otras lineas como no reseultas. Si se  detecta solo un newline/whitespace en la linea, se escriben los desarrollos,
se limpia el diccionario de las lineas junto con sus resultados y se reinicia el valor de ANS a 0."""
with open("problemas.txt", "r") as problemas, open("desarrollos.txt", "w") as desarrollos:
    problema = {}
    for linea in problemas:
        if re.fullmatch("\n", linea) != None: 
            if "Error" in problema.values():
                for lin, res in problema.items():
                    if res != "Error":
                        desarrollos.write(lin+" = Sin resolver\n")
                    else:
                        desarrollos.write(lin+" = "+res+"\n")
            else:
                for lin, res in problema.items():
                    desarrollos.write(lin+" = "+res+"\n")
            desarrollos.write("\n")
            results["ANS"] = 0
            problema = {}
            continue
        linea_aux = linea.strip("\n")
        separacion(linea)
        problema[linea_aux] = str(results["ANS"])