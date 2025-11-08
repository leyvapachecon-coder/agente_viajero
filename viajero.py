import random
import numpy as np
import pandas as pd
import operator


# CLASE MUNICIPIO

# esta clase representa cada ciudad o punto del mapa con coordenadas X, Y
# esta clase nos sirve como unidad basica en la ruta, y sus distancias se usan
# para evaluar la calidad de cada solucion
class Municipio:
    # aqui inicializamos el municipio con su nombre y coordendas
    def __init__(self, nombre, x, y):
        self.nombre = nombre
        self.x = x
        self.y = y
    
    # aqui calculamos la distancia entre este municipio y otro
    # por medio de la formula del teorema de pitagoras
    def distancia(self, otro):
        xDis = abs(self.x - otro.x)
        yDis = abs(self.y - otro.y)
        return np.sqrt((xDis ** 2) + (yDis ** 2))

    # Este método nos devuelve uan representación legible del municipio
    # para mostrar en consola
    def __repr__(self):
        return f"{self.nombre} ({self.x}, {self.y})"



# CLASE APTITUD
# esta clase lo que hace es evaluar la calidad (o la función fitness) de una ruta
# se supone que una mas corta tiene mayor aptitud
class Aptitud:
    # recibimos una lista de objetos municipio que conforman una posible ruta
    def __init__(self, ruta):
        self.ruta = ruta
        self.distancia_total = 0
        self.valor_aptitud = 0.0

    # aqui sumamos todas las diferencias entre municipios consecutivos
    def calcular_distancia(self):
        if self.distancia_total == 0:
            distancia_relativa = 0
            for i in range(len(self.ruta)):
                punto_inicial = self.ruta[i]
                punto_final = self.ruta[(i + 1) % len(self.ruta)]
                distancia_relativa += punto_inicial.distancia(punto_final)
            self.distancia_total = distancia_relativa
        return self.distancia_total

    # en este metodo retornamos la inversa de la distancia total 
    # a menos distancia, va haber mayor aptitud
    def calcular_aptitud(self):
        if self.valor_aptitud == 0:
            self.valor_aptitud = 1 / float(self.calcular_distancia())
        return self.valor_aptitud



# FUNCIONES DEL ALGORITMO GENÉTICO

# ----- Inicialización de la población -----
# aquí en este metodo creamos una ruta random
def crear_ruta(lista_municipios):
    return random.sample(lista_municipios, len(lista_municipios))
# aqui generamos una lista de rutas aleartorias, en pocas palabras, la poblacion incial
# este metodo es muy importante, ya que es el punto de partida de la evolucion genetica
def generar_poblacion_inicial(tamano_pob, lista_municipios):
    return [crear_ruta(lista_municipios) for _ in range(tamano_pob)]


# ----- Evaluación de la aptitud -----

# aqui evaluamos todas las rutas mediante la clase Aptitud, y las ordenamos de mejor a peor
# segun el fitness
def clasificar_rutas(poblacion):
    resultados = {i: Aptitud(ruta).calcular_aptitud() for i, ruta in enumerate(poblacion)}
    return sorted(resultados.items(), key=operator.itemgetter(1), reverse=True)


# ----- Selección de individuos -----

# elegimos las rutas que pasaran a la siguiente generacion
# para eso, usamos dos metodos, el de seleccion directa y el probabilistica
def seleccionar_rutas(pop_ranked, num_seleccionados):
    resultados = []
    df = pd.DataFrame(np.array(pop_ranked), columns=["Indice", "Aptitud"])
    df['cum_sum'] = df['Aptitud'].cumsum()
    df['cum_perc'] = 100 * df['cum_sum'] / df['Aptitud'].sum()

    # Selección directa de los mejores
    for i in range(num_seleccionados):
        resultados.append(pop_ranked[i][0])

    # Selección por probabilidad
    for _ in range(len(pop_ranked) - num_seleccionados):
        seleccion = 100 * random.random()
        for i in range(len(pop_ranked)):
            if seleccion <= df.iloc[i, 3]:
                resultados.append(int(df.iloc[i, 0]))
                break

            
    return resultados

# aqui creamos un grupo de padres con las rutas seleccionadas
def grupo_apareamiento(poblacion, seleccionados):
    return [poblacion[i] for i in seleccionados]


# ----- reproducción -----

