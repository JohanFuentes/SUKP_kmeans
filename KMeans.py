#Set de pruebas

listaTxt = list(["100_85_0.15_0.85.txt","100_100_0.15_0.85.txt","400_385_0.10_0.75.txt","300_300_0.10_0.75.txt","400_400_0.15_0.85.txt","400_400_0.10_0.75.txt","285_300_0.10_0.75.txt","200_200_0.15_0.85.txt","300_300_0.15_0.85.txt","100_100_0.10_0.75.txt","85_100_0.10_0.75.txt","500_500_0.10_0.75.txt","300_285_0.10_0.75.txt","500_500_0.15_0.85.txt","400_385_0.15_0.85.txt","300_285_0.15_0.85.txt","200_185_0.15_0.85.txt","185_200_0.15_0.85.txt","100_85_0.10_0.75.txt","185_200_0.10_0.75.txt","85_100_0.15_0.85.txt","500_485_0.15_0.85.txt","485_500_0.10_0.75.txt","385_400_0.10_0.75.txt","485_500_0.15_0.85.txt","500_485_0.10_0.75.txt","385_400_0.15_0.85.txt","200_200_0.10_0.75.txt","285_300_0.15_0.85.txt","200_185_0.10_0.75.txt"])

#####################         FUNCIONES           ###############################

def calcularPesoItem(filabinaria, pesosElementos):
  sumaPeso = 0
  indices = np.where(filabinaria == 1)
  for i in indices[0]:
    sumaPeso = sumaPeso + int(pesosElementos[i])
  return sumaPeso

def mejor(arrLargo, arrDist):
  largo = len(arrLargo)
  max = -10000
  indices = np.empty([largo])
  resultados = np.empty([largo])
  for i in range(largo):
    resultado = (0.1*arrLargo[i])-(0.9*arrDist[i])
    resultados[i] = resultado
    indices[i] = i
  resultadosOrdenados, indicesOrdenados = map(list, zip(*sorted(zip(resultados, indices))))
  return indicesOrdenados

def mejor_cluster(matriz, centro_cluster, label_cluster):
  mejorCluster = 0
  listaR = list()
  num_clusters = len(centro_cluster)
  arrayLargos = np.empty([num_clusters])
  resultados = np.empty([num_clusters])
  ArrayOrdenados = np.empty([num_clusters])
  for i in range(num_clusters):
    distancia_total = 0
    centro = centro_cluster[i]
    array = np.where(label_cluster == i)
    largo = len(array[0])
    arrayLargos[i] = largo
    arrayDistancias = np.empty([len(array[0])])
    contador = 0
    for index in array[0]:
      a = centro
      b = matriz[index]
      dist = np.linalg.norm(a-b)
      distancia_total = distancia_total + dist
      arrayDistancias[contador] = dist
      contador = contador + 1
    distancias, indices = map(list, zip(*sorted(zip(arrayDistancias, array[0]))))
    listaR.append(indices)
    promedio = distancia_total/largo
    resultados[i] = promedio
  mejorCluster = mejor(arrayLargos,resultados)
  return mejorCluster[::-1], listaR

def verificacion(aux,matrizItemElementos,list_ganancia_items,list_pesos_elementos):
  count = 0
  suma_ga = 0

  for i in aux:
    indices = np.where(matrizItemElementos[int(i)] == 1)
    suma_ga = suma_ga + int(list_ganancia_items[int(i)])
    count = count + 1

  sumaPeso = 0
  setIndicesPesos = set()

  for i in aux:
    indices = np.where(matrizItemElementos[int(i)] == 1)
    for j in indices[0]:
      setIndicesPesos.add(j)

  for k in setIndicesPesos:
    sumaPeso = sumaPeso + int(list_pesos_elementos[k])

  return count, suma_ga, sumaPeso

def marcar(inicial, filaGuia):
  for i in range(len(inicial)):
    if filaGuia[i] == 1 and inicial[i] == 0:
      inicial[i] = 1

def escogerPrimerItem(aux,matrizItemElementos,list_ganancia_items,list_pesos_elementos):
  mayor = 0
  indiceEscogido = -1
  contador = 0
  pos = -1

  for i in aux:
    gananciaItem = list_ganancia_items[int(i)]
    pesoItem = calcularPesoItem(matrizItemElementos[i], list_pesos_elementos)
    ganPeso = (int(gananciaItem) / int(pesoItem))
    if ganPeso > mayor:
      mayor = ganPeso
      indiceEscogido = i
      pos = contador
    contador = contador + 1
  return indiceEscogido, pos

