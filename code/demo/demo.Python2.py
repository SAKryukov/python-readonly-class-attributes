''' 
Read-only class attributes

This is a comprehensive solution which does not
depend on any naming conventions

(Read-only properties are easy on class instances, not so on class objects.)

https://github.com/SAKryukov/python-readonly-class-attributes

Based on the ideas of rIZenAShes, https://github.com/rIZenAShes:
https://gist.github.com/rIZenAShes/8469932

Copyright (C) 2012 by Sergey A Kryukov

http://www.SAKryukov.org
https://github.com/SAKryukov
https://www.codeproject.com/Members/SAKryukov

'''

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
from library.readonly import Readonly

class ReadonlyBase(object):
    __metaclass__ = Readonly

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
