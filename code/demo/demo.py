''' 
Read-only class attributes

This is a comprehensive solution which does not
depend on any naming conventions

Readonly.Attribute instances assigned to attributes are converted to read-only properties 

(Read-only properties are easy on class instances, not so on class objects.)

Original publication:
https://www.codeproject.com/Articles/1227368/Python-Readonly-Class-Attributes
Code:
https://github.com/SAKryukov/python-readonly-class-attributes

Based on the ideas of rIZenAShes, https://github.com/rIZenAShes:
https://gist.github.com/rIZenAShes/8469932

Copyright (C) 2018 by Sergey A Kryukov

http://www.SAKryukov.org
https://github.com/SAKryukov
https://www.codeproject.com/Members/SAKryukov

'''

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
from library.readonly import Readonly

ReadonlyBase = Readonly(str(), (), {})
'''
The creation of class ReadonlyBase shown above unifies Python 2 and 3

Normally, equivalent version-dependent sample of syntax would be:

Python 2.*.*:
class ReadonlyBase(object):
    __metaclass__ = Readonly

Python 3.*.*:
class ReadonlyBase(object, metaclass = Readonly):
    pass

'''

class Foo(ReadonlyBase):
    bar = 100
    test = Readonly.Attribute(13)

print("Foo.bar: " + str(Foo.bar))
Foo.bar += 1
print("Modified Foo.bar: " + str(Foo.bar))
print("Foo.test: " + str(Foo.test))
try:
    Foo.test = Foo.test + 1 # will raise exception
except Exception:
    print ("Cannot set attribute Foo.test")