def dif(inicial,vectorItem):
  a1 = np.where(vectorItem==1)
  a2 = a1[0]
  b1 = np.where(inicial==1)
  b2 = b1[0]
  inter = np.intersect1d(a2,b2)
  diferencia = len(a2) - len(inter)
  return diferencia

def agregarDif0(numero_clusters, labelsCluster, vectorInicial, mit, listaItemsEscogidos, itemsNoEscogidos,turnoValido):
  for indexCluster in range(numero_clusters):
    #ingresar todos los items que pueda
    for indiceItem in labelsCluster[indexCluster]: #Recorremos los items del cluster
      if(dif(vectorInicial,mit[indiceItem])==0):
        listaItemsEscogidos.append(indiceItem)
        labelsCluster[indexCluster].remove(indiceItem)
        if(len(labelsCluster[indexCluster])==0):
          turnoValido.update({indexCluster:False})
        itemsNoEscogidos.remove(indiceItem)
        #num_agregados = num_agregados + 1

def descartar(numero_clusters, labelsCluster, vectorInicial, mit, itemsNoEscogidos, turnoValido, capacidad):
  for indexCluster in range(numero_clusters):
    #ingresar todos los items que pueda
    lc = labelsCluster[indexCluster].copy()
    for indiceItem in lc: #Recorremos los items del cluster
      copiaVectorInicial = vectorInicial.copy()
      marcar(copiaVectorInicial, mit[indiceItem])
      copiaPeso = calcularPesoItem(copiaVectorInicial, list_pesos_elementos)

      if copiaPeso > capacidad:
        labelsCluster[indexCluster].remove(indiceItem)
        if(len(labelsCluster[indexCluster])==0):
          turnoValido.update({indexCluster:False})
        itemsNoEscogidos.remove(indiceItem)

def descartarLista(labelsCluster, vectorInicial, mit, itemsNoEscogidos, turnoValido, capacidad, listaAux, indexCluster):

  for indiceItem in listaAux: #Recorremos los items del cluster
    copiaVectorInicial = vectorInicial.copy()
    marcar(copiaVectorInicial, mit[indiceItem])
    copiaPeso = calcularPesoItem(copiaVectorInicial, list_pesos_elementos)

    if copiaPeso > capacidad:
      labelsCluster[indexCluster].remove(indiceItem)
      if(len(labelsCluster[indexCluster])==0):
        turnoValido.update({indexCluster:False})
      itemsNoEscogidos.remove(indiceItem)
      listaAux.remove(indiceItem)

def elementosEx(vectorItem,vectorInicial):
  a1 = np.where(vectorItem==1)
  a2 = a1[0]
  a3 = set(a2)
  b1 = np.where(vectorInicial==1)
  b2 = b1[0]
  b3 = set(b2)
  c = a3.difference(b3)
  return list(c)

def elementosEnItems(elemento, mit, itemsNoEscogidos): #en cuantos items esta presente el elemento
  cantidad = 0
  for item in itemsNoEscogidos:
    if(mit[item][elemento]==1):
      cantidad = cantidad + 1
  return cantidad

def borrarUnos(copiaMit,vectorInicial):
  for indiceItem in range(len(copiaMit)):
    for indiceElemento in range(len(copiaMit[indiceItem])):
      if vectorInicial[indiceElemento] == 1 and copiaMit[indiceItem][indiceElemento] == 1:
        copiaMit[indiceItem][indiceElemento] == 0

def numeroElementosItems(elemento, mit, itemsNoEscogidos,vectorInicial): #cantidad de elementos que tienen los items, en los que esta presente el elemento
  cantidad = 0
  copiaMit = mit.copy()
  borrarUnos(copiaMit,vectorInicial)
  for item in itemsNoEscogidos:
    if(copiaMit[item][elemento]==1):
      cantidad = cantidad + len(copiaMit[item].nonzero()[0])
  return cantidad

def mejorIt(listaItems,vectorInicial,mit,list_pesos_elementos,itemsNoEscogidos,list_ganancia_items):
  if(len(listaItems)==1):
    itemSeleccionado = listaItems[0]
  else: 
    itemSeleccionado = -1
    mayor = -1000
    elementosExtras = list()
    #Obtener los elementos de diferencia entre cada item y el vector inicial
    for indiceItem in listaItems:
      eEItems = 0      #
      nEItems = 0  #
      peso = 0
      elementosExtras = elementosEx(mit[indiceItem],vectorInicial)
      for indiceElemento in elementosExtras:
      #Obtener numero de items en los que esta el elemento, peso, numero de elementos que tiene los items en los que se encuentra el elemento
        peso = peso + int(list_pesos_elementos[indiceElemento])
        nEItems = nEItems + numeroElementosItems(indiceElemento,mit,itemsNoEscogidos,vectorInicial)
        #eEItems = eEItems + elementosEnItems(indiceElemento,mit,itemsNoEscogidos)
      #resultado = (nEItems/(peso*eEItems))*(int(list_ganancia_items[indiceItem]))*(int(list_ganancia_items[indiceItem])) #Incluyendo la ganancia por item
      resultado = (nEItems/peso)*(int(list_ganancia_items[indiceItem]))

      if resultado > mayor:
        mayor = resultado
        itemSeleccionado = indiceItem
  return itemSeleccionado

