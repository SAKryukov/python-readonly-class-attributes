''' 
Read-only class attributes

This is a comprehensive solution which does not
depend on any naming conventions

(Read-only properties are easy on class instances, not so on class objects.)

Original publication:
https://www.codeproject.com/Articles/1227368/Python-Readonly-Class-Attributes
Code:
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
                aProperty = property(getAttrFromMetaclass(attr))
                setattr(NewMetaclass, attr, aProperty)
                classdict[attr] = aProperty
                classdict.pop(attr, None)               
        return type.__new__(NewMetaclass, classname, bases, classdict)
    # __new__

    @staticmethod
    def ConvertReadonlyAttributes(cls, instance):
        def getAttrFromMetaclass(attr):
            return lambda cls: getattr(cls, ".")[attr]
        readonlyClass = type(instance)
        setattr(readonlyClass, ".", {})
        instanceAttributes = dir(instance)
        clone = list(instanceAttributes)
        for name in clone:
            value = getattr(instance, name)
            if not isinstance(value, cls.Attribute):
                continue
            delattr(instance, name)
            getattr(readonlyClass, ".")[name] = value.value
            aProperty = property(getAttrFromMetaclass(name))
            setattr(readonlyClass, name, aProperty)

# class Readonly
