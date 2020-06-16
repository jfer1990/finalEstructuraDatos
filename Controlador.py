from modelo import *
from vista import view
import tkinter

class Controlador:
    def __init__(self):
        self._master = tkinter.Tk()
        self._modelo = Graphs()
        self._vista = view(self._master)

        self.aux = None
        self.diccionarioLugares = {}
        self.nodeList = self.cargaNodos()
        self.edgeList = []
        self.L = self.cargaConjuntoAristas()
        self.Lmapeo = {}
        self.listaRelaciones = self.generaAdyacencia()
        self.weightDictionary = {("v5","v0"):45,("v0","v5"):45,("v0","v1"):30,("v1","v0"):30,("v6","v7"):50,("v7","v6"):50,
                                 ("v5","v6"):35,("v6","v5"):35,("v0","v6"):20,("v6","v0"):20,
                                 ("v1","v2"):25,("v2","v1"):25,("v2","v9"):20,("v9","v2"):20,("v9","v4"):30,("v4","v9"):30,
                                 ("v9","v8"):30,("v8","v9"):30,("v4","v8"):20,("v8","v4"):20,
                                 ("v5","v10"):50,("v10","v5"):50, ("v3","v10"):80, ("v10","v3"):80, ("v4","v11"):30, ("v11","v4"):30,
                                 ("v3","v11"):20, ("v7","v10"):80,("v11","v3"):20, ("v10","v7"):80,
                                 ("v11","v10"):90, ("v11","v12"):35, ("v4","v12"):65, ("v10","v11"):90, ("v12","v11"):35, ("v12","v4"):65,
                                 ("v10","v13"):100, ("v11","v13"):110,("v13","v10"):100, ("v13","v11"):110,
                                 ("v12","v13"):90, ("v15","v14"):60, ("v16","v14"):50, ("v13","v12"):90, ("v14","v15"):60, ("v14","v16"):50,
                                 ("v16","v15"):75, ("v14","v13"):175,("v15","v16"):75, ("v13","v14"):175,
                                 ("v15","v13"):200,("v7","v9"):15,("v13","v15"):200,("v9","v7"):15,
                                 ("v9","v3"):5,("v6","v10"):30,("v3","v9"):5,("v10","v6"):30}

        self.listaLineasDibujadas = []
        self.listaOvalosSeleccionados = []
        self.nodosDibujados = []


        self.nodoRaiz = None
        self.nodoDestino = None

        self.canvas = self._vista.lienzo
        self.canvas.bind('<Double-Button-1>',self.selectPositions)



     #   self._vista.button.bind('<Button-1>',self.adyacencia)
    def run(self):
        self._master.title("Mapa Ciencias Exactas UADY")
        self._master.deiconify()
        self._master.mainloop()


    #Precondicion: recibe una tupla de posiciones: (xRel,yRel)
    #Returns una tupla de la lista de posiciones de la clase vista o Falso si no hay coincidencias
    def isPoint(self,position):
        for key,tupla in self._vista.diccionarioPosiciones.items():
            name = tupla[0]
            pos = tupla[1]
            if self.isCollision(pos,position):
                return (key,name,pos[0],pos[1])
        return False

    #Precondición: recibe 2 tuplas (x,y) representando posiciones cada una
    #PostCondición: no hay sideEffects.
    #Returns: predicado si los puntos colisionan: True.
    def isCollision(self,tupla1,tupla2):

        rad = self._vista.rad
        rad = self.absX(rad)+10
        x0 = self.absX(tupla1[0])
        y0 = self.absX(tupla1[1])
        x1 = self.absX(tupla2[0])
        y1 = self.absX(tupla2[1])

        distAB = ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** (1 / 2)
        if distAB <= 2 * rad:
            return True
        else:
            return False
    def absX(self,numb):
        prom = (self.canvas.winfo_width()+self.canvas.winfo_height())/2
        return numb*prom
    def cargaNodos(self):
        lista = []
        for key,tupla in self._vista.diccionarioPosiciones.items():
            name = key
            nombreLugar = tupla[0]
            self.diccionarioLugares[name] = nombreLugar
            posicion = tupla[1]
            x = posicion[0]
            y = posicion[1]
            currentNode = Node(Position(x,y),name,.003)
            lista.append(currentNode)
            self._modelo.addNode(currentNode)
        return lista
    def _EdgesScripts(self,event):

        pos = self._vista.getRelPos(event)
        point = self.isPoint(pos)
        if point != False:
            if self.aux == None:
                self.aux = point
                self.edgeList.append((point[1],point[2]))
            else:
                x1 = point[1]
                y1 = point[2]
                x2 = self.aux[1]
                y2 = self.aux[2]
                self.edgeList.append((point[1],point[2]))
                pos1 = self._vista.getAbsPos((x1, y1))
                pos2 = self._vista.getAbsPos((x2, y2))
                self.canvas.create_line(pos1[0], pos1[1], pos2[0], pos2[1], fill='red')
                self.aux = None
                #print(self.edgeList)
                self.edgeList.clear()
        else:
            self.edgeList.append(pos)
    def selectPositions(self,event):
        pos = self._vista.getRelPos(event)
        point = self.isPoint(pos)
        if point != False:
            keyNode = point[0]
            if self.nodoRaiz == None:
                for nodo in self.nodeList:
                    if nodo.getName()==keyNode:
                        self.nodoRaiz = nodo
            else:
                for nodo in self.nodeList:
                    if nodo.getName()==keyNode:
                        self.nodoDestino = nodo
                self.crearRuta(self.nodoRaiz, self.nodoDestino)
                self.nodoRaiz = None
                self.nodoDestino = None





    def cargarGrafo(self):
        for node in self.nodeList:
            if not self._modelo.addNode(node):
                print("error")
                return False
            # for each in self.nodeList:
            #   print(each.getName()+" position: "+str(each.getPos().getX())+","+str(each.getPos().getY())+"radio: "+str(each.getRad()))
        return True

    def cargaConjuntoAristas(self):
        listaLineas = []
        file = open("coordenadasAristas.txt","r")
        linesInText = file.read().splitlines()
        for line in linesInText:
            lista = []
            line = line.split("=")
            lineSet = line[1].replace(" ","")
            lineSet = lineSet.replace("[","")
            lineSet = lineSet.replace("]","")
            lineSet = lineSet.replace("(","")
            lineSet = lineSet.replace("),",";")
            lineSet = lineSet.replace(")","")
            lineSet = lineSet.split(";")
            for elemento in lineSet:
                elemento = elemento.split(",")
                tupla = (float(elemento[0]),float(elemento[1]))
                lista = lista+[tupla]
            listaLineas.append(lista)
        return listaLineas

    #Esta función puede dividirse en 2, ya que carga en el modelo una lista de adyacencia pero igual
    #modifica el atributo self.lmapeo de la clase controlador, por tiempo fue implementada así.
    def generaAdyacencia(self):
        for sublista in self.L:
            tupla1 = sublista[0]
            tupla2 = sublista[len(sublista)-1]
            for nodo1 in self.nodeList:
                for nodo2 in self.nodeList[1:]:
                    nodo1Tupla = (nodo1.getPos().getX(),nodo1.getPos().getY())
                    nodo2Tupla = (nodo2.getPos().getX(),nodo2.getPos().getY())
                    if nodo1Tupla[0] == tupla1[0] and nodo1Tupla[1] == tupla1[1]:
                        if nodo2Tupla[0] == tupla2[0] and nodo2Tupla[1] == tupla2[1]:
                            self._modelo.createEdge(nodo1,nodo2)
                            self.Lmapeo[(nodo1.getName(),nodo2.getName())] = (sublista)
                            self.Lmapeo[(nodo2.getName(),nodo1.getName())] = (sublista)

    def probarDijkstra(self):
        pos = self._vista.diccionarioPosiciones
        for nodo in self.DijkstraPath:
            posicion = pos.get(nodo.getName())
            if nodo.getName() != self.nodoRaiz.getName():
                parent = pos.get(nodo.parent.getName())
                print(parent[0] + " -> " + str(posicion[0]) + " " + str(nodo.distance))

    # Invariante de lazo: todo nodo  tiene únicamente un único padre excepto el inicial
    def crearRuta(self, nodoInicial, nodoFinal):
        self.DijkstraPath = self._modelo.Diskstra(self.weightDictionary, nodoInicial)
        path = self.defineCamino(nodoInicial,nodoFinal)
        self.printOnTerminalRout(path)
        self.printOnCanvas(path)
    def defineCamino(self,nodoInicial,nodoFinal):
        if nodoFinal.getName() != nodoInicial.getName():
            return self.defineCamino(nodoInicial,nodoFinal.parent) + [nodoFinal]
        else:
            return [nodoFinal]
    def printOnTerminalRout(self,ruta):
        pos = self._vista.diccionarioPosiciones
        for nodo in ruta:
            posicion = pos.get(nodo.getName())
            if nodo.getName() != self.nodoRaiz.getName():
                parent = pos.get(nodo.parent.getName())
                print(parent[0] + " -> " + str(posicion[0]) + "; ",end = '')

    def printOnCanvas(self, ruta):
        for each in self.listaLineasDibujadas:
            self.canvas.delete(each)
        for each in self.listaOvalosSeleccionados:
            self.canvas.delete(each)
        for each in self.nodosDibujados:
            each.destroy()


        LineSet = []

        sumaMetros = 0
        for index in range(1,len(ruta)):
            actual = ruta[index]
            parent = actual.parent.getName()
            sumaMetros = self.weightDictionary.get((actual.getName(),parent))+sumaMetros
            actual = actual.getName()
            LineSet.append(self.Lmapeo.get((parent,actual)))
            #drawSpot
            #cada sublista en lineSet, es el conjunto de puntos de un punto a uno b
        print("\n")


        auxiliarList = []
        ptoB = None
        ptoA = None
        derechaA = None
        first = True
        while LineSet:
            if derechaA == None:
                ptoA = LineSet.pop(0)
                derechaA = self.isPoint(ptoA[len(ptoA)-1])
            else:
                ptoB = LineSet.pop(0)
                izquierdaB = self.isPoint(ptoB[0])
                if derechaA != izquierdaB:
                    ptoB.reverse()
                    izquierdaB = self.isPoint(ptoB[0])
                if derechaA != izquierdaB:
                    ptoB.reverse()
                    ptoA.reverse()
                    derechaA = self.isPoint(ptoA[len(ptoA)-1])
                    izquierdaB = self.isPoint(ptoB[0])
                if derechaA != izquierdaB:
                    ptoB.reverse()
                    izquierdaB = self.isPoint(ptoB[0])
                if derechaA == izquierdaB:
                    derechaA = self.isPoint(ptoB[len(ptoB)-1])
                    if first:
                        auxiliarList = auxiliarList + ptoA
                        first = False

                auxiliarList = auxiliarList + ptoB
        if first:
            auxiliarList = auxiliarList + ptoA

        #Dibuja las lineas de los lugares en la ruta
        for index in range(len(auxiliarList)-1):
            posA = auxiliarList[index]
            posB = auxiliarList[index + 1]
            posA = self._vista.getAbsPos(posA)
            posB = self._vista.getAbsPos(posB)
            self.listaLineasDibujadas.append(self.canvas.create_line(posA[0], posA[1], posB[0], posB[1],width=4,fill='green'))

        #Dibuja texto en el canvas
        salida =""
        for nodo in ruta:
            self.dibujaNodo(nodo)
            nombreLugar = self.diccionarioLugares.get(nodo.getName())
            salida = salida+" >> "+nombreLugar
        salida = salida + " : "+str(sumaMetros) +  "mts"
        self.canvas.itemconfig(self._vista.text,fill="RoyalBlue4",text=salida)

    def dibujaNodo(self,nodo):
        texto = self.diccionarioLugares.get(nodo.getName())
        pos = nodo.getPos()
        xRel = pos.getX()
        yRel = pos.getY()
        label = tkinter.Label(self.canvas, text=texto, font=("Helvetica", 13), fg="white")
        label.config(bg='orange')
        label.place(relx=xRel, rely=yRel, anchor="sw")
        self.nodosDibujados.append(label)








c = Controlador()
c.run()
