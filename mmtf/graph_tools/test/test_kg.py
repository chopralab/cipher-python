import unittest
import sys
sys.path.insert(0, '../')
import knowledge_graph as kg
import os

#SRO Tuple Testing
class SRO_tuple_Test(unittest.TestCase):

    def test_sro_eq(self):
        tup1 = kg.sro_tuple("peak1","has m/z",112)
        tup2 = kg.sro_tuple("peak1","has m/z",112)
        tup3 = kg.sro_tuple("peak1","has m/z",200)
        tup4 = kg.sro_tuple("peak2","has m/z",112)
        tup5 = kg.sro_tuple("peak1","has intensity",112)

        self.assertEqual(tup1==tup2,True,"Should be True")
        self.assertEqual(tup1==tup3,False,"Should be False")
        self.assertEqual(tup1==tup4,False,"Should be False")
        self.assertEqual(tup1==tup5,False,"Should be False")

    def test_sro_ne(self):
        tup1 = kg.sro_tuple("peak1","has m/z",112)
        tup2 = kg.sro_tuple("peak1","has m/z",112)
        tup3 = kg.sro_tuple("peak1","has m/z",200)
        tup4 = kg.sro_tuple("peak2","has m/z",112)
        tup5 = kg.sro_tuple("peak1","has intensity",112)

        self.assertEqual(tup1!=tup2,False,"Should be False")
        self.assertEqual(tup1!=tup3,True,"Should be True")
        self.assertEqual(tup1!=tup4,True,"Should be True")
        self.assertEqual(tup1!=tup5,True,"Should be True")

    def test_sro_getitem(self):
        tup = kg.sro_tuple("peak1","has m/z",112)
        
        self.assertEqual(tup[0],"peak1","Should be peak1")
        self.assertEqual(tup[1],"has m/z","Should be has m/z")
        self.assertEqual(tup[2],112,"Should be 112")

    def test_sro_mod_sub(self):
        tup = kg.sro_tuple("peak1","has m/z",112)
        tup.mod_sub("peak2")

        self.assertEqual(tup[0],"peak2","Should be peak2")
        self.assertEqual(tup[1],"has m/z","Should be has m/z")
        self.assertEqual(tup[2],112,"Should be 112")

    def test_sro_mod_rel(self):
        tup = kg.sro_tuple("peak1","has m/z",112)
        tup.mod_rel("has intensity")

        self.assertEqual(tup[0],"peak1","Should be peak1")
        self.assertEqual(tup[1],"has intensity","Should be has intensity")
        self.assertEqual(tup[2],112,"Should be 112")

    def test_sro_mod_obj(self):
        tup = kg.sro_tuple("peak1","has m/z",112)
        tup.mod_obj(200)

        self.assertEqual(tup[0],"peak1","Should be peak1")
        self.assertEqual(tup[1],"has m/z","Should be has m/z")
        self.assertEqual(tup[2],200,"Should be 200")

#RO Tuple Testing
class RO_tuple_test(unittest.TestCase):

    def test_ro_init(self):
        pass

    def test_ro_eq(self):
        pass

    def test_ro_ne(self):
        pass

    def test_ro_getitem(self):
        pass

    def test_ro_mod_rel(self):
        pass

    def test_ro_mod_obj(self):
        pass

# Knowledge Graph Testing
class KG_test(unittest.TestCase):

    def test_kg_init(self):
        pass

    def test_kg_add_sro(self):
        pass

    def test_kg_del_sro(self):
        pass

    def test_mod_sro_list(self):
        pass

    def test_mod_adj_list(self):
        pass

if __name__ == '__main__':
    unittest.main()