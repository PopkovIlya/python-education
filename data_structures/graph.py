from typing import Any

from hashtable import HashTable
from linked_list import ListNode, LinkedList


class Graph(object):

    def __init__(self, graph_dict: HashTable):
        """ initializes a graph object
            If no dictionary or None is given,
            an empty HashTable will be used
        """
        if graph_dict is None:
            graph_dict = HashTable()
        self._graph_dict = graph_dict

    def insert(self, vertex, edge) -> None:
        self._add_vertex(vertex)
        self._add_edge(edge)

    def lookup(self, value) -> Any:
        """
        Find vertex by value
        :return: the vertex
        """
        return value if value in self._graph_dict.keys() else None

    def delete(self, vertex):
        edges = self._edges(vertex)
        cur_node = edges.get_root()
        while cur_node is not None:
            self._delete_edge(cur_node.value)
            cur_node = cur_node.next
        self._graph_dict.delete(vertex)

    def _edges(self, vertex):
        """ returns a list of all the edges of a vertex"""
        return self._graph_dict.lookup(vertex)

    def _add_vertex(self, vertex):
        """ If the vertex "vertex" is not in
            self._graph_dict, a key "vertex" with an empty
            list as a value is added to the dictionary.
            Otherwise nothing has to be done.
        """
        if self._graph_dict.lookup(vertex) is None:
            self._graph_dict.insert(vertex, LinkedList())

    def _add_edge(self, edge):
        """ assumes that edge is of type set, tuple or list;
            between two vertices can be multiple edges!
        """
        edge = set(edge)
        vertex1, vertex2 = tuple(edge)
        for x, y in [(vertex1, vertex2), (vertex2, vertex1)]:
            if self._graph_dict.lookup(x) is not None:
                self._graph_dict.lookup(x).append(ListNode(y))
            else:
                dependencies = LinkedList()
                dependencies.append(ListNode(y))
                self._graph_dict.insert(x, dependencies)

    def _delete_edge(self, edge):
        """ assumes that edge is of type set, tuple or list;
            between two vertices can be multiple edges!
        """
        edge = set(edge)
        vertex1, vertex2 = tuple(edge)
        for x, y in [(vertex1, vertex2), (vertex2, vertex1)]:
            if self._graph_dict.lookup(x) is not None:
                self._graph_dict.lookup(x).delete(y)

    def __str__(self):
        res = "vertices: "
        for vertex in self._graph_dict.keys():
            res += str(vertex) + " "
        res += "\nedges: "
        for edge in self._graph_dict.values():
            res += str(edge) + "<->"
        return res
