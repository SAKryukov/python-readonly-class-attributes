''' 
Read-only class and instance attributes

This is a comprehensive solution which does not depend on any naming conventions

Readonly.Attribute instances assigned to attributes are converted to read-only properties 
(Read-only properties are easily created on class instances, not so on class objects.)

Original publication:
https://www.codeproject.com/Articles/1227368/Python-Readonly-Class-Attributes
Code:
https://github.com/SAKryukov/python-readonly-class-attributes

Partially based on the ideas of rIZenAShes, https://github.com/rIZenAShes:
https://gist.github.com/rIZenAShes/8469932

Copyright (C) 2018 by Sergey A Kryukov

http://www.SAKryukov.org
https://github.com/SAKryukov
https://www.codeproject.com/Members/SAKryukov

'''

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
from library.readonly import Readonly

ReadonlyBase = Readonly.Base()
'''
The creation of class ReadonlyBase shown above unifies Python 2 and 3

Normally, equivalent version-dependent syntax would be:

Python 2.*.*:
class ReadonlyBase(object):
    __metaclass__ = Readonly

Python 3.*.*:
class ReadonlyBase(object, metaclass = Readonly):
    pass

'''

class Foo(ReadonlyBase): # or make Readonly a metaclass of Foo, see above
    bar = 100
    test = Readonly.Attribute(13)
    def __init__(self, a, b):
        self.a = a
        self.b = Readonly.Attribute(b)

print("Class attributes:")
print(str())

print("Class attribute Foo.bar: " + str(Foo.bar))
Foo.bar += 1
print("Modified class attribute Foo.bar: " + str(Foo.bar))
print("Class attribute Foo.test: " + str(Foo.test))
try:
    Foo.test += 1 # will raise exception
except Exception:
    print ("Cannot set class attribute Foo.test")

print(str())
print("Instance attributes:")
print(str())

instance1 = Foo(300, 3.14159)
print("Instance attribute a: " + str(instance1.a))
instance1.a += 1
print("Modified instance attribute a: " + str(instance1.a))
print("Instance attribute b: " + str(instance1.b))
try:
    instance1.b += 1 # will raise exception
except Exception:
    print ("Cannot set instance attribute b")

print("Another instance:")

instance2 = Foo(400, 2.71828)
print("Instance attribute a: " + str(instance2.a))
instance2.a += 1
print("Modified instance attribute a: " + str(instance2.a))
print("Instance attribute b: " + str(instance2.b))
try:
    instance2.b += 1 # will raise exception
except Exception:
    print ("Cannot set instance attribute b")
