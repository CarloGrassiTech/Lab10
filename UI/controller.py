import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleCalcola(self, e):
        if self._view._txtAnno.value >2016 or self._view._txtAnno.value <1816:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("l'anno non rientra tra l'intervallo "
                                                           "1816-2016", color= "red "))
            self._view.update_page()
        self._model.buildGraph()
        if len(self._model._grafo.nodes())>0:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text(f"Il grafo è stato creato correttamente \n"
                                                           f"è formato da {len(self._model._nodes)} nodi e {len(self._model._edges)} archi \n"))
            self._view.update_page()
        else:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("il grafo non è stato correttamente", color = "red"))
            self._view.update_page()
