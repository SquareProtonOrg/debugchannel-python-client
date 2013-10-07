from DebugChannel import DebugChannel
from unittest import TestCase
from model.Person import Person

class DebugChannelTest(TestCase):

    def setUp(self):
        self.d = DebugChannel('http://192.168.2.17', '1025', 'hello/world')


    def testLogStringDoesNotThrowException(self):
        self.d.log("hello")

    def testLogIntDoesNotThrowException(self):
        self.d.log(44)

    def testLogNullDoesNotThrowException(self):
        self.d.log(None)

    def testLogObjectDoesNotThrowException(self):
        peterGriffin = Person('Peter Griffin', 45)
        chrisGriffin = Person('Chris Griffin', 15, peterGriffin)
        self.d.log(chrisGriffin)

    def testLogRecursionDoesNotThrowException(self):
        class Node(object): pass
        n1, n2 = Node(), Node()
        n1.name, n2.name = "NODE 1", "NODE 2"
        n1.neighbour, n2.neighbour = n2, n1
        self.d.log(n1)

