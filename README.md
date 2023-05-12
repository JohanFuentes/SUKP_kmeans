# SUKP_kmeans
Se resuelve el Set Union Knapsack Problem (SUKP), con el algoritmo de clusterización kmeans.
## SUKP
Set-Union Knapsack Problem (SUKP), es una generalización del problema de la mochila, que puede ser formulado para aplicaciones adicionales. 

Se puede definir de la siguiente manera:

- Elementos: U = {1,...,n}
- Pesos: W_j > 0 (j = 1,...,n)
- Items: V = {1,...,m}
- Capacidad : C > 0 

Donde cada ítem i (i = 1,...,m), está asociado a un subconjunto de elementos ( U_i C U ), esto es determinado a través de una matriz, donde las filas corresponden a los ítems y las columnas a los elementos. Esta matriz relaciona los elementos con los ítems, donde los elementos que pertenecen a un ítem, tienen el valor de 1 y los que no pertenecen, tienen el valor de 0. Además cada ítem tiene un beneficio asociado,

- Beneficio: P_i > 0

El objetivo del SUKP es encontrar un subconjunto de ítems que maximicen el beneficio, con la restricción de que, la suma de los pesos de los elementos asociados a los ítems escogidos, no sobrepasen la capacidad de la mochila. Algo importante a mencionar es que si existen elementos que estén relacionados a más de un ítem y estos ítems son escogidos, solo es considerado el peso del elemento una vez.

## Kmeans
K-means es un algoritmo de aprendizaje automático utilizado en el campo de la minería de datos y el análisis de datos no supervisado. Su objetivo principal es agrupar un conjunto de datos en diferentes grupos basados en sus características y similitudes. El algoritmo busca encontrar los "k" centroides óptimos que representen los grupos.

## Algoritmo
Con Kmeans se agrupan los items en base a la similitud de sus elementos, para luego ir escogiendo de cada clusters 1 item.
Para saber la cantidad de clusters (valor de K) a utilizar, se utiliza el promedio de la silueta, la cual es una técnica utilizada para evaluar la calidad de la agrupaciones realizadas. Entrega una medida de cuán bien se agrupan los objetos dentro de sus propios clusters en comparación con los clusters vecinos. El promedio de la silueta varía entre -1 y +1. Un valor de silueta cercano a 1 indica que el objeto está bien emparejado con su propio cluster y mal emparejado con los clusters vecinos. Esto indica una buena calidad de agrupación.
