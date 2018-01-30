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

class DefinitionSet:
    attributeContainerName = "."

class Readonly(type):

    class Attribute(object):
        def __init__(self, value):
            self.value = value

    @classmethod
    def Base(cls): # base class with access control of class attribute
        return Readonly(str(), (), {})
    
    def __new__(metaclass, classname, bases, classdict):
        def getAttrFromMetaclass(attr):
            return lambda cls: getattr(type(cls), DefinitionSet.attributeContainerName)[attr]
        class NewMetaclass(metaclass):
            setattr(metaclass, DefinitionSet.attributeContainerName, {})
            def __call__(cls, *args, **kwargs):
                instance = type.__call__(cls, *args, **kwargs)
                setattr(cls, DefinitionSet.attributeContainerName, {})
                names = dir(instance)
                for name in names:
                    value = getattr(instance, name)
                    if not isinstance(value, metaclass.Attribute):
                        continue;
                    delattr(instance, name)
                    getattr(cls, DefinitionSet.attributeContainerName)[name] = value.value
                    aProperty = property(getAttrFromMetaclass(name))
                    setattr(cls, name, aProperty)
                return instance
        clone = dict(classdict)
        for name, value in clone.items():
            if not isinstance(value, metaclass.Attribute):
                continue;
            getattr(NewMetaclass, DefinitionSet.attributeContainerName)[name] = value.value
            aProperty = property(getAttrFromMetaclass(name))
            setattr(NewMetaclass, name, aProperty)
            classdict[name] = aProperty
            classdict.pop(name, None)               
        return type.__new__(NewMetaclass, classname, bases, classdict)
    # __new__

# class Readonly
