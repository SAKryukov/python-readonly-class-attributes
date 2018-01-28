Python Readonly Class Attributes: Complete Solution[](title)

Reliable solution does the trick: it does not depend on any naming conventions, works for both Python 2 and 3 and offers clear and concise usage syntax

<ul class="download">
    <li>Source code <a href="https://github.com/SAKryukov/python-readonly-class-attributes">on GitHub</a></li>
</ul>

## Contents[](notoc)

[](toc)

## Introduction

This solution is based on the brilliant ideas by [rIZenAShes](https://github.com/rIZenAShes) found [on GitHub](
https://gist.github.com/rIZenAShes/8469932).

As to the code, I found it, by far, not satisfactory. First, it is only compatible with Python 2, not 3. Worse, it is based on some naming conventions. The attributes to be exposed are marked by leading underscore, which is removed be the metaclass for exposed read-only properties. The present solution is compatible with both lines of Python versions and offers clear and concise syntax.

So, what's the big deal?

For class instances, the solution is simple enough: ready only properties:
<pre lang="Python">
class PropertySet:
    @property
    def readOnlyValue(self):
        return 13
    readWriteValue = 14

propertyDemo = PropertySet()
print (PropertySet.readOnlyInt)
print (propertyDemo.readOnlyValue)
propertyDemo.readOnlyValue = 100 # will throw exception</pre>

Note that in this example, `readWriteValue` is not an instance, but is a _class attribute_. In contrast to an _instance attribute_, it is not so easy to make it read-only.

## Why Class Attributes?

Class attributes have many uses, but I want to illustrate their importance on one simple use case: definition sets. Let's say we need to define some strings and integer constants. It's a good idea to put all of them in one place, to avoid using immediately defined [magic numbers](https://en.wikipedia.org/wiki/Magic_number_%28programming%29) or [magic string](https://en.wikipedia.org/wiki/Magic_string) anywhere else.

Let's, for a minute, forget about read-only properties and simply compare two options:

<pre lang="Python"># using class attributes:
class DefinitionSet:
    greetings = "Hello!"
    myNameFormat = "My name is {}."
    durationSeconds = 3.5
    color = { "opacity": 0.7, "wavelength": 400 }

#...
print (DefinitionSet.durationSeconds)</pre>
and
<pre lang="Python"># using instance attributes:
class DefinitionSet:
    def __init__(self):
        self.greetings = "Hello!"
        self.myNameFormat = "My name is {}."
        self.durationSeconds = 3.5
        self.color = { "opacity": 0.7, "wavelength": 400 }
definitionSet = DefinitionSet()

#...
print (definitionSet.durationSeconds)</pre> 

It is apparent that the option with class attribute is shorter and more convenient. Normally, the instance is needed only if we need more than one instance, but in this case even more boring part would be passing values as `__init__` arguments. For a single set of definitions it would be totally pointless.

The only real benefit of instantiation of the class is the ease of creation of read-only properties via the `@property` _decorator_. With class objects, it's pretty tricky. But let's fix it, so it will look even simpler than the use of `@property`.

## The Solution: Usage

First, let's see how it can be used:
<pre lang="Python">
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
    print ("Cannot set attribute Foo.test")</pre>

Here, the attribute `test` is just marked with the assignment to the expression of `Readonly.Attribute`; the desired constant value of any type is moved to an actual argument of the call. In fact, `Attribute` is the inner class of the class `Readonly`, so the whole call expression is the instantiation of this class.

In fact, `Readonly` base does not have to be used. It is shown in this code sample due to different syntax of Python 2 and Python 3. In fact, without any base classes, the class `Foo` could directly setup its _metaclass_, which should be the same class `Readonly`, only the syntax is different. For example,

<pre lang="Python">
# Python 2.*.*:
class ReadonlyBase(object, metaclass = Readonly):
    pass</pre>

<pre lang="Python">
# Python 3.*.*:    
class ReadonlyBase(object):
    __metaclass__ = Readonly</pre>

Here is the idea: the entire trick is performed by the metaclass: if the attribute is assigned to a `Readonly.Attribute` object, instantiation of the class object removes this attributes and creates matching read-only property exposed by another metaclass. It may sounds tricky, but... it is really pretty tricky. Let's see how it works.

## How it Works?

This is the entire solution:

<pre lang="Python">
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
        return type.__new__(NewMetaclass, classname, bases, classdict)</pre>

It is easy to show but harder to explain.

First of all, for all classes using `Readonly` as a metaclass, this metaclass is used only for the instantiation of a class object. At the moment of instantiation, the class object is created with a different metaclass named `NewMetaclass`, individual instance for each class instance. It is called "New" because it is ultimately used in the call `type.__new__(NewMetaclass, classname, bases, classdict)`.

Each instance of `NewMetaclass` is different. First of all, it is used as a container of all instances of the class `Readonly.Attribute` to be used by the class being initialized. Second of all, it is used as a container of some properties each named exactly as original class attribute to be re-worked into a read-only property.

When the original set of attributes of the class is traversed, the `Readonly.Attribute` instances are created and placed in the dictionary `NewMetaclass.attributeContainer`. For each such attribute, the property object is created using the constructor `property()`. For each distinct attribute name, such property is initialized with `lambda` expression generated based in the name, returning the value retrieved from `attributeContainer`.

During these manipulations, original class dictionary passed to `type._new_` if modified to remove original wanna-be-read-only class attributes. Before the traversal, the dictionary is cloned, otherwise we could face exception (in case of Python 3) caused by the attempt of modification of a dictionary being iterated.