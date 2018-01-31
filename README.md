# Python Readonly Class Attributes: Complete Solution

[Original publication](https://www.codeproject.com/Articles/1227368/Python-Readonly-Class-Attributes)

## Basic usage:

```
class Foo(ReadonlyBase):
    bar = 100
    test = Readonly.Attribute(13)
    def __init__(self, a, b):
        self.a = a
        self.b = Readonly.Attribute(b)
```

Partially based on the ideas by [rIZenAShes](https://github.com/rIZenAShes) found [on GitHub](https://gist.github.com/rIZenAShes/8469932)