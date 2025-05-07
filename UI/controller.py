import flet as ft
from networkx import all_neighbors, neighbors, connected_components, degree


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

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

    def popolaDDNodes(self, e):
        pass
    def handleRaggiungibili(self, e):
        pass