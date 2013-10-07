__author__ = 'joseph'

class Parent(object): pass
class What(object): pass

class Person(Parent):

    MAX_AGE = 21
    MIN_AGE = 1

    def __init__(self, name, age, guardian=None):
        self.name, self.age, self.guardian = name, age, guardian


    def getName(self):
        return self.name