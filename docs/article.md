Python Readonly Attributes: Complete Solution[](title)

Reliable solution does the trick: it does not depend on any naming conventions, works for both Python 2 and 3 and offers clear and concise usage syntax

<ul class="download">
    <li><a href="https://github.com/SAKryukov/python-readonly-class-attributes">Download source code from GitHub</a></li>
</ul>

## Contents[](notoc)

[](toc)

## Introduction

This solution is based on the small code sample by [rIZenAShes](https://github.com/rIZenAShes) found [on GitHub](
https://gist.github.com/rIZenAShes/8469932), which demonstrates quite interesting ideas.

As to the code, I found it, by far, not satisfactory. First, it is only compatible with Python 2, not 3. Worse, it is based on some naming conventions. The attributes to be exposed are marked by leading underscore, which is removed be the metaclass for exposed read-only properties. The present solution is compatible with both lines of Python versions and offers clear and concise syntax.

So, what's the big deal?

Implementing read-only attributes is fairly easy:
<pre lang="Python">
class Meta(type):
    @property
    def RO(self):
        return 13

class DefinitionSet(Meta(str(), (), {})):
    greetings = "Hello!"
    myNameFormat = "My name is {}."
    durationSeconds = 3.5
    color = { "opacity": 0.7, "wavelength": 400 }
    @property
    def RO(self):
        return 14
    def __init__(self):
        self.greetings = "Hello again!"
        self.myNameFormat = "Let me introduce myself. My name is {}."
        self.durationSeconds = 3.6
        self.color = { "opacity": 0.8, "wavelength": 410 }

instance = DefinitionSet()
# instance.RO and DefinitionSet.RO are two different
# read-only attributes</pre>

In this code sample, `instance.RO` behaves as an _instance attribute_ and `DefinitionSet.RO` — as a _class attribute_; they are introduced as `read-only properties`.

Note certain inconvenience in development: while in usage such property is used as a peer of some "regular" attributes (for example, `instance.RO` vs. `instance.color`), it is set up on an upper level, the level of the _object type_. For `instance`, this is instance type, `type(instance) == DefinitionSet`; for `DefinitionSet`, this is its _metaclass_, `type(DefinitionSet) == Meta`. (Not so obvious way of setting up a metaclass for `DefinitionSet`, through _inheritance_ is shown; this is done for the sole purpose of showing equivalent code for Python 2 and 3, [see below](#heading.unification-of-python-2-and-3-in-the-demo).)

Definition of read-only class properties looks a bit more complicated than in case of instance properties: with instances, the description at least can be placed in _almost_ one place (compare `DefinitionSet.RO` and `self.greetings` in `__init__`). For a class attribute, the property definition should be placed in a separate class (`Meta` in our sample).

Now, the problem is alleviated with the small device, `@property` _decorator_, which can be considered as kind of [syntactic sugar](https://en.wikipedia.org/wiki/Syntactic_sugar). If we wanted to start _[ab ovo](https://en.wikipedia.org/wiki/Ab_ovo)_, we would show mode fundamental use of _descriptors_, based on `__get__`, as it is described in documentation for [Python 2](https://docs.python.org/2/howto/descriptor.html) and [Python 3](https://docs.python.org/3/howto/descriptor.html).

So, can we create syntactic sugar sweeter than that, shorter, more clear and concise? Would it make any practical sense?

The answer depends on our usage of _class attributes_, as turning them into read-only properties looks more confusing and less clear.

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

## Solution for Class Attributes: Usage

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

Here, the attribute `test` is just marked with the assignment using `Readonly.Attribute`; the desired constant value of any type is moved to an actual argument of the call. The object `Attribute` is the inner class of the class `Readonly`; the whole line is the call to its constructor and assignment.

Here is the idea: the entire trick is performed by the metaclass: if the attribute is assigned to a `Readonly.Attribute` object, instantiation of the class object removes this attributes and creates matching read-only property exposed by another metaclass. It may sounds tricky, but... it is really pretty tricky. [Below, we can see how it works.](#heading.how-it-works3f)

In fact, `ReadonlyBase` base class does not have to be used. It is shown in this code sample due to different syntax of Python 2 and Python 3. The class `Foo` could directly setup its _metaclass_, without any base classes. The only problem is the different syntax. Let's consider this unpleasant Python problem and its work-around.

### Unification of Python 2 and 3 in the Demo

The usage sample [shown above](heading.the-solution3a-usage) lacks the definition of the class `ReadonlyBase`. Without this class, the class `Foo` could be created directly from the class `Readonly` used as its metaclass, using the following syntax:

<pre lang="Python">
# Python 2.*.*:
class Foo(object, metaclass = Readonly):
    # ...</pre>

<pre lang="Python">
# Python 3.*.*:    
class Foo(object):
    __metaclass__ = Readonly
    # ...</pre>

Alternatively, the base class `ReadonlyBase` could have been created in the same way. Instead, the file "demo.py" uses creation of an equivalent class object using _metaprogramming_ approach: 

<pre lang="Python">ReadonlyBase = Readonly(str(), (), {})</pre>

This piece of code is compatible with both lines of Python versions. To understand how it works, it's enough to know that a metaclass is just a class derived (directly or indirectly) from the class `type`. The call to its constructor creates an object which is a class: it has all the properties of a class and can be used as a class, and possibly, depending on the second parameter (`bases`), as a metaclass.

At this point, the usage is explained. Now, it's time to show how the metaclass `Readonly` turns the class attributes marked by the assignment into read-only properties.

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
        for name, value in clone.items():
            if not isinstance(value, metaclass.Attribute):
                continue;
            getattr(NewMetaclass, DefinitionSet.attributeContainerName)[name] = value.value
            aProperty = property(getAttrFromMetaclass(name))
            setattr(NewMetaclass, name, aProperty)
            classdict[name] = aProperty
            classdict.pop(name, None)               
        return type.__new__(NewMetaclass, classname, bases, classdict)</pre>

It is easy to show but harder to explain.

First of all, for all classes using `Readonly` as a metaclass, this metaclass is used only for the instantiation of a class object. At the moment of instantiation, the class object is created with a different metaclass named `NewMetaclass`, individual instance for each class instance. It is called "New" because it is ultimately used in the call `type.__new__(NewMetaclass, classname, bases, classdict)`.

Each instance of `NewMetaclass` is different. First of all, it is used as a container of all instances of the class `Readonly.Attribute` to be used by the class being initialized. Second of all, it is used as a container of some properties each named exactly as original class attribute to be re-worked into a read-only property.

When the original set of attributes of the class is traversed, the `Readonly.Attribute` instances are created and placed in the dictionary `NewMetaclass.attributeContainer`. For each such attribute, the property object is created using the constructor `property()`. For each distinct attribute name, such property is initialized with `lambda` expression generated based in the name, returning the value retrieved from `attributeContainer`.

During these manipulations, original class dictionary passed to `type._new_` if modified to remove original wanna-be-read-only class attributes. Before the traversal, the dictionary is cloned, otherwise we could face exception (in case of Python 3) caused by the attempt of modification of a dictionary being iterated.

Isn't that quite enough? No. We can make one big step further.

## What to Do with Instance Attributes?

Can the same mechanism be used for instance attributes, too?

Perhaps we would not bother if we needed only instance attributes and not class attributes. But when the mechanism of using `Readonly.Attribute` is already available, it would be more natural to have more concise and uniform look for both class and instance attributes:

<pre lang="Python">
class Foo(ReadonlyBase): # or make Readonly a metaclass of Foo, see above
    bar = 100
    test = Readonly.Attribute(13)
    def __init__(self):
        self.a = 1
        self.b = Readonly.Attribute(3.14159)</pre>

So, how to achieve similar read-only effect on the instance attributes, such as `b`? This is shown below.

## Generalized Solution

Surprisingly, applying the similar technique to instance attribute appears much trickier than with class attributes.

The major problem here is working with several instances of the class. Implementation of a property, read-only or not, require modification of the instance class. It can be easily done in the `__new__` method of the metaclass, but it would work only on one instantiation of this class. On the attempt of creating of the second instance, a constructor assigning `Readonly.Attribute` to the same attribute will fail, because the modified class already made to provide read-only functionality for this attribute. Therefore, we come to the situation when we need to create a separate class for each instance. 

The real trick is to inject a hook in the class constructor, which is done via the call to `type.__call__` in the body of the method `__call__` of the metaclass.

When this call creates an `instance`, we need another instance of the class created dynamically. This new instance, `newInstance`, is created from the dynamically-created class `NewClass` without a constructor. Now, using two instances and two classes, new and old ones, we can manipulate instance attributes to distribute them between `newInstance` --- for read-write instance attributes and `NewClass` --- for read-only properties replacing instance attributes: 

<pre lang="Python">
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
                        getattr(
                            newClass,
                            DefinitionSet.attributeContainerName)[name] = value.value
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
</pre>

Note that `getAttrFromClass` is reused between different classes, the class of the instance used for implementation of instance read-only properties and for metaclass, used for implementation of class read-only properties. However, the mechanism of the substitution is different.

Another trick is "hiding" the dictionary instance stored in the class and given the attribute name `DefinitionSet.attributeContainerName`. With such name, this attribute cannot appear as a result of "usual" operation dot-notation syntax, `instance.attribute = value`; it can only be operated via the methods `getattr/setattr/delattr/hasattr`. This seems to be really important, because it helps to avoid all possible collision with user attributes based on dot notation, even if the user uses attribute names with any number of underscores. This way, the implementation does not rely on any kind of naming conventions, so typical for Python developers.

## Versions

**v.1.0.0**: Initial fully-functional version.
**v.1.0.1**: Minor fixes.
**v.2.0.0**: Stable version; Demo comes with Python 2 and 3 unification [explained above](#heading.unification-of-python-2-and-3-in-the-demo).
**v.3.0.0**: Major [generalization](#heading.generalized-solution) of the mechanism to both class and instance attributes.