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

class DefinitionSet:
    attributeContainerName = "."

class Readonly(type):

    class Attribute(object):
        def __init__(self, value):
            self.value = value

    @classmethod
    def Base(cls): # base class with access control of class attribute
        return Readonly(str(), (), {})
    
    def __new__(metaclass, className, bases, classDictionary):
        def getAttrFromClass(attr):
            return lambda cls: getattr(type(cls), DefinitionSet.attributeContainerName)[attr]
        class NewMetaclass(metaclass):
            setattr(metaclass, DefinitionSet.attributeContainerName, {})
            def __call__(cls, *args, **kwargs):
                instance = type.__call__(cls, *args, **kwargs)
                newClass = metaclass(cls.__name__, cls.__bases__, {})
                newInstance = type.__call__(newClass)
                setattr(newClass, DefinitionSet.attributeContainerName, {})
                names = dir(instance)
                for name in names:
                    if hasattr(cls, name):
                        continue
                    value = getattr(instance, name)
                    if isinstance(value, metaclass.Attribute):
                        if hasattr(newInstance, name):
                            delattr(newInstance, name)
                        getattr(newClass, DefinitionSet.attributeContainerName)[name] = value.value
                        aProperty = property(getAttrFromClass(name))
                        setattr(newClass, name, aProperty)
                    else:
                        setattr(newInstance, name, getattr(instance, name))
                return newInstance
        clone = dict(classDictionary)
        for name, value in clone.items():
            if not isinstance(value, metaclass.Attribute):
                continue;
            getattr(NewMetaclass, DefinitionSet.attributeContainerName)[name] = value.value
            aProperty = property(getAttrFromClass(name))
            setattr(NewMetaclass, name, aProperty)
            classDictionary[name] = aProperty
            classDictionary.pop(name, None)               
        return type.__new__(NewMetaclass, className, bases, classDictionary)
    # __new__

# class Readonly
