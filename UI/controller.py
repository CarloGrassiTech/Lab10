import flet as ft
import networkx as nx
from networkx import all_neighbors, neighbors, connected_components, degree
from networkx.algorithms.traversal import bfs_successors
from networkx.classes import nodes


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._subgraph = nx.Graph()
        self._res = []

    def handleCalcola(self, e):
        if int(self._view._txtAnno.value) > 2016 or int(self._view._txtAnno.value) < 1816:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("l'anno non rientra tra l'intervallo "
                                                           "1816-2016", color= "red"))
            self._view.update_page()
            return
        self._model.setYear(int(self._view._txtAnno.value))
        self._model.buildGraph()
        res=[]
        for i in self._model._nodes:
            self._view._ddNodes.options.append(ft.dropdown.Option(str(i)))
            self._model._mapDD[str(i)] = i
        self._view._ddNodes.disabled = False
        self._view._statiRaggiungibili.disabled = False

        if len(self._model._grafo.nodes())>0:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text(f"Il grafo è stato creato correttamente \n"
                                                           f"è formato da {len(self._model._nodes)} nodi e {len(self._model._edges)} archi \n"))
            #stampare i paesi presenti nel grafo e il rispettivo grado del nodo(numero di confini)
            self._view._txt_result.controls.append(ft.Text(f"Il grafo contiene i seguenti paesi con il rispettivo numero di confini:"))

            for v in self._model._grafo.nodes:
                self._view._txt_result.controls.append(ft.Text(f"{v} di grado: {degree(self._model._grafo, v)}"))
            #devo ora aggiungere il numero delle parti connesse
            count = 0
            for c in connected_components(self._model._grafo):
                count +=1
            self._view._txt_result.controls.append(ft.Text(f"Il numero delle parti connesse è : {count}"))
            self._view.update_page()
        else:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("il grafo non è stato correttamente creato", color = "red"))
            self._view.update_page()

    def handleRaggiungibili(self, e):
        if self._view._ddNodes.value is None:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("selezionare un paese", color="red"))
            self._view.update_page()
            return

        if degree(self._model._grafo, self._model._mapDD[self._view._ddNodes.value]) > 1:
            self._view._txt_result.controls.clear()
            nodi_raggiungibili = []

            source = self._model._mapDD[self._view._ddNodes.value]
            #trovare la componenete connessa del nodo del DD
            for c in connected_components(self._model._grafo):
                if source in c:
                    self._subgraph = self._model._grafo.subgraph(c).copy()
                    break

            #come calcolo i nodi raggiungibili
            #nodi_raggiungibili = self.getNodiRaggiungibiliNX(self._model._mapDD[self._view._ddNodes.value])
            self.getNodiRaggiungibiliRicorsione(nodes(self._model._grafo), self._model._mapDD[self._view._ddNodes.value])
            nodi_raggiungibili = self._res.copy()
            #nodi_raggiungibili = self.getNodiRaggiungibiliIterazione(self._model._mapDD[self._view._ddNodes.value])


            self._view._txt_result.controls.append(ft.Text("il nodo ha i seguenti nodi raggiungibili:"))
            for v in nodi_raggiungibili:
                self._view._txt_result.controls.append(ft.Text(f"{str(v)}"))
            self._view.update_page()
        else:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("il nodo non ha paesi raggiungibili", color="red"))
            self._view.update_page()

    def getNodiRaggiungibiliNX(self, source):
        #for i in self._model._subgraph.nodes:
        res = []
        for i in bfs_successors(self._subgraph, source):
            res.append(i)
        return res

    def getNodiRaggiungibiliRicorsione(self, nodi_rim, parziale):
        #ricorsione provando ogni volta ad aggiungere un nodo dei rimanenti che sia collegabile all'ultimo nodo in parziale
        if len(nodi_rim) == 0:
            self._res.extend(parziale)
            return
        else:
            for v in nodi_rim:
                if v in neighbors(self._model._grafo, parziale[-1]):
                    parziale.append(v)
                    self.getNodiRaggiungibiliRicorsione( nodi_rim, parziale)
            parziale.pop()


    def getNodiRaggiungibiliIterazione(self, source):
        #for n in range(len(self._model._subgraph.nodes)):
        pass