# creamos un hijo mezclando partes de dos rutas, tomamos un segmento de un progenitor
# y lo completamos con genes del otro sin duplicar a los municipios
def cruzar(progenitor1, progenitor2):
    hijo_p1 = []
    hijo_p2 = []

    gene_a = int(random.random() * len(progenitor1))
    gene_b = int(random.random() * len(progenitor2))

    inicio_gen = min(gene_a, gene_b)
    fin_gen = max(gene_a, gene_b)

    for i in range(inicio_gen, fin_gen):
        hijo_p1.append(progenitor1[i])

    hijo_p2 = [item for item in progenitor2 if item not in hijo_p1]

    return hijo_p1 + hijo_p2

# aqui generamos una nueva poblacion partiendo de los padres seleccionados
def reproducir_poblacion(grupo_apareamiento, num_elite):
    hijos = []
    longitud = len(grupo_apareamiento) - num_elite
    seleccion = random.sample(grupo_apareamiento, len(grupo_apareamiento))

    for i in range(num_elite):
        hijos.append(grupo_apareamiento[i])

    for i in range(longitud):
        hijo = cruzar(seleccion[i], seleccion[len(grupo_apareamiento) - i - 1])
        hijos.append(hijo)
    return hijos


# ----- Mutación -----

#intercambiamos aleartoriamente 2 posiciones en una ruta, con una cierta probabilidad
# para evitar que el algoritmo se quede estancado en una sola solucion
def mutar(individuo, tasa_mutacion):
    for i in range(len(individuo)):
        if random.random() < tasa_mutacion:
            j = int(random.random() * len(individuo))
            individuo[i], individuo[j] = individuo[j], individuo[i]
    return individuo

# aplicamos la mutaciona a toda la poblacion
def mutar_poblacion(poblacion, tasa_mutacion):
    return [mutar(ind, tasa_mutacion) for ind in poblacion]


# ----- Crear nueva generación -----

# aqui producimos una nueva poblacion aplicando los pasos:
# 1.- evaluacion / 2.- seleccion / 3.- cruce / 4.- mutacion
def nueva_generacion(poblacion_actual, num_elite, tasa_mutacion):
    rutas_ordenadas = clasificar_rutas(poblacion_actual)
    seleccionados = seleccionar_rutas(rutas_ordenadas, num_elite)
    grupo = grupo_apareamiento(poblacion_actual, seleccionados)
    hijos = reproducir_poblacion(grupo, num_elite)
    nueva_pob = mutar_poblacion(hijos, tasa_mutacion)
    return nueva_pob


# ----- Algoritmo Genético Principal -----

#aqui, controlamos el flujo general del algortimo
# 1.- generamos la poblacion inicial / 2.- iteramos las generaciones / 3.- muestra la distancia inicial y final
# 4.- devuelve la mejor ruta encontrada
def algoritmo_genetico(lista_municipios, tamano_pob, num_elite, tasa_mutacion, generaciones):
    poblacion = generar_poblacion_inicial(tamano_pob, lista_municipios)
    print(f"Distancia inicial: {1 / clasificar_rutas(poblacion)[0][1]:.2f}")

    for i in range(generaciones):
        poblacion = nueva_generacion(poblacion, num_elite, tasa_mutacion)
    mejor_resultado = clasificar_rutas(poblacion)[0]
    mejor_ruta = poblacion[mejor_resultado[0]]
    print(f"Distancia final: {1 / mejor_resultado[1]:.2f}")
    print("Mejor ruta encontrada:", mejor_ruta)
    return mejor_ruta



# PROGRAMA PRINCIPAL

# aqui en el programa principal, creamos una lista de objetos Municipio con coordenadas reales, por ende,
# llamamos al metodo "algoritmo_genetico()" con algunos parametros ya definidos
# como resultado, nos va a mostrar en consola la distancia incial, la distancia final optimizada y la mejor ruta
if __name__ == "__main__":
    # aqui ya se corrigio el error que habia al momento de crear objetos de tipo municipio
    # por lo cual el codigo ya funciona correctamente
    ciudades = [
        Municipio("Madrid", 40.4168, -3.7038),
        Municipio("Barcelona", 41.3784, 2.1925),
        Municipio("Valencia", 39.4699, -0.3763),
        Municipio("Sevilla", 37.3891, -5.9845),
        Municipio("culiacan", 37.3894, -7.4745),
         Municipio("mazatlan", 35.3894, -4.4745),
          Municipio("mochis", 32.3894, -3.4745),
           Municipio("italia", 31.3894, -2.4745)
    ]

    # Ejecutamos el algoritmo genético con algunos valores ya predefinidos
    algoritmo_genetico(
        lista_municipios=ciudades,
        tamano_pob=100,
        num_elite=20,
        tasa_mutacion=0.01,
        generaciones=200
    )
