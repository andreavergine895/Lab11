import networkx as nx
from database.dao import DAO



class Model:
    def __init__(self):
        self.G = nx.Graph()
        self.rifugi= DAO.get_all_rifugi()

    def build_graph(self, year: int):
        """
        Costruisce il grafo (self.G) dei rifugi considerando solo le connessioni
        con campo `anno` <= year passato come argomento.
        Quindi il grafo avrà solo i nodi che appartengono almeno ad una connessione, non tutti quelli disponibili.
        :param year: anno limite fino al quale selezionare le connessioni da includere.
        """
        self.G.clear()
        connessioni= DAO.get_connessioni_fino_anno(year)
        for cnx in connessioni:
            r1= self.rifugi[cnx.id_rifugio1]
            r2= self.rifugi[cnx.id_rifugio2]
            # aggiungiamo nodi (in teoria networkx gestisce i doppioni)
            self.G.add_node(r1)
            self.G.add_node(r2)

            # aggiungiamo arco non pesato
            self.G.add_edge(r1, r2)

    def get_nodes(self):
        """
        Restituisce la lista dei rifugi presenti nel grafo.
        :return: lista dei rifugi presenti nel grafo.
        """
        return list(self.G.nodes())

    def get_num_neighbors(self, node):
        """
        Restituisce il grado (numero di vicini diretti) del nodo rifugio.
        :param node: un rifugio (cioè un nodo del grafo)
        :return: numero di vicini diretti del nodo indicato
        """
        return self.G.degree(node)

    def get_num_connected_components(self):
        """
        Restituisce il numero di componenti connesse del grafo.
        :return: numero di componenti connesse
        """
        return nx.number_connected_components(self.G)

    def get_reachable(self, start):
        """
        Deve eseguire almeno 2 delle 3 tecniche indicate nella traccia:
        * Metodi NetworkX: `dfs_tree()`, `bfs_tree()`
        * Algoritmo ricorsivo DFS
        * Algoritmo iterativo
        per ottenere l'elenco di rifugi raggiungibili da `start` e deve restituire uno degli elenchi calcolati.
        :param start: nodo di partenza, da non considerare nell'elenco da restituire.

        ESEMPIO
        a = self.get_reachable_bfs_tree(start)
        b = self.get_reachable_iterative(start)
        b = self.get_reachable_recursive(start)

        return a
        """
        a= self.get_reachable_bfs_tree(start)
        b=self.get_reachable_recursive(start)

        return b

    def get_reachable_bfs_tree(self, start):
        #La bfs_tree è un grafo radicato nel nodo 'start'.
        #Ritorna la lista dei nodi raggiungibili, escluso il nodo iniziale.
        bfs_tree= nx.bfs_tree(self.G, start)
        nodes= list(bfs_tree.nodes)
        nodes.remove(start)
        return nodes


    def get_reachable_recursive(self, start):
        visitati= set()
        self.DFS_ricorsione(start, visitati)

        visitati.discard(start) #dobbiamo escludere lo start per la consegna
        return list(visitati)


    def DFS_ricorsione(self, node, visitati):
        visitati.add(node)

        for nodo in self.G.neighbors(node):
            if nodo not in visitati:
                self.DFS_ricorsione(nodo, visitati)

