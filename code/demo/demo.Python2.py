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
