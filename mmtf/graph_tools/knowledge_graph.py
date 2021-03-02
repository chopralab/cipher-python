# Imports
import networkx as nx
import pandas as pd
import pickle
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Custom Errors and Exceptions
class Error(Exception):
    pass

class InvalidSROTupleError(Error):
    pass

class InvalidROTupleError(Error):
    pass

class InvalidKGError(Error):
    pass

# Knowledge Graph Class
class knowledge_graph:
    # Knowledge graph class for CIPHER
    # TODO change the way we read in the graph
    def __init__(self, obj_id=-1, name="default", dataset="default", data=None):
        # Construct a knowledge graph with
        #   id: unique identifier for KG
        #   name: name for KG
        #   dataset: dataset the graph relates to
        #   sro_list: optional predefine list of SRO (subject/relationship/object) tuples
        if not isinstance(obj_id, int):
            raise InvalidKGError
        if not isinstance(name, str):
            raise InvalidKGError
        if not isinstance(dataset, str):
            raise InvalidKGError

        self.id = obj_id
        self.name = name
        self.dataset = dataset

        if data is None:
            self.sro_list = []
            self.nx_graph = nx.DiGraph()
            self.adj_list = {}
        elif isinstance(data, list):
            for sro in data:
                if not isinstance(sro, type(sro_tuple)):
                    raise InvalidKGError
            
            self.sro_list = data
            self.gen_adj_list_fro_sro()
            self.gen_nx_graph_from_sro()

    # Overide the representation
    def __repr__(self):
        return "ID: " + str(self.id) + ", Name: " + self.name

    # Overide the str operator
    def __str__(self):
        return_string = ""
        for elem in self.sro_list:
            return_string += str(elem) + "\n"
        return return_string

    # Add a SRO tuple to the KG
    def add_sro(self, sro_tup):
        if not isinstance(sro_tup, type(sro_tuple)):
            raise InvalidKGError

        self.sro_list.append(sro_tup)

        self.nx_graph.add_node(sro_tup[0])
        self.nx_graph.add_node(sro_tup[2])
        self.nx_graph.add_edge(sro_tup[0],sro_tup[2],rel=sro_tup[1])

        if sro_tup[0] not in self.adj_list:
            self.adj_list[sro_tup[0]] = [ro_tuple(sro_tup[1],sro_tup[2])]
        else:
            self.adj_list[sro_tup[0]].append(ro_tuple(sro_tup[1],sro_tup[2]))

    # Delete a SRO tuple in the KG
    def del_sro(self, del_tup):
        if not isinstance(del_tup, type(sro_tuple)):
            raise InvalidKGError

        self.sro_list.remove(del_tup)

        self.nx_graph.remove_edge(del_tup[0], del_tup[2])
        if self.nx_graph.degree[del_tup[0]] is 0:
            self.nx_graph.remove_node(del_tup[0])
        if self.nx_graph.degree[del_tup[2]] is 0:
            self.nx_graph.remove_node(del_tup[2])

        if self.adj_list.get(del_tup[0],-1) is not -1:
            self.adj_list[del_tup[0]].remove(ro_tuple(del_tup[1],del_tup[2]))
                
    # Modify the SRO list
    def mod_sro_list(self, sro_list):
        if not isinstance(sro_list, list):
            raise InvalidKGError
        
        for sro in sro_list:
            if not isinstance(sro, type(sro_tuple)):
                raise InvalidKGError
        
        self.sro_list = sro_list
        self.__gen_nx_graph_from_sro()
        self.__gen_adj_list_fro_sro()

    # Modify the adjacency list
    def mod_adj_list(self, adj_list):
        if not isinstance(adj_list, dict):
            raise InvalidKGError

        for key, value in adj_list:
            if not isinstance(key, str):
                raise InvalidKGError

            if not isinstance(value, list):
                raise InvalidKGError

            for i in range(len(value)):
                if not isinstance(value[i], (type(ro_tuple), tuple)):
                    raise InvalidKGError

                if isinstance(value[i], tuple):
                    if len(value[i]) is not 2:
                        raise InvalidROTupleError
                    value[i] = ro_tuple(value[i][0], value[i],[1])

        
        self.adj_list = adj_list
        self.__gen_sro_list_from_adj_list
        self.__gen_nx_graph_from_sro

    # Modify the NetworkX graph
    # TODO this is an optional implementation
    def mod_nx_graph(self, nx_graph):
        pass

    # Generate a NetworkX graph from our SRO list
    def __gen_nx_graph_from_sro(self):
        G = nx.DiGraph()
        for elem in sro_list:
            G.add_node(elem[0])
            G.add_node(elem[2])
            G.add_edge(elem[0],elem[2],rel=elem[1])
        self.nx_graph = G

    # Generate the adjacency matrix from our SRO list
    def __gen_adj_list_fro_sro(self):
        adj_list = {}
        for elem in self.sro_list:
            if elem[0] not in adj_list:
                adj_list[elem[0]] = [ro_tuple(elem[1],elem[2])]
            else:
                adj_list[elem[0]].append(ro_tuple(elem[1],elem[2]))
        self.adj_list = adj_list

    # Generate the SRO list from a networkx graph
    def __gen_sro_list_from_graph(self):
        sro_list = []
        for edge in self.nx_graph.edges:
            sub = edge[0]
            obj = edge[1]
            rel = self.nx_graph[sub][obj]['rel']
            sro_list.append(sro_tuple(sub,obj,rel))
        self.sro_list = sro_list

    # Generate the SRO list from an adjacency list
    def __gen_sro_list_from_adj_list(self):
        sro_list = []
        for s,ro_list in adj_list:
            for ro in ro_list:
                sro_list.append(sro_tuple(s,ro[0],ro[1]))
        self.sro_list = sro_list

    # Write out the graph to a file
    def graph_from_p(self,fname):
        self.nx_graph = pickle.load(open(fname))
        self.sro_list_from_graph()

    # Read in the graph from a file
    def graph_to_p(self,fname="graph_out.p"):
        if isinstance(self.nx_graph, type(nx.DiGraph())):
            pickle.dump(self.nx_graph, open(fname,'w'))
    
    # Draw the graph to a PNG file
    def graph_to_image(self,fname="graph_out.png"):
        plt.subplot(111)
        nx.draw(self.nx_graph, with_labels=True, font_weight="bold")
        plt.save_fig(fname)

    # Get all of the subjects O(1)
    def get_all_subjects(self):
        return self.adj_list.keys
    
    # Get all of the relationships O(n) (will improve later)
    def get_all_relationships(self):
        rel = []
        for elem in self.sro_list:
            if elem[1] not in rel:
                rel.append(elem[1])
        return rel

    # Get all of the objects O(n) (will improve later)
    def get_all_objects(self):
        obj = []
        for elem in self.sro_list:
            if elem[2] not in obj:
                obj.append(elem[2])
        return obj

    @staticmethod
    def get_one_hot(kg_list):
        if not isinstance(kg_list, list):
            raise InvalidKGError

        for elem in kg_list:
            if not isinstance(elem, type(knowledge_graph)):
                raise InvalidKGError
        
        # TODO finish this