def diferenciaMinima(vectorInicial,mit,itemsNoEscogidos):
  difMinimo = 10000
  for indiceItem in itemsNoEscogidos:
    diferencia = dif(vectorInicial,mit[indiceItem])
    if diferencia < difMinimo:
      difMinimo = diferencia
  return difMinimo

#################################################################################
import math
import numpy as np
import random
import pandas as pd
from sklearn.metrics import silhouette_samples, silhouette_score
from sklearn.cluster import KMeans

listaGananciaTotal = list()
listaK = list()

for txt in listaTxt:
  print("#######################################",txt,"#########################################")
###################################### LEER ARCHIVO TXT #######################################################################
  fichero = open('C:\\Users\\johan\\Desktop\\JOHAN\\UNIVERSIDAD\\SUKP\\Greedys-20220831T150654Z-001\\Greedys\\Benchmarks\\'+txt)
  lineas = fichero.readlines()
  for linea in lineas:
      if linea == "\n":
        lineas.remove("\n")
  num_items = int(lineas[0])           #numero de items (entero)
  num_elementos = int(lineas[1])       #numero de elementos (entero)
  capacidad = int(lineas[2])           #capacidad de la mochila (entero)
  list_ganancia_items = (lineas[3].lstrip()).split(sep = " ") #lista de ganancia para cada item
  list_pesos_elementos = (lineas[4].lstrip()).split(sep = " ") #lista de peso para cada elemento
  
  try:
    list_pesos_elementos.remove("\n")
  except:
    print("")
  try:
    list_ganancia_items.remove("\n")
  except:
    print("")

  ganancia_items = np.array(list_ganancia_items)
  pesos_elementos = np.array(list_pesos_elementos)
  matrizItemElementos = np.empty((num_items,num_elementos)) #matriz que asocia los items con los elementos

  for j in range(num_items):
    line = lineas[j+5].split(sep = " ")
    
    for i in line:
      if i == "\n":
        line.remove("\n")
    matrizItemElementos[j:j+1] = line #Llenando la matriz
  
  mit = matrizItemElementos
  newMit = mit.copy()
############################  Definiendo el parametro K (cantidad de clusters) de Kmeans   #####################################################
#Una de las formas de estimar el mejor k es a traves del promedio de la silueta, el cual se mueve en un
#rango entre 0 y 1, mientras mas cercano a 1 es un mejor valor de k

  range_n_clusters = range(2,5) #2,3,4
  lista = list() #lista que contendra el promedio de la silueta para cada k
  for n_clusters in range_n_clusters:
    clusterer = KMeans(n_clusters=n_clusters, n_init=10, random_state=10)
    cluster_labels = clusterer.fit_predict(newMit)
    silhouette_avg = silhouette_score(newMit, cluster_labels)
    lista.append(silhouette_avg)

  #Encontrar los 3 K con mejor valor del promedio de la silueta
  copia_silueta = np.array([lista])
  clustersEscogidos = list()

  for i in range(3):
    indice = np.argmax(copia_silueta[0])
    max = copia_silueta[0][indice]
    copia_silueta[0][indice] = -1
    print(i+1,'. Para K:', indice+2, "=> promedio de la silueta:", max)
    clustersEscogidos.append(indice+2)

  X = newMit.copy()
  range_n_clusters = clustersEscogidos.copy()
  maximaGanancia = 0
  clustersMaximaGanancia = 0
#####################################   ALGORITMO   ########################################################################

  for n_clusters in range_n_clusters:
    print("Prueba con el cluster de tamaño: ",n_clusters)
    clusterer = KMeans(n_clusters=n_clusters, n_init=10, random_state=10)
    cluster_labels = clusterer.fit_predict(X)
    a,b = mejor_cluster(newMit,clusterer.cluster_centers_,cluster_labels)
    # a: es una lista que contiene los indices de los K clusters
    # b: lista que contiene k lista con los elementos de cada cluster
    itemsNoEscogidos = list(range(len(list_ganancia_items)))
    peso = 0
    labelsCluster = b
    numero_clusters = len(labelsCluster)
    turno = 0 # clusters que le toca escoger un item
    listaItemsEscogidos = list()
    vectorInicial = np.zeros(len(list_pesos_elementos)) # Contiene los elementos que se han considerado sus pesos

