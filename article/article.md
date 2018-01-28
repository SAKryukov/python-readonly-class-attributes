Python Readonly Class Attributes: Complete Solution[](title)

[*Sergey A Kryukov*](https://www.SAKryukov.org)

## Contents[](notoc)

[](toc)

## Introduction

We shall consider the cases where some classes are created dynamically. In essence, this is the same as creation of objects.

## NamedDictionary

## Enumeration

## Time for Metaclasses

### No Pseudo-Hidden Objects

#### Hiding in Function

### No Hiding

### Inaccessible Attributes

```
def makeInaccessibleAttributeName(cls, name):
    return cls.DefinitionSet.inaccessibleNamePrefix + name 
```

Python developer are strange people. They defend their language, in the case of SA???

In Python, as in some other scripting languages, such as JavaScript, access to objects can be limited by putting some code inside a function.

### "A new-style class can't have only classic bases"

```
bases.append(object)
```