# Subject/Relationship/Object tuple class for use with Knowledge Graphs
class sro_tuple:
    # Subject/Relationship/Object class for CIPHER
    def __init__(self, sub, rel, obj):
        # Construct a SRO tuple
        #   subject: the subject of the tuple (constrained to str)
        #   relationship: the relationship of the tuple (constrained to str)
        #   object: the object of the tuple (constrained str or numeric)
        if not isinstance(sub, str):
            raise InvalidSROTupleError
        if not isinstance(rel, str):
            raise InvalidSROTupleError
        if not isinstance(obj, (str, int, float)):
            raise InvalidSROTupleError

        self.tup = (sub,rel,obj)
        self.sub = sub
        self.rel = rel
        self.obj = obj

    # Overide the representation
    def __repr__(self):
        return str(self.tup)

    # Overide the str method
    def __str__(self):
        return str(self.sub) + " " + str(self.rel) + " " + str(self.obj)

    # Overide getitem method for accessing the object with an index
    def __getitem__(self, index):
        # Raise exception if we provide more than one index
        if isinstance(index,tuple):
            raise InvalidSROTupleError
        
        # Get the value dependent on conditions
        if index is "subject" or index is "sub":
            return self.sub
        elif index is "relationship" or index is "rel":
            return self.rel
        elif index is "object" or index is "obj":
            return self.obj
        else:
            return self.tup[index]

    # Override the equal operator
    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        elif (self.tup[0] == other.tup[0]) and (self.tup[1] == other.tup[1]) and (self.tup[2] == other.tup[2]):
            return True
        else:
            return False

    # Override the not equal operator
    def __ne__(self, other):
        if not isinstance(other, type(self)):
            return True
        elif (self.tup[0] == other.tup[0]) and (self.tup[1] == other.tup[1]) and (self.tup[2] == other.tup[2]):
            return False
        else:
            return True
    
    # Modify the subject
    def mod_sub(self, sub):
        if not isinstance(sub, str):
            raise InvalidSROTupleError
        self.tup[0] = sub
        self.sub = sub
    
    # Modify the relationship
    def mod_rel(self, rel):
        if not isinstance(rel, str):
            raise InvalidSROTupleError
        self.tup[1] = rel
        self.rel = rel
    
    # Modify the object
    def mod_obj(self, obj):
        if not isinstance(obj, (str, int, float)):
            raise InvalidSROTupleError
        self.tup[2] = obj
        self.obj = obj

# Ojbect/Relationship tuple class for use with Knowwledge Graphs
class ro_tuple:
     # Relationship/Object class for CIPHER
    def __init__(self, rel, obj):
        # Construct a SRO tuple
        #   relationship: the relationship of the tuple (constrained to str)
        #   object: the object of the tuple (constrained str or numeric)
        if not isinstance(rel, str):
            raise InvalidROTupleError
        if not isinstance(obj, (str, int, float)):
            raise InvalidROTupleError

        self.tup = (rel,obj)
        self.rel = rel
        self.obj = obj

    # Overide the repersentation
    def __repr__(self):
        return str(self.tup)

    # Overide the str method
    def __str__(self):
        return str(self.rel) + " " + str(self.obj)

    # Overide getitem method for accessing the object with an index
    def __getitem__(self, index):
        # Raise exception if we provide more than one index
        if isinstance(index,tuple):
            raise InvalidROTupleError
        
        if index is "relationship" or index is "rel":
            return self.rel
        elif index is "object" or index is "obj":
            return self.obj
        else:
            return self.tup[index]

    # Override the equal operator
    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        elif (self.tup[0] == other.tup[0]) and (self.tup[1] == other.tup[1]):
            return True
        else:
            return False

    # Override the not equal operator
    def __ne__(self, other):
        if not isinstance(other, type(self)):
            return True
        elif (self.tup[0] == other.tup[0]) and (self.tup[1] == other.tup[1]):
            return False
        else:
            return True
    
    # Modify the relationship
    def mod_rel(self, rel):
        if not isinstance(rel, str):
            raise InvalidROTupleError
        self.tup[0] = rel
        self.rel = rel
    
    # Modify the object
    def mod_obj(self, obj):
        if not isinstance(obj, (str, int, float)):
            raise InvalidROTupleError
        self.tup[1] = obj
        self.obj = obj