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

class Readonly(type):

    class Attribute(object):
        def __init__(self, value):
            self.value = value
    
    def __new__(metaclass, classname, bases, classdict):
        class NewMetaclass(metaclass):
            attributeContainer = {}
        def getAttrFromMetaclass(attr):
            return lambda cls: type(cls).attributeContainer[attr]
        clone = dict(classdict)
        for attr, value in clone.items():
            if isinstance(value, metaclass.Attribute):
                NewMetaclass.attributeContainer[attr] = value.value
                newAttrName = attr
                aProperty = property(getAttrFromMetaclass(attr))
                setattr(NewMetaclass, newAttrName, aProperty)
                classdict[newAttrName] = aProperty
                classdict.pop(attr, None)               
        return type.__new__(NewMetaclass, classname, bases, classdict)
    # __new__

# class Readonly
