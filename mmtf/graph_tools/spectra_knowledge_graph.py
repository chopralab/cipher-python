# Imports
import networkx as nx

class knowledge_graph:
    # Knowledge graph class for cipher
    def __init__(self, id=-1, name="default", dataset="default", sro_list=[], nx_graph=None):
        # Construct a knowledge graph with
        #   id: unique identifier for KG
        #   name: name for KG
        #   sro_list: optional predefine list of SRO (subject/relationship/object) tuples
        self.id = id
        self.name = name
        self.dataset = dataset
        self.sro_list = sro_list
        self.nx_graph = nx_graph

    # Add a SRO tuple to the KG
    def add_sro(self, sro_tup):
        self.sro_list.append(sro_tup)

    # Modify a SRO tuple in the KG
    def mod_sro(self, old_sro, new_sro):
        for idx, elem in self.sro_list:
            if elem is old_sro:
                self.sro_list[idx] = new_sro


class sro_tuple:
    