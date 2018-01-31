class Meta(type):
    @property
    def RO(self):
        return 13

# Below, the use of base class Meta(str(), (), {}) is the
# invariant form of using a class Meta as a metaclass,
# suitable for both Python 2.*.* and 3.*.*:

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
# read-only attributes

#...
print (DefinitionSet.durationSeconds)  
