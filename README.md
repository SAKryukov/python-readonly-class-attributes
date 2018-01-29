## Python Readonly Class Attributes: Complete Solution

[Original publication](https://www.codeproject.com/Articles/1227368/Python-Readonly-Class-Attributes)

Usage:
```
class Foo(ReadonlyBase):
    bar = 100
    test = Readonly.Attribute(13)
    anotherAttribute = "can modify"
    ro = Readonly.Attribute("read-only")
```

