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
    hiddenAttributeContainerName = '.'
    exceptionMsgOldStyleClass = "New-style class should be used; derive it from the type 'object'"
# class DefinitionSet

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

    @classmethod # for instance attributes, to make them readonly
    def ConvertReadonlyAttributes(cls, instance):
        oldStyleClass = type(instance) != instance.__class__ # can happen with Python 2.*.* 
        if oldStyleClass:
            raise cls.OldStyleTypeException(instance, type(instance))
        def getAttrFromMetaclass(attr):
            return lambda cls: getattr(cls, DefinitionSet.hiddenAttributeContainerName)[attr]
        readonlyClass = type(instance)
        setattr(readonlyClass, DefinitionSet.hiddenAttributeContainerName, {})
        instanceAttributes = dir(instance)
        clone = list(instanceAttributes)
        for name in clone:
            value = getattr(instance, name)
            if not isinstance(value, cls.Attribute):
                continue
            delattr(instance, name)
            getattr(readonlyClass, DefinitionSet.hiddenAttributeContainerName)[name] = value.value
            aProperty = property(getAttrFromMetaclass(name))
            setattr(readonlyClass, name, aProperty)

    class OldStyleTypeException(TypeError):
        def __init__(self, anInstance, cls):
            TypeError.__init__(
                self,
                DefinitionSet.exceptionMsgOldStyleClass,
                dict(oldStyleClass=cls, instance=anInstance))

# class Readonly
