from modelo import *
from vista import view
import tkinter

class Controlador:
    def __init__(self):
        self._master = tkinter.Tk()
        self._modelo = Graphs()
        self._vista = view(self._master)

        self.aux = None
        self.nodeList = self.cargaNodos()
        self.edgeList = []
        self.L = self.cargaConjuntoAristas()
        self.listaRelaciones = self.generaAdyacencia()
        print(self._modelo.printAdjacentList())

        self.canvas = self._vista.lienzo
     #   self.canvas.bind('<Double-Button-1>',self._EdgesScripts)
        self._vista.button.bind('<Button-1>',self.adyacencia)
    def run(self):
        self._master.title("Mapa Ciencias Exactas UADY")
        self._master.deiconify()
        self._master.mainloop()
    def dijkstra(self,event):
        #ahora sólo cosas para probar el programa
        pos = self._vista.getRelPos(event)
        point = self.isPoint(pos)
        if point != False:
            if self.aux == None:
                self.aux = point
            else:
                x1= point[1]
                y1 = point[2]
                x2 = self.aux[1]
                y2 = self.aux[2]
                pos1 = self._vista.getAbsPos((x1,y1))
                pos2 = self._vista.getAbsPos((x2,y2))
                self.canvas.create_line(pos1[0],pos1[1],pos2[0],pos2[1],fill='red')
                self.aux = None

      #  self.canvas.create_line()

    #Precondicion: recibe una tupla de posiciones: (xRel,yRel)
    #Returns una tupla de la lista de posiciones de la clase vista o Falso si no hay coincidencias
    def isPoint(self,position):
        for key,tupla in self._vista.diccionarioPosiciones.items():
            name = tupla[0]
            pos = tupla[1]
            if self.isCollision(pos,position):
                return (name,pos[0],pos[1])
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
            posicion = tupla[1]
            x = posicion[0]
            y = posicion[1]
            lista.append(Node(Position(x,y),name,.003))
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
                print(self.edgeList)
                self.edgeList.clear()
        else:
            self.edgeList.append(pos)
    def adyacencia(self,event):
        if self.cargarGrafo():
            pass


    def cargarGrafo(self):
        for node in self.nodeList:
            if not self._modelo.addNode(node):
                print("error")
                return False
            # for each in self.nodeList:
            #   print(each.getName()+" position: "+str(each.getPos().getX())+","+str(each.getPos().getY())+"radio: "+str(each.getRad()))
        return True
    def aristas(self,event):
        pass
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
    def generaAdyacencia(self):
        relacion = []
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








c = Controlador()
c.run()