#Escoger un item por cada cluster
    for indiceCluster in range(numero_clusters):
      indiceEscogido, pos = escogerPrimerItem(labelsCluster[indiceCluster],matrizItemElementos,list_ganancia_items,list_pesos_elementos)
      listaItemsEscogidos.append(indiceEscogido)
      labelsCluster[indiceCluster].remove(indiceEscogido)
      marcar(vectorInicial, mit[indiceEscogido])
      itemsNoEscogidos.remove(indiceEscogido)

    peso = calcularPesoItem(vectorInicial, list_pesos_elementos) #Calcula el peso actual
    turnoValido = {0 : True, 1 : True, 2 : True, 3 : True}  # Valores boolenos que permiten saber si esta vacio un cluster (True: No vacio; False: Vacio)
    #turnoValido = {0 : True, 1 : True, 2 : True, 3 : True, 4 : True, 5 : True, 6 : True, 7 : True}
    agregarDif0(numero_clusters, labelsCluster, vectorInicial, mit, listaItemsEscogidos,itemsNoEscogidos,turnoValido) #Agrega todos los items que se puedan agregar con los elementos hasta ahora considerados
    diferenciaPermitida = diferenciaMinima(vectorInicial,mit,itemsNoEscogidos) # numero que indica la minima diferencia de elementos, entre el vector inicial y los elementos de los items
    
    while(len(itemsNoEscogidos)>0):  #Mientras la lista de items no escogidos no este vacia 
      listaAux = list()
      itemSeleccionado = -1
      if turno < numero_clusters:
        if(turnoValido.get(turno)):
          #Escoger un item del cluster numero "turno", entre los cuales tengan una diferencia igual a "diferenciaPermitida"
          for indiceItem in labelsCluster[turno]:
            if(dif(vectorInicial,mit[indiceItem])==diferenciaPermitida):
              listaAux.append(indiceItem) #Agrega a la lista todos los items del cluster que cumplan con la diferencia minima
    
          descartarLista(labelsCluster, vectorInicial, mit, itemsNoEscogidos, turnoValido, capacidad, listaAux, turno) #Elimina todos los items de la lista "listaAux" que al agregarse superarian la capacidad 
          
          while(len(listaAux)!=0):   
            itemSeleccionado = mejorIt(listaAux,vectorInicial,mit,list_pesos_elementos,itemsNoEscogidos,list_ganancia_items) #Selecciona el mejor item de la lista
            listaItemsEscogidos.append(itemSeleccionado)
            labelsCluster[turno].remove(itemSeleccionado)
            if(len(labelsCluster[turno])==0):
              turnoValido.update({turno:False})
            marcar(vectorInicial, mit[itemSeleccionado])
            itemsNoEscogidos.remove(itemSeleccionado)
            peso = calcularPesoItem(vectorInicial, list_pesos_elementos)
            descartar(numero_clusters, labelsCluster, vectorInicial, mit, itemsNoEscogidos, turnoValido, capacidad) #Elimina todos los items de los clusters que ya no cumplen la condicion de la capacidad maxima
            break
          turno = turno + 1 # Turno mas uno
        else:
          turno = turno + 1 # Turno mas uno
      else:
        turno = 0 #Vuelve a recorrer cada cluster
        diferenciaPermitida = diferenciaMinima(vectorInicial,mit,itemsNoEscogidos) #Nueva diferencia minima
      agregarDif0(numero_clusters, labelsCluster, vectorInicial, mit, listaItemsEscogidos,itemsNoEscogidos,turnoValido) #Agrega todos los items que se puedan agregar con los elementos hasta ahora considerados
      print("Largo",len(itemsNoEscogidos))
    a1,a2,a3 = verificacion(listaItemsEscogidos,matrizItemElementos,list_ganancia_items,list_pesos_elementos)
    print("Ganancia obtenida: ",a2)
    if(a2>maximaGanancia):
      maximaGanancia = a2
      clustersMaximaGanancia = n_clusters    
  listaK.append(clustersMaximaGanancia)
  listaGananciaTotal.append(maximaGanancia)

datosExportar = pd.DataFrame({'Txt' : listaTxt,'Valor de K' : listaK,'Ganancia Total': listaGananciaTotal})
result = pd.ExcelWriter('ResultadosKMeans3.xlsx')  
datosExportar.to_excel(result)
result.save()