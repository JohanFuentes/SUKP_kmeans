# SUKP_kmeans
Se resuelve el Set Union Knapsack Problem (SUKP), con el algoritmo de clusterización kmeans.
## SUKP
Set-Union Knapsack Problem (SUKP), es una generalización del problema de la mochila, que puede ser formulado para aplicaciones adicionales. 

Se puede definir de la siguiente manera:

- Elementos: U = {1,...,n}
- Pesos: wj > 0 (j = 1,...,n)
- Items: V = {1,...,m}
- Capacidad : C > 0 

Donde cada ítem i (i = 1,...,m), está asociado a un subconjunto de elementos ( Ui  U ), esto es determinado a través de una matriz, donde las filas corresponden a los ítems y las columnas a los elementos. Esta matriz relaciona los elementos con los ítems, donde los elementos que pertenecen a un ítem, tienen el valor de 1 y los que no pertenecen, tienen el valor de 0. Además cada ítem tiene un beneficio asociado,

- Beneficio: Pi > 0

El objetivo del SUKP es encontrar un subconjunto de ítems que maximicen el beneficio, con la restricción de que, la suma de los pesos de los elementos asociados a los ítems escogidos, no sobrepasen la capacidad de la mochila. Algo importante a mencionar es que si existen elementos que estén relacionados a más de un ítem y estos ítems son escogidos, solo es considerado el peso del elemento una vez.
