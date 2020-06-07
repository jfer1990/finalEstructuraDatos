from math import inf
from _collections import deque
from heapq import * #AUNQUE NO ESTÁN IMPLEMENTADOS, PUEDEN USARSE Y EL PROGRAMA SERÍA MÁS EFICIENTE POR LA ARITMÉTICA DE BINARIOS.

class Vertex:
    def __init__(self):
        self.color = None
        self.distance = None
        self.parent = None
    def setDistance(self,d):
        self.distance = d
    def setParent(self,p):
        self.parent = p


#RECIBE TODO EN POSICION RELATIVA
class Node(Vertex):
    def __init__(self,pos,name,rad):
        super().__init__()
        self._pos = pos
        self._name = name
        self._rad = rad

    def getPos(self):
        return self._pos
    def getRad(self):
        return self._rad
    def getName(self):
        return self._name
    def setPos(self, pos):
        self._pos = pos
    def __lt__(self, other):
        return self.distance < other.distance



class Position:
    def __init__(self,x,y):
        self._x = x
        self._y = y
    def getX(self):
        return self._x
    def getY(self):
        return self._y


class Graphs:
    def __init__(self):
        #adjList es un diccionario que tiene como llave el nombre del nodo
        self.nodeList = []
        self.adjList = {}
        self._numOfNodes = 0


    def isNewNode(self,node):
        h,k = (node.getPos().getX()),(node.getPos().getY())
        for each in self.nodeList:
            x1 = float(each.getPos().getX())
            y1 = float(each.getPos().getY())
            distAB = ((x1 - h) ** 2 + (y1 - k) ** 2) ** (1 / 2)
            if distAB <= 2*node.getRad():
                return each
        return True

    def getAdjacentList(self):
        return self.adjList


    #Return True if node was added succesfully, otherwise returns False
    def addNode(self,node):
        x = True if self.isNewNode(node) == True else False
        if x:
            self.nodeList.append(node)
            return True
        else:
            return self.isNewNode(node)
    #Precondición: node1 and node2 must be instantiated, returns False when node1 and node2 doesnt already existed
    #def createEdge(self,node1, node2):
     #   pos = -1
      #  for each in self.nodeList:
       #     pos += 1
        #    if each == node1:
         #       self.adjList[pos] = self.adjList[pos] + [node2]
          #      return True
        #return False
    def createEdge(self,node1,node2):
        if node1 == None:
            return False
            #self.adjList.update({node2.getName():[]})
        elif node2== None:
            return False
           # self.adjList.update({node1.getName():[]})
        #Obligación que nodo 1 y nodo2 existan.
        else:
            k1 = node1.getName()
            k2 = node2.getName()
            if self.adjList.get(k1) != None:
                aux = self.adjList.get(k1) + [node2]
                self.adjList.update({k1:aux})
            else:
                self.adjList.update({k1:[node2]})

            if self.adjList.get(k2) != None:
                aux = self.adjList.get(k2) + [node1]
                self.adjList.update({k2:aux})
            else:
                self.adjList.update({k2:[node1]})


    def printAdjacentList(self):
        c = 0
        file = ""
        for key,list in self.adjList.items():
            output = key+"  ->"
            for elem in list:
                output = output +" - "+ elem.getName()
            output = output + "\n"
            file = file+output
            c += 1
        return file
    def nodeName(self):
        val = "v"+str(self._numOfNodes)
        self._numOfNodes += 1
        return val
    def getNumNode(self,node):
        return node.getName()[len(node.getName())-1]
    def BFS_Tree(self):
        vertexList = []
        edgesList = []
        for v in self.nodeList[1:]:
            v.distance = inf
            v.parent = None
            v.color = "white"
            vertexList.append(v)
        s = self.nodeList[0]
        s.parent = None
        s.color = "gray"
        s.distance = 0
        Q = deque()
        Q.append(s) #instead of enqueue
        while(Q.__len__()>0):
            u = Q.popleft() #instead of dequeue
            adjNodesVector = self.adjList.get(u.getName())
            for v in adjNodesVector:
                if v.color.casefold() == "white".casefold():
                    edgesList.append((u,v))
                    v.color = "gray"
                    v.distance = u.distance + 1
                    v.parent = u
                    Q.append(v)
            u.color = "black"

        for u,v in edgesList:
            print(u.getName()+"~"+v.getName())
        return edgesList
    def Diskstra(self,w,s):
        pila = []
        alpha = None
        Q = self.nodeList.copy()
        self.Initialize(s)
        S = []
        while len(Q) > 0:
            u = self.minimumDistance(Q)
            u.color = "black"
            S.append(u)
            neighbors = self.adjList.get(u.getName())
            for neighbor in neighbors:
                self.Relax(u,neighbor,w)
            #self._updateQadjaceny(u)
            #heapify(Q)

       # for element in S:
        #    print(element.getName()+" - "+str(element.distance))
        return S

    def Initialize(self,s):
        for v in self.nodeList:
            v.distance = inf
            v.parent = None
            v.color = "white"
        s.distance = 0



    #w is a dictionary which key is a tuple of nodeNames
    def Relax(self,u,v,w):
        val = w.get((u.getName(),v.getName()))
        if v.distance > u.distance + val and v.color=="white":
            v.setDistance(u.distance+val)
            v.setParent(u)


    def _updateQadjaceny(self,u):
        lista = self.adjList.get(u.getName())
        for item in lista:
            actualList = self.adjList.get(item.getName())
            for i in actualList:
                if i.getName() == u.getName():
                    actualList.remove(i)
                    break
        self.adjList.pop(u.getName())

    #Quita la distancia más pequeña en el conjunto de vértices  y elimina el nodo

    def minimumDistance(self,Q):
        # Initilaize minimum distance for next node
        min = inf
        minVertex = None

        # Search not nearest vertex not in the
        # shortest path tree
        for v in Q:
            if v.distance < min and v.color == "white":
                min = v.distance
                minVertex = v
        Q.remove(minVertex)


        return minVertex

