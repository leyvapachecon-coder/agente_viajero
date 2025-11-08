import random
from viajero import Municipio, Aptitud, seleccionar_rutas, cruzar, mutar

# PRUEBAS UNITARIAS DEL ALGORITMO GENÉTICO 
# en este archivo nos encargamos de ver si los metodos que establecimos en el archivo
# viajero.py estan funcionando correctamente

# Verificamos que la función de aptitud calcule correctamente la distancia total de una ruta y 
# que devuelva una aptitud coherente con esa distancia.
def prueba_funcion_aptitud():
    a = Municipio("A", 0, 0)
    b = Municipio("B", 3, 0)
    c = Municipio("C", 6, 0)
    ruta = [a, b, c]

    aptitud = Aptitud(ruta)
    distancia = aptitud.calcular_distancia()
    assert round(distancia, 2) == 12.00, "Error en la distancia"
    print("Función de aptitud funciona correctamente.")

# aqui comprobamos que el proceso de selección de rutas dentro del algoritmo genético esté funcionando 
# adecuadamente.
def prueba_seleccion():
    poblacion_simulada = [(i, random.uniform(0.1, 1.0)) for i in range(10)]
    poblacion_simulada = sorted(poblacion_simulada, key=lambda x: x[1], reverse=True)
    seleccionados = seleccionar_rutas(poblacion_simulada, 3)
    assert len(seleccionados) == len(poblacion_simulada), "Error en selección"
    print("Proceso de selección funcionando correctamente.")

#en este metodo garantizamos que las funciones de cruce y mutación generen
#  descendientes válidos y sin errores.
def prueba_cruce_mutacion():
    municipios = [
        Municipio("A", 0, 0),
        Municipio("B", 1, 2),
        Municipio("C", 2, 3),
        Municipio("D", 3, 1),
        Municipio("E", 4, 0)
    ]

    padre1 = random.sample(municipios, len(municipios))
    padre2 = random.sample(municipios, len(municipios))
    hijo = cruzar(padre1, padre2)
    assert len(hijo) == len(set(hijo)), "Error: hijo con duplicados"
    hijo_mutado = mutar(hijo.copy(), 0.5)
    assert len(hijo_mutado) == len(hijo), "Error: mutación incorrecta"
    print("Cruce y mutación generan descendencia válida.")



# EJECUCIÓN DE LAS PRUEBAS
if __name__ == "__main__":
    print("==============================================")
    print("INICIANDO PRUEBAS DEL ALGORITMO GENÉTICO")
    print("==============================================")
    prueba_funcion_aptitud()
    prueba_seleccion()
    prueba_cruce_mutacion()
   
