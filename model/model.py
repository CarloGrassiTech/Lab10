import networkx as nx

from database.DAO import DAO


class Model:

    def __init__(self):
        self._grafo = nx.Graph()
        self._nodes = None
        self._edges = None
        self._idMap = {}
        self._year = 0

    def setYear(self, e):
        self._year = e
    def buildGraph(self):
        self._nodes =  DAO.getCountriesByYear(self._year)
        for i in self._nodes:
            self._idMap[i.CCode] = i
        self.createEdges(self._year)
        for v in self._edges: #edges sara una tubla con due codici di due paesi che rispecchiano le caratteristiche per essere degli archi
            self._grafo.add_edge(self._idMap[v[0]], self._idMap[v[1]])


    def createEdges(self, year):
        #devo ottenere con una query sul dao gli archi che hanno campo conntype=1 e che
        #rispettino l'anno corretto. restituendo come tupla con valore il codice due paesi confinanti in
        #che poi sfruttando la chiave dei nodi cioè i paesi ne recuperi i valori per mappare gli archi
        self._edges = DAO.getEdgesByYear(self._year